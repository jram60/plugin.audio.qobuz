import os
import sys

import xbmcaddon
import xbmc

import tempfile

from icacheable import ICacheable
from api import QobuzApi
from mydebug import log, info, warn
from utils import _sc
from track import QobuzTrack
from icacheable import ICacheable
from getrecommandation import QobuzGetRecommandation
from product import QobuzProduct
from userplaylists import QobuzUserPlaylists
from playlist import QobuzPlaylist
from searchtracks import QobuzSearchTracks
from searchalbums import QobuzSearchAlbums

###############################################################################
# Class QobuzXbmc
###############################################################################
class QobuzXbmc:
    fanImg = xbmc.translatePath(os.path.join('resources/img/','playlist.png'))
    def __init__(self):
        self.data = ""
        self.conn = ""
        self.Api = QobuzApi(self)
        self.__playlists = {}
        self._handle = int(sys.argv[1])
        self.cacheDir = os.path.join(tempfile.gettempdir(),'qobuz_xbmc')
        info(self, "cacheDir: " + self.cacheDir)
        if os.path.isdir(self.cacheDir) == False:
            os.makedirs(self.cacheDir)
            info("Make cache directory: " + self.cacheDir)

    def login(self,user,password):
        info(self, "Try to login as user: " + user)
        return self.Api.login(user,password)

    def is_logged(self):
        return self.Api.userid

    def getPlaylist(self,id):
        return QobuzPlaylist(self, id)

    def getProduct(self,id):
        return QobuzProduct(self, id)

    def getUserPlaylists(self):
        return QobuzUserPlaylists(self)

    def getQobuzAlbum(self, id):
        return QobuzAlbum(self, id)

    def getTrack(self,id):
        return QobuzTrack(self,id)
    
    def getEncounteredAlbum(self):
        return QobuzEncounteredAlbum(self)
    
    def getQobuzSearchTracks(self):
        return QobuzSearchTracks(self)

    def getQobuzSearchAlbums(self):
        return QobuzSearchAlbums(self)
    
    def watchPlayback( self ):
        if not self.player.isPlayingAudio():
            self.Timer.stop()
            exit(0)
        print "Watching player: " + self.player.getPlayingFile() + "\n"
        self.Timer = threading.Timer( 6, self.watchPlayback, () )
        self.Timer.start()


    def getRecommandation(self,genre_id):
        return QobuzGetRecommandation(self, genre_id)
    
#    def download_track_withurl(self,file_name,url):
#        u = urllib2.urlopen(url)
#        f = open(file_name, 'wb')
#        meta = u.info()
#        file_size = int(meta.getheaders("Content-Length")[0])
#        print "Downloading: %s Bytes: %s" % (file_name, file_size)
#        file_size_dl = 0
#        block_sz = 8192
#        while True:
#            buffer = u.read(block_sz)
#            if not buffer:
#                break
#            file_size_dl += len(buffer)
#            f.write(buffer)
#            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
#            status = status + chr(8)*(len(status)+1)
#            print status,
#        f.close()
#        u.close()

    def getRecommandation(self, genre_id,type):
        return QobuzGetRecommandation(self, genre_id, type)


#    def tag_track(self,track,file_name,album_title="null"):
#        audio = FLAC(file_name)
#        audio["title"] = track['title']
#        
#        if album_title == "null":
#            audio["album"] = track['album']['title']
#            audio["genre"] = track['album']['genre']['name']
#            audio["date"] = track['album']['release_date']
#        else:
#            audio["album"] = album_title
#        
#        #audio["genre"] = self.pdata['product']['genre']['name']
#        #audio["date"] = self.pdata['product']['release_date'] 
#        
#        audio["length"] = track['duration']
#        audio["artist"] = track['interpreter']['name']
#        audio["discnumber"] = track['media_number']
#        audio["tracknumber"] = track['track_number']
#        audio.pprint()
#        audio.save()
#     
#     
#    def download_track(self,track,context,context_id,album_title="null"):
#        url=self.Api.get_track_url(track['id'],context,context_id) 
#        if album_title == "null":
#            track_album=track['album']['title']
#        else:
#            track_album=album_title 
#        file_name = track['interpreter']['name'] +" - "+ track_album + " - "+track['track_number']+" - "+track['title']+".flac"
#        self.download_track_withurl(file_name,url)
#        if album_title != "null":
#            self.tag_track(track,file_name,album_title)
#        else:
#            self.tag_track(track,file_name)

