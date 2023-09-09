from flask import jsonify, request, Response

from Commons.models import Playlist, Song
from Commons.database import session

class SearchAPI:
    endpoints = ['Search']
    def __init__(self, request):
        self.request = request

    def _register_API_hit(self, endpoint):
        return 0

    def _validate_request(self, endpoint):
        return True, "", 200
    
    def _extract_query_params(self, entity, value):
        '''
        /album/meliora                 album=meliora
        /album/                        album=all
        /album/meliora?entity&Value    album=meliora
        /album?entity&Value            album=value
        ?entity&value                  entity=value 
        ?entity                        entity=all
        '''
        if not entity:
            if 'entity' in self.request.args:
                entity = self.request.args.get('entity')

        if not value:
            if 'value' in self.request.args:
                value = self.request.args.get('value')
            else:
                value = 'all'

        return entity, value
    

    # Support both tese URLs formats:
    # /Search/album/Meliora
    # /Search?entity=album&value=Meliora
    # if value is not passed, return all
    def Search(self, entity=None, value=None):
        endpoint = 'Search'
        if not entity:
            valid, msg, http_code = self._validate_request(endpoint)
            if not valid:
                return Response(msg, status=http_code)
                 
        self._register_API_hit(endpoint)

        entity, value = self._extract_query_params(entity, value)
        valid_entities = ['album', 'artist', 'playlist', 'title']
        if entity not in valid_entities:
            return Response("Invalid Request", status=400)
        
        try: 
            match entity:
                case 'playlist':
                    q = session.query(Playlist)
                    q = q.filter(
                            Playlist.name.like(f"{value}%")
                        )
                    result = q.all()
                    response = {'data': [pl.__serial__() for pl in result]}

                case 'album':
                    q = session.query(Song)
                    q = q.filter(Song.album.like(f"{value}%"))
                    q = q.order_by(Song.track_num)
                    result = q.all()

                    response = {'data':{}}
                    for song in result:
                        if song.album not in response['data']:
                            response['data'][song.album] = []
                        response['data'][song.album].append(song.__serial__())

                case 'artist':
                    # Consider comma separated multiple
                    # song artists and 'ft' artists.
                    # %song_artist% is avoided as meaningless superstrings will also qualify
                    q = session.query(Song)
                    q = q.filter(
                            or_(
                                Song.album_artist.like(f"{value}%"),
                                Song.song_artist.like(f"{value}%"),
                                Song.song_artist.like(f"%,_{value}%"),
                                Song.song_artist.like(f"%ft_{value}%")
                            )
                        ).order_by(Song.track_num)
                    result = q.all()

                    response = {'data': []}
                    for song in result:
                        response['data'].append(song.__serial__())

                case 'title':
                    q = session.query(Song)
                    q = q.filter(Song.title.like(f"{value}%"))
                    result = q.all()
                    response = {'data': [song.__serial__() for song in result]}

        except Exception as e:
            return Response("Internal Server Error", status=500)
        return jsonify(response), 200

