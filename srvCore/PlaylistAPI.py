from flask import jsonify, request, Response

from Commons.models import Playlist, PlaylistSongReltn, Song
from Commons.database import session


class PlaylistAPI():
    def __init__(self, request):
        self.request = request

    def _register_API_hit(self, endpoint):
        return 0

    def _validate_request(self, endpoint):
        match endpoint:
            case 'GetPlaylist':
                if not self.request.query_string or self.request.query_string == "":
                    return False, "No Query String", 400
                if 'playlist_id' not in self.request.args:
                    return False, "No Query String", 400
                return True, "", 200
            
            case 'AddPlaylist':
                json = self.request.json
                if json is None:
                    return False, "No json", 400
                # Songs is a list of song_ids and name is the name of PL
                if {'songs', 'name'} < json.keys():
                    return False, "Invalid Request", 400
                return True, "", 200
            
            case 'ModifyPlaylist':
                json = self.request.json
                if json is None:
                    return False, "No json", 400
                # Playlist_id to denote what playlist to modify
                # add and rmv are list of song_ids to add or remove
                # nname is the new name of the playlist. Request must contain atleast one
                if ('playlist_id' not in json) or ('add' not in json and 'rmv' not in json and 'nname' not in json):
                    return False, "Invalid Request", 400
                return True, "", 200
            
            case 'RemovePlaylist':
                json = self.request.json
                if json is None:
                    return False, "No json", 400
                if 'playlist_id' not in json.keys():
                    return False, "Invalid Request", 400
                return True, "", 200

        return False, "Internal Server Error", 500
    

    # Returns playlist details by playlist_id
    def GetPlaylist(self, playlist_id=0):
        endpoint = 'GetPlaylist'

        if playlist_id == 0:
            # check if query string has song_id
            valid, msg, http_code = self._validate_request(endpoint)
            if not valid:
                return Response(msg, status=http_code)   
        self._register_API_hit(endpoint)

        try:
            if playlist_id == 0:
                playlist_id = args.get('playlist_id')

            playlist = session.query(Playlist).get(playlist_id)
            
            response = {'data' : {}}
            response['data']['name'] = playlist.name
            response['data']['playlist_id'] = playlist.playlist_id
            response['data']['songs'] = []
            for song in playlist._songs:
                response['data']['songs'].append(session.query(Song).get(song.song_id).__serial__())
        except Exception as e:
            return Response("Internal Server Error", status=500)
        
        return jsonify(response)

    # Creates Playlists
    # Accepts a json { songs : [song_id], name : str }
    # Returns a playlist_id on success
    def AddPlaylist(self):
        endpoint = 'AddPlaylist'
        valid, msg, http_code = self._validate_request(endpoint)
        if not valid:
            return Response(msg, status=http_code)
        
        self._register_API_hit()
        
        json = self.request.json
        try: 
            # Check if Playlist already exisits. 
            PL = session.query(Playlist).filter(Playlist.name==json['name']).all()
            for playlist in PL:
                if playlist.name == json['name']:
                    song_ls = [s.song_id for s in playlist._songs]
                    if song_ls == json['songs']:
                        return Response("Playlist already exists", status=200)

            # Need to manually add psr row, since we dont want
            # to insert in Song table using Cascaded inserts
            playlist = Playlist(name=json['name'])
            session.add(playlist)
            session.flush()

            # Add songs to playlist
            for song_id in json['songs']:
                psr = PlaylistSongReltn(
                                playlist_id = playlist.playlist_id,
                                song_id = song_id,
                            )
                session.add(psr)
            session.commit()
        except Exception as e:
            session.rollback()
            return Response("Internal Server Error"+str(e), status=500)

        return jsonify({'playlist_id': playlist.playlist_id}), 200


    # Modifies an existing playlist
    # Accepts json {playlist_id:int, nname:str, add:[song_id], rmv:[song_id]}
    # Returns status 200 on success
    def ModifyPlaylist(self):
        endpoint = 'ModifyPlaylist'
        valid, msg, http_code = self._validate_request(endpoint)
        if not valid:
            return Response(msg, status=http_code)

        self._register_API_hit(endpoint)

        json = request.json
        try:
            playlist = session.query(Playlist).get(json['playlist_id'])
            if not playlist:
                return Response("Playlist does not exist", status=404)
            
            # if new name is supplied, set it as new name of the playlist.
            if 'nname' in json:
                if json['nname']:
                    playlist.name = json['nname']

            # Add songs to playlist
            if 'add' in json:
                for song_id in json['add']:
                    psr = PlaylistSongReltn(
                                playlist_id = playlist.playlist_id,
                                song_id = song_id,
                            )
                    session.add(psr)

            # Remove songs from playlist
            if 'rmv' in json:
                q = session.query(PlaylistSongReltn)
                for song_id in json['rmv']:
                    q = q.filter(
                            PlaylistSongReltn.song_id==song_id
                        )
                q.delete()

            session.commit()
        except Exception as e:
            session.rollback()
            return Response("Internal Server Error", status=500)

        return Response("Success", status=200)


    # Deletes a playlist
    # Returns status 200 on success
    def RemovePlaylist(self):
        endpoint = 'RemovePlaylist'
        valid, msg, http_code = self._validate_request(endpoint)
        if not valid:
            return Response(msg, status=http_code)

        self._register_API_hit(endpoint)

        json = request.json
        try:
            session.query(PlaylistSongReltn).filter(
                        PlaylistSongReltn.playlist_id == json['playlist_id']
                    ).delete()
                    
            session.query(Playlist).filter(
                        Playlist.playlist_id == json['playlist_id']
                    ).delete()

            session.commit()
        except Exception as e:
            session.rollback()
            return Response("Internal Server Error", status=500)

        return Response("Success", status=200)

