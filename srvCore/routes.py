from srvCore import app
from srvCore.Playlist import Playlist
from srvCore.Song import Song

from flask import request, Response

from Commons.models import *
from Commons.database import session


'''
TODO
#
'''

# This decorator adds the function you decorate with it to a list of functions
# on a Flask object instance (app in our case). This list is then iterated over
# in reverse order when the appcontext is torn down, with each function being
# passed the exception triggering the teardown, or a placeholder.
@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()

@app.route('/play/<int:song_id>', methods=['GET'])
# Starts an audio stream
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
                data = fmp3.read(1024)
    return Response(stream(), mimetype="audio/mpeg")

@app.route('/song')
def song():
    return Song.dispatch(request)

@app.route('/playlist')
def playlist():
    return Playlist.dispatch(request)
