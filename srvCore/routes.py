from srvCore import app
from flask import request, Response

from Commons.models import *
from Commons.database import session

from base64 import b64encode, b64decode
from mutagen.id3 import ID3, APIC
import os

from srvCore.SongAPI import SongAPI
from srvCore.PlaylistAPI import PlaylistAPI


'''
TODO
# Implement SearchSong handler
# Implement app factory - Prod, Test, Debug
# Implement Logging
# Implement API hit counter
# Add support for seek
# Add support for Album Artwork
'''

# This decorator adds the function you decorate with it to a list of functions
# on a Flask object instance (app in our case). This list is then iterated over
# in reverse order when the appcontext is torn down, with each function being
# passed the exception triggering the teardown, or a placeholder.
@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove() 

# Starts an audio stream
@app.route('/play/<int:song_id>', methods=['GET'])
def play(song_id):
    path = session.query(Song)\
                  .filter(
                        Song.song_id==song_id,
                  ).first().path
    def stream():
        with open(path, "rb") as fmpeg:
            data = fmpeg.read(1024)
            while data:
                yield data
                data = fmpeg.read(1024)
    return Response(stream(), mimetype="audio/mpeg")  

@app.route('/song', methods=['POST', 'GET'])
def DispatchSongAPI():
    API = SongAPI(request)
    match request.method:
        case 'POST':
            return API.AddSong()
        case 'GET':
            return API.GetSongs()
        
    return Response("Resource Not Found", status=404)

@app.route('/playlist', methods=['POST', 'GET', 'PATCH', 'DELETE'])
def DispatchPlaylistAPI():
    API = PlaylistAPI(request)
    match request.method:
        case 'GET':
            return API.GetPlaylists()
        case 'POST':
            return API.AddPlaylist()
        case 'PATCH':
            return API.ModifyPlaylist()
        case "DELETE":
            return API.RemovePlaylist() 
        
    return Response("Resource Not Found", status=404)