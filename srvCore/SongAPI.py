from srvCore import app

from flask import jsonify, request, Response

from Commons.models import Song
from Commons.database import session

from base64 import b64encode, b64decode
from mutagen.id3 import ID3, APIC
import os

class SongAPI:
    endpoints = ['AddSong', 'GetSong']

    def __init__(self, request):
        self.request = request
    
    def _ismp3(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower()=='mp3'

    def _register_API_hit(self, endpoint):
        pass

    def _validate_request(self, endpoint):
        match endpoint:
            case 'AddSong':
                file = self.request.files.get('file', None)
                if file is None or file.filename is None:
                    return False, "AddSong - Invalid file or filename", 400
                if not self._ismp3(file.filename):
                    return False, "AddSong - File type is not mp3", 400
                return True, "", 200

            case 'GetSong':
                if not self.request.query_string or self.request.query_string == "":
                    return False, "No Query String", 400
                if 'song_id' not in self.request.args:
                    return False, "No Query String", 400
                return True, "", 200

        return False

    def _extract_metadata(self, file, form):
        try:
            # If form does not have data, look in ID3 tags.
            # see https://mutagen.readthedocs.io/en/latest/api/id3_frames.html#id3v2-3-4-frames
            # for the ID tags reference
            audio = ID3(file)
            title = form.get('title') if form.get('title') else file.filename

            # Expect front end to fill up album and album_artist fields in form by
            # either user input or reading ID3 tags itself. But we read ID3 as well.
            album = form.get('album')
            if not album:
                if 'TALB' in audio:
                    album = audio['TALB'].text[0] #or audio['TOAL']
                else:
                    album = 'Unknown Album' 

            album_artist = form.get('album')
            if not album_artist:
                if 'TSO2' in audio:
                    album = audio['TSO2'].text[0]
                else:
                    album_artist = 'Unknown Artist'
            
            # An album may be a compilation from different artists, hence treating
            # song artist as different from album artist. Also, Song artist may have 
            # featuring and collaboration artists not credited in the album
            song_artist = form.get('song_artist')
            song_artist = audio['TPE1'].text[0] if not song_artist else None
            
            track_num = form.get('track_num')
            track_num = audio['TRCK'].text[0] if not track_num else None

            # https://www.w3.org/2000/10/swap/pim/mp3/mp3info.py 
            # https://chunminchang.github.io/blog/post/estimation-of-mp3-duration
            # Consider estimating duration. Needed to support seek
            duration = audio['TLEN'].txt[0] if 'TLEN' in audio else None

            path = os.path.join(app.config['MEDIA_PATH'], album_artist, album)

            metadata = {
                'title' : title,
                'path' : path,
                'song_artist' : song_artist,
                'duration' : duration,
                'track_num' : track_num,
                'album' : album,
                'album_artist' : album_artist
            }
            return metadata
        except KeyError:
            return None
        

    # Takes the .mp3 file and extracts metadata.
    # Saves file in File System and metadata in SQL
    def AddSong(self):
        endpoint = 'AddSong'
        valid, msg, http_code = self._validate_request(endpoint)
        if not valid:
            return Response(msg, status=http_code)
        self._register_API_hit(endpoint)

        try:   
            file = self.request.files.get('file')
            metadata = self._extract_metadata(file, self.request.form)

            if not metadata:
                return Response("Error extracting metadata", status=400)

            # Create directories before appending filename to path
            os.makedirs(metadata['path'], 0o777, exist_ok=True)
            metadata['path'] = os.path.join(metadata['path'], file.filename)
            file.save(metadata['path'])

            # Save Metadata to SQL
            song = Song(metadata)
            session.add(song)
            session.flush()
            session.commit()

            # Consider storing base64 encoded artwork in SQL table
            #audio = ID3(song.path) 
            #if 'APIC' not in audio:
            #    response[song.album]['artwork'] = None
            #else:
            #    artwork = audio['APIC'] 
            #    # t = {'b64':b64encode(bytes(artwork.data)).decode(), 'mime':artwork.mime}
            #    response[song.album_name]['artwork'] = {'img' : artwork.data, 'mime' : artwork.mime}
        except OSError as e:
            session.rollback()
            return Response("Error saving file"+str(e), status=500)
        except Exception as e:
            session.rollback()
            return Response("Error saving file"+str(e), status=500)

        return jsonify({"song_id" : song.song_id}), 200


    # Returns song details by song_id
    def GetSong(self, song_id=0):
        endpoint = 'GetSong'
        if song_id == 0:
            # check if query string has song_id
            valid, msg, http_code = self._validate_request(endpoint)
            if not valid:
                return Response(msg, status=http_code)
        self._register_API_hit(endpoint)

        try:
            if song_id == 0:
                song_id = self.request.args.get('song_id')

            song = session.query(Song).get(song_id)
            
            response = {'data' : song.__serial__()} 
        except Exception as e:
            return Response("Internal Server Error", status=500)
        
        return jsonify(response)  