#===============================================================================
# class QobuzGetRecommandation():
# 
#    def __init__(self, qob,):
#        self.Qob = qob
#        self._raw_data = {}
#        
#    def get(self, genre_id, limit = 100):
#        self._raw_data = self.Qob.Api.get_recommandations(genre_id, limit)
#        pprint.pprint(self._raw_data)
#        return self
#        
#    def length(self):
#        pprint.pprint(self._raw_data)
#        return len(self._raw_data)
#    
#    def add_to_directory(self):
#        n = self.length()
#        h = int(sys.argv[1])
#        for t in self._raw_data:
#            title = _sc(t['title'])
#            interpreter = _sc(t['subtitle'])
#            #print "Interpreter: " + interpreter + "\n"
#            #print "Title: " + t['title']
#            year = int(t['released_at'].split('-')[0]) if t['released_at'] else 0
#            u = sys.argv[0] + "?mode=" + str(MODE_SONG) + "&id=" + str('' + t['id'])
#            #(sh,sm,ss) = t['duration'].split(':')
#            #duration = (int(sh) * 3600 + int(sm) * 60 + int(ss))
#            item = xbmcgui.ListItem('test')
#            item.setLabel(interpreter + ' - ' + _sc(t['subtitle']) + ' - ' + _sc(t['title']))
#            item.setInfo(type="Music",infoLabels={
#                                                   #"count":+,
#                                                   "title":  title,
#                                                   "artist": interpreter,
#                                                   "album": _sc(t['subtitle']),
#                                                   # "tracknumber": '0',
#                                                   "genre": 'unavailable',
#                                                   "comment": "Qobuz Stream",
#                                                   # "duration": duration,
#                                                   "year": year
#                                                   })
#            item.setPath(u)
#            item.setProperty('Music','true')
#            item.setProperty('IsPlayable','true');
#            item.setProperty('mimetype','audio/flac')
#            item.setThumbnailImage(t['image']['large'])
#            xbmcplugin.addDirectoryItem(handle=h ,url=u ,listitem=item,isFolder=False,totalItems=n)
#            xbmcplugin.setContent(h,'songs')
#        #xbmcplugin.setPluginFanart(int(sys.argv[1]), self.Qob.fanImg)       
#===============================================================================



###############################################################################
# Class QobuzAlbum
###############################################################################
#class QobuzAlbum(ICacheable):
#
#    def __init__(self, qob, id):
#        self.Qob = qob
#        self.id = id
#        self._raw_data = []
#        self.cache_path = os.path.join(
#                                        self.Qob.cacheDir,
#                                        'album-' + str(self.id) + '.dat'
#        )
#        self.cache_refresh = 600
#        self.fetch_data()
#
#    def _fetch_data(self):
#        #ea = self.Qob.getEncounteredAlbum()
#        data = self.Qob.Api.get_product(self.id)
#        #for a in data['tracks']:
#        #    ea.add(a)
#        return data
#
#    def length(self):
#        return len(self._raw_data['tracks'])
#
#    def add_to_directory(self):
#        n = self.length()
#        h = int(sys.argv[1])
#        for t in self._raw_data['tracks']:
#            title = _sc(t['title'])
#            if t['streaming_type'] != 'full':
#                warn(self, "Skipping sample " + title.encode("utf8","ignore"))
#                continue
#            interpreter = _sc(t['interpreter']['name'])
#            year = int(t['album']['release_date'].split('-')[0]) if t['album']['release_date'] else 0
#            u = sys.argv[0] + "?mode=" + str(MODE_SONG) + "&id=" + str(t['id'])
#            (sh,sm,ss) = t['duration'].split(':')
#            duration = (int(sh) * 3600 + int(sm) * 60 + int(ss))
#            item = xbmcgui.ListItem('test')
#            item.setLabel(interpreter + ' - ' + t['album']['title'] + ' - ' + t['track_number'] + ' - ' + t['title'])
#            item.setInfo(type="Music",infoLabels={
#                                                    "count":+self.id,
#                                                   "title":  title,
#                                                   "artist": interpreter,
#                                                   "album": _sc(t['album']['title']),
#                                                   "tracknumber": int(t['track_number']),
#                                                   "genre": _sc(t['album']['genre']['name']),
#                                                   "comment": "Qobuz Stream",
#                                                   "duration": duration,
#                                                   "year": year
#                                                   })
#            item.setPath(u)
#            item.setProperty('Music','true')
#            item.setProperty('IsPlayable','true');
#            item.setProperty('mimetype','audio/flac')
#            item.setThumbnailImage(t['album']['image']['large'])
#            xbmcplugin.addDirectoryItem(handle=h ,url=u ,listitem=item,isFolder=False,totalItems=n)
#        xbmcplugin.setContent(h,'songs')
#        #xbmcplugin.setPluginFanart(int(sys.argv[1]), self.Qob.fanImg)


class QobuzPlayer(xbmc.Player):
    def __init__(self, type):
        super(QobuzPlayer, self).__init__(type)
        self.id = None
        self.last_id = None
    
    def onPlayBackEnded(self, id):
        print "Stopping file with id" + str(self.last_id)
    
    def set_track_id(self, id):
        if self.id:
            self.last_id = self.id
        self.id = id
        
class QobuzEncounteredAlbum(ICacheable):
    # Constructor
    def __init__(self,qob):
        self.Qob = qob
        self._raw_data = {}
        self.cache_path = os.path.join(self.Qob.cacheDir,
                                        'encoutered_albums' + '.dat')
        self.cache_refresh = None

    # Methode called by parent class ICacheable when fresh data is needed
    def _fetch_data(self):
        return self._raw_data

    def add(self, album):
        id = str(album['id'])
        print "Id: " + id + "\n"
        if self._raw_data[id]:
            info(self, "AlbumID: " + id + ' already present')
        self._raw_data[id] = album
        self._save_cache_data(album)
    