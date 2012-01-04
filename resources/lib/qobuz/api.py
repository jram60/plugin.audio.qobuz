#!/usr/bin/python
import httplib,json,time,urllib2,urllib,hashlib,mutagen
from mutagen.flac import FLAC
import pprint

class QobuzApi:

    def __init__(self,qob):
        self.qob = qob
        self.headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        self.authtoken = None
        self.userid = None

    def _api_request(self,params,uri):
        self.conn = httplib.HTTPConnection("player.qobuz.com")
        self.conn.request("POST",uri,params,self.headers)
        response = self.conn.getresponse()
        response_json = json.loads(response.read())
        return response_json

    def get_track_url(self,track_id,context_type,context_id ,format_id = 6):
        params = urllib.urlencode({
                                   'x-api-auth-token':self.authtoken,
                                   'track_id': track_id ,
                                   'format_id': format_id,
                                   'context_type':context_type,
                                   'context_id':context_id})
    # add try catch here
        done = False
        while done == False:
            try:
                data = self._api_request(params,"/api.json/0.1/track/getStreamingUrl")
                done = True
            except:
                print "try again"
        # xbmc.log(json.dumps(data))
            url = data[u'streaming_url']
        return data


    def get_track(self,trackid):
        params = urllib.urlencode({'x-api-auth-token':self.authtoken,'track_id': trackid})
        data = self._api_request(params,"/api.json/0.1/track/get")
        return data

    def get_playlists1(self):
        params = urllib.urlencode({'x-api-auth-token':self.authtoken,'user_id': self.userid})
        data = self._api_request(params,"/api.json/0.1/playlist/getUserPlaylists")
        return self._parsePlaylists(data)

    def get_user_playlists(self):
        params = urllib.urlencode({'x-api-auth-token':self.authtoken,'user_id': self.userid})
        data = self._api_request(params,"/api.json/0.1/playlist/getUserPlaylists")
        return data

    def _parsePlaylists(self,items):
        i = 0
        list = []
          #if 'playlist' in data:
          #      playlists = items['result']['playlists']
          #elif len(items) > 0:
          #      playlists = items
          #else:
          #      return []

          #while (i < len(playlists)):
          # print json.dumps(items)
        for playlist in items:
          # s = playlists[i]
            list.append([playlist['playlist']['name'].encode('ascii','ignore'),playlist['playlist']['id']])
          #i = i + 1
        return list

    def getPlaylistSongs(self,playlistID):
        result = self._callRemote('getPlaylistSongs',{'playlistID' : playlistID});
        if 'result' in result:
            return self._parseSongs(result)
        else:
            return []

    def login(self,user,password):
        params = urllib.urlencode({'x-api-auth-token':'null','email': user ,'hashed_password': hashlib.md5(password).hexdigest() })
        data = self._api_request(params,"/api.json/0.1/user/login")
        if not 'user' in data:
            return None
        self.authtoken = data['user']['session_id']
        self.userid = data['user']['id']
        return self.userid

    def get_playlist(self,playlist_id=39837):
        params = urllib.urlencode({'x-api-auth-token':self.authtoken,'playlist_id':playlist_id,'extra':'tracks'})
        return self._api_request(params,"/api.json/0.1/playlist/get")

    def get_album_tracks(self,album_id):
        params = urllib.urlencode({'x-api-auth-token':self.authtoken,'product_id':album_id})
        return self._api_request(params,"/api.json/0.1/product/get")


if __name__ == '__main__':
    pass