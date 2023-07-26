from flask import jsonify, request, Response

from Commons.models import *
from Commons.database import session

from base64 import b64encode, b64decode
from mutagen.id3 import ID3, APIC
import os


class Song:
    def __init__(self):
        return 0

    def dispatch(self, request):
        match (request.method):
            case 'GET':
                return GetSongs(request)
            case 'POST':
            case 'PUT':
                return AddSongs(request)
        return Response("Invalid request", status=400)


    def _ismp3(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower()=='mp3'


    # Returns a list of all songs
    # Sorted by Album, Track number
    def GetSongs(request):
        songs = session.query(Song).order_by(Song.track_num).all()

        response = {}
        for song in songs:
            if song.album_name == None or song.album_name == "":
                if 'Unknown Album' not in response:
                    response['Unknown Album'] = {}
                    response['Unknown Album'][songs] = []
                    response['Unknown Album']['album_artist'] = song.album_artist
                    response['Unknown Album']['album_artwork'] = None
                    response['Unknown Album'][songs].append(song._serial_())
            else:
                if song.album_name not in response:
                    response[song.album_name] = {}
                    response[song.album_name][songs] = []
                    response[song.album_name]['album_artist'] = song.album_artist
                
                response[song.album_name][songs].append(song._serial_())

                # Consider storing base64 encoded artwork in SQL table
                audio.ID3(song.path)
                if 'APIC' not in audio:
                    response[song.album_name]['artwork'] = None
                else:
                    artwork = audio['APIC'] 
                    # t = {'b64':b64encode(bytes(artwork.data)).decode(), 'mime':artwork.mime}
                    response[song.album_name]['artwork'] = {'img' : artwork.data, 'mime' : artwork.mime}

        return jsonify(response)    



    # Takes the .mp3 file and extracts metadata.
    # Saves file in File System and metadata in SQL
    # Redirects to Landing page on success
    def AddSong(request):
        try:   
            if 'file' not in request.files:
                raise TypeError

            file = request.files['file']

            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                raise TypeError

            if not (file and _ismp3(file.filename)):
                raise TypeError

            # Need to save a temp file as werkzeug's FileStorage may not be
            # compatible with ID3's fileobj or fspath object
            temp_path = os.path.join(app.config['TEMP_MEDIA_PATH'], filename)
            file.save(temp_path)
        except TypeError:
            return Response("Invalid File", status=400)

        try:
            # see https://mutagen.readthedocs.io/en/latest/api/id3_frames.html#id3v2-3-4-frames
            # for the ID tags reference
            audio = ID3(temp_path)
            dict = {}
            song_name = audio['TIT2']
            album_artist = audio['TSO2']
            album_name = audio['TALB'] #or TOAL
            path = os.path.join(app.config['PERM_MEDIA_PATH'], album_artist, album_name)
            song_artist = audio['TPE1']
            duration = audio['TLEN'] / 1000 #convert ms to secs
            track_num = audio['TRCK']
        except KeyError:
            return Response("Invalid File", status=400)

        # Cache Metadata to SQL
        try:
            song = Song(
                        song_name = song_name,
                        path = path,
                        song_artist = song_artist,
                        duration = duration,
                        track_num = track_num,
                        album_name = album_name,
                        album_artist = album_artist
                        )
            session.add(song)
            session.commit()
        except e:
            session.rollback()
            return Response("Error saving file", status=500)

        # Save MP3 file to PERM_MEDIA_PATH and Delete it from TEMP_MEDIA_PATH
        try:
            tempf = open(temp_path, 'rb')
            permf = open(path, 'wb')
            while tempf:
                permf.write(tempf.read())
            tempf.close()
            os.remove(temp_path)
            permf.close()
        except e:
            return Response("Internal Server Error", status=500)

        return Response("Success", status=200)
