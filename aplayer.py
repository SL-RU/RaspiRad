__author__ = 'SL_RU'
# -*- coding: utf-8 -*-
#Проигрыватель музыкальных файлов

import vlc
#import time
#import sys
from queue import Queue


def log(msg):
    #print(msg)
    pass

class Aplayer(object):
    def __init__(self, output_device):
        """Initializing Aplayer.
            output_device can be:
               'bt' - blutooth,
               'hw' - audio jack,
               'hdmi'
            """
        self.init_functions()
        self.vlc_instance = vlc.Instance()
        self.cur_player = self.vlc_instance.media_player_new()
        if(output_device == "bt"):
            self.cur_player.audio_output_device_set('alsa', 'bluetooth')
        if(output_device == "hdmi"):
            self.cur_player.audio_output_device_set('alsa', 'hdmi')
        self.tasks = Queue()
        self.song_loading = False
        self.cur_media = None
        self.cur_player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, self.on_end_event)

    playing = False
        
    def connect_bluetooth(self, a):
        self.cur_player.audio_output_device_set('alsa', 'bluetooth')

    def _play_file(self, fl):
        log("PLAY: requested file " + fl)
        self.song_loading = True
        self.cur_media = self.vlc_instance.media_new(fl)
        self.cur_player.set_media(self.cur_media)
        self.cur_player.set_position(0)
        self.cur_player.play()
        self.song_loading = False
        self.playing = True

    def play_file(self, fl):
        """Load and play requested media file"""
        self._add_task('play_file', fl)

    def _pause(self, a=0):
        if(self.cur_player is not None):
            self.cur_player.pause()
            self.playing = False

    def pause(self):
        """Pause playing media"""
        self._add_task('pause', 0)

    def _play(self, a=0):
        if(self.cur_player is not None):
            self.cur_player.play()
            self.playing = True

    def play(self):
        """Continue playing after pause()"""
        self._add_task('play', None)

    end_event_handlers = list()

    def add_endevent(self, func):
        """Set function, which will be executed after audio file's end.
            func - function, which will be executed"""
        self.end_event_handlers.append(func)

    def rem_endevent(self, func):
        self.end_event_handlers.remove(func)

    def on_end_event(self, s):
        for i in self.end_event_handlers:
            i()
        self.playing = False

    def set_pos(self, pos):
       self._add_task('set_pos', pos)
    
    def _set_pos(self, pos):
        #global self.cur_player
        if(self.cur_player != None and pos >= 0 and pos <= self.get_duration()):
            log("setting pos " + str(pos/self.get_duration()))
            self.cur_player.set_position(pos/self.get_duration())
        else:
            log("invalid position. Duration: " + str(self.get_duration()))
    def set_pos(self, pos):
       self._add_task('set_pos', pos)
    
    def get_pos(self):
        #global self.cur_player
        return self.cur_player.get_position() * self.get_duration()
    def get_duration(self):
        #global self.cur_player, self.cur_media
        if(self.cur_media != None):
            return self.cur_media.get_duration() / 1000

    def _add_task(self, func, arg):
        self.tasks.put((func, arg))
        log('APLTASK: added ' + func)

    def init_functions(self):
        self.functions = {
            'play_file': self._play_file,
            'pause': self._pause,
#            'add_endevent': self._add_endevent,
            'play': self._play,
            'set_pos': self._set_pos,
#            'rem_endevent': self._rem_endevent,       
        }

    def turn_off():
        pass

    def update(self):
        f = self.tasks.get()
        print(f)
        log('TASK: doing ' + f[0])
        self.functions[f[0]](f[1])
        log('TASK: done')
        self.tasks.task_done()

        
