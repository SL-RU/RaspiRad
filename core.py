import aplayer as P
import time
import vlc
from threading import Thread
import lcd
import hardware as hw

hw.Init()

bb = hw.GPIOButton(8)
bp = hw.GPIOButton(10)
bf = hw.GPIOButton(12)

lcd.lcd_init()
lcd.lcd_string("Hello!", lcd.LCD_LINE_1);

pl = P.Aplayer("hw");


#Станции можно брать отсюда: http://nevremya.narod.ru/transmission/

stid = 0
stlist = []
with open("stations.txt", "r") as fl:
	cont = fl.readlines()
	for c in cont:
		c = c.strip()
		if c[0] != "#" and c != "":
			f = c.split(" ")
			nm = ""
			if(len(f) > 1):
				for i in range(1, len(f)):
					nm += f[i] + " "
			stlist.append((f[0], nm))

pl.play_file(stlist[stid][0])

def pl_upd():
	while(1):
		pl.update()

def lcd_upd():
	global stid, stlist
	while (1):
		try:
			nm = stlist[stid][1]
			if(nm == ""):
				nm = pl.cur_media.get_meta(vlc.Meta.Title)
			lcd.lcd_string(nm, lcd.LCD_LINE_1)
		except Exception:
			lcd.lcd_string("---  Loading  ---", lcd.LCD_LINE_1)
		tmp =     "%d %b  %H:%M:%S"
		if(int((time.clock()/3))%2):
			tmp = "%d %b %a %M:%S"
		lcd.lcd_string(str(time.strftime(tmp, time.localtime())), lcd.LCD_LINE_2)
		#time.sleep(1)

def forw():
	global stid, stlist, pl
	stid = min(stid+1, len(stlist) - 1)
	pl.play_file(stlist[stid][0])
def back():
	global stid, stlist, pl
	stid = max(stid-1, 0)
	pl.play_file(stlist[stid][0])
def play():
	global pl
	if(pl.cur_player.is_playing()):
		pl.cur_player.stop()
	else:
		pl.play()

def hot(i):
	global stid, stlist, pl
	stid = max(0, min(len(stlist), i))
	pl.play_file(stlist[stid][0])
def hot1():
	hot(0)
def hot2():
	hot(1)
def hot3():
	hot(2)
bb.click = forw
bf.click = back
bp.click = play
bb.press = hot3
bp.press = hot2
bf.press = hot1


thr = Thread(target=pl_upd)
thr.setDaemon(True)
thr.start()

thr_l = Thread(target=lcd_upd)
thr_l.setDaemon(True)
thr_l.start()

while (1):
	hw.Update()