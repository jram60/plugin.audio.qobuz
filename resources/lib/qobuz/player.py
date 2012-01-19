#     Copyright 2011 Joachim Basmaison, Cyril Leclerc
#
#     This file is part of xbmc-qobuz.
#
#     xbmc-qobuz is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     xbmc-qobuz is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.   See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with xbmc-qobuz.   If not, see <http://www.gnu.org/licenses/>.

import sys
from time import time
import re
import math
import pprint

import xbmc
import xbmcplugin
import xbmcgui

from debug import info, warn, log
import qobuz
from utils.list_item import QobuzListItem_track
from data.track import QobuzTrack
from utils.tag import QobuzTagTrack
from data.track_streamurl import QobuzTrackURL
    
class QobuzPlayer(xbmc.Player):
    
    def __init__(self, type = xbmc.PLAYER_CORE_AUTO):
        super(QobuzPlayer, self).__init__()
        
    def sendQobuzPlaybackEnded(self, duration):
        qobuz.api.report_streaming_stop(self.id, duration)
    
    def sendQobuzPlaybackStarted(self,):
        qobuz.api.report_streaming_start(self.id)
        
    def play(self, id):
        lang = qobuz.lang
        info(self, "We need to play song with id: " + str(id))
        mytrack = QobuzListItem_track(id)
        mytrack.fetch_stream_url(qobuz.addon.getSetting('streamtype'))
        info(self, mytrack.to_s())
        if not mytrack.get_stream_url():
            warn(self, "Cannot get stream url for track with id: " + str(id))
            qobuz.gui.showNotification(34000, 34002)
            return False
        item = mytrack.get_xbmc_list_item()
        '''
            PLaying track
        '''
        if qobuz.addon.getSetting('notification_playingsong') == 'true':
            qobuz.gui.showNotificationH(lang(34000), item.getLabel(), item.getProperty('image'))
        '''
            We are called from playlist...
        '''
        if qobuz.boot.handle == -1:
            super(QobuzPlayer, self).play(item.getProperty('streaming_url'), item, False)
        else:
            xbmcplugin.setResolvedUrl(handle=qobuz.boot.handle,succeeded=True,listitem=item)
        '''
            May be a bad idea!!!
        '''
        xbmc.executebuiltin('Dialog.Close(all,true)')
        '''
            Waiting for song to start
        '''
        timeout = 30
        info(self, "Waiting song to start")
        while timeout > 0:
            if self.isPlayingAudio() == False:
                xbmc.sleep(250)
                timeout-=0.250
            else: 
                break
        if timeout <= 0:
            warn(self, "Player can't play track: " + item.getLabel())
            return False
        return True
