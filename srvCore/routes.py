from srvCore import app
from flask import request, Response

from Commons.models import *
from Commons.database import session

from base64 import b64encode, b64decode
from mutagen.id3 import ID3, APIC
import os

from srvCore.SongAPI import SongAPI
from srvCore.PlaylistAPI import PlaylistAPI
from srvCore.SearchAPI import SearchAPI


'''
TODO
# Write OpenAPI document
# Format search-by-artist response
# Implement app factory - Prod, Test, Debug
# Implement Logging
# Implement API hit counter
# Add support for seek
# Add support for Album Artwork
# Add Authorization service
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
    if not song_id:
        return Response("No song_id", status=400)
    
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


@app.route('/song/<int:song_id>', methods=['GET'])
@app.route('/song', methods=['POST', 'GET'])
def DispatchSongAPI(song_id=0):
    API = SongAPI(request)
    match request.method:
        case 'POST':
            return API.AddSong()
        case 'GET':
            return API.GetSong(song_id)
    return Response("Resource Not Found", status=404)


@app.route('/playlist/<int:playlist_id>', methods=['GET'])
@app.route('/playlist', methods=['POST', 'GET', 'PATCH', 'DELETE'])
def DispatchPlaylistAPI(playlist_id=0):
    API = PlaylistAPI(request)
    match request.method:
        case 'GET':
            return API.GetPlaylist(playlist_id)
        case 'POST':
            return API.AddPlaylist()
        case 'PATCH':
            return API.ModifyPlaylist()
        case "DELETE":
            return API.RemovePlaylist() 
    return Response("Resource Not Found", status=404)


@app.route('/search/<string:entity>/<int:value>', methods=['GET'])
@app.route('/search', methods=['GET'])
def DispatchPlaylistAPI(entity=None, value=None):
    API = SearchAPI(request)
    return API.Search(entity)