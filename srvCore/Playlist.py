from flask import jsonify, request, Response

from Commons.models import *
from Commons.database import session


class Playlist():
    def __init__(self):
        return 0

    def dispatch(self, request):
        match (request.method):
            case 'GET':
                return GetPlaylists(request)
            case 'POST':
            case 'PUT':
                return AddPlaylists(request)
            case 'PATCH':
                return ModifyPlaylists(request)
            case "DELETE":
                return RemovePlaylists(request)  
        return Response("Invalid request", status=400)


    # Returns all playlists created by user
    # Also return song_ids and metadata
    def GetPlaylists(request):
        playlists = session.query(Playlist).all()
        response = {}
        for playlist in playlists:
            response[playlist.name] = []
            songs = playlist._songs
            for song in songs:
                response[playlist.name].append(song.__serial__())
        return jsonify(response)



    # Creates Playlists
    # Accepts a json { songs : [song_id], name : str }
    # Returns a playlist_id on success
    def AddPlaylists(request):
        json = request.json
        try:
            if json is None:
                raise KeyError
            if {'songs', 'name'} >= json.keys():
                raise KeyError
        except KeyError:
            return Response("Invalid Request", status=400)

        try:
            # Need to manually add psr row, since we dont want
            # to insert in Song table.
            playlist = Playlist(
                            name = json['name']
                        )
            session.add(playlist)
            for song_id in json['songs']:
                psr = PlaylistSongReltn(
                                playlist_id = playlist.playlist_id,
                                song_id = song_id,
                            )
                session.add(psr)
            session.commit()
        except e:
            session.rollback()
            return Response("Internal Server Error", status=500)

        return Response(jsonify({'playlist_id': playlist_id}), status=200)



    # Modifies an existing playlist
    # Accepts json {playlist_id:int, nname:str, add:[song_id], rmv:[song_id]}
    # Returns status 200 on success
    def ModifyPlaylists(request):
        json = request.json
        try:
            if json is None:
                raise KeyError
            if {'playlist_id', 'add', 'rmv'} >= json.keys():
                raise KeyError
        except KeyError:
            return Response("Invalid Request", status=400)

        try:
            # .one() may throw NoResultFound error
            playlist = session.query(Playlist).one(json['playlist_id'])
            if 'nname' in json:
                playlist.name = json['nname']

            # Add songs to playlist
            for song_id in json['add']:
                psr = PlaylistSongReltn(
                            playlist_id = playlist.playlist_id,
                            song_id = song_id,
                        )
                session.add(psr)

            # Remove songs from playlist
            q = session.query(PlaylistSongReltn)
            for song_id in json['rmv']:
                q = q.filter(
                        PlaylistSongReltn.song_id = song_id
                    )
            q.delete()

            session.commit()
        except e:
            session.rollback()
            return Response("Internal Server Error", status=500)

        return Response("Success", status=200)



    # Deletes a playlist
    # Returns status 200 on success
    def RemovePlaylists(request):
        json = request.json
        try:
            if json is None:
                raise KeyError
            if not 'playlist_id' in json.keys():
                raise KeyError
        except KeyError:
            return Response("Invalid Request", status=400)

        try:
            session.query(PlaylistSongReltn)\
                    .filter(
                        PlaylistSongReltn.playlist == json['playlist_id']
                    ).delete()
                    
            session.query(Playlist)\
                    .filter(
                        Playlist.playlist_id == json['playlist_id']
                    ).delete()

            session.commit()
        except e:
            session.rollback()
            return Response("Internal Server Error", status=500)

        return Response("Success", status=200)

