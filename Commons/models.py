from sqlalchemy import ForeignKey, Column, String, Integer #Boolean, Float, DateTime
from sqlalchemy.orm import relationship
from Commons.database import Base

'''
TODO
'''

class Song(Base):
    '''
    #
    '''
    __tablename__ = 'song'
    song_id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    path = Column(String(256), nullable=False)
    song_artist = Column(String(64))
    duration = Column(Integer) # Song length in msec
    track_num = Column(Integer)
    album = Column(String(64))
    album_artist = Column(String(64))
    #_playlists = relationship('Playlist', secondary=PlaylistSongReltn, backref='Song')

    def __init__(self, metadata):
        super().__init__()
        self.title = metadata['title'],
        self.path = metadata['path'],
        self.song_artist = metadata['song_artist'],
        self.duration = metadata['duration'],
        self.track_num = metadata['track_num'],
        self.album = metadata['album'],
        self.album_artist = metadata['album_artist']

    def __serial__(self):
        dict = {}
        dict['song_id'] = self.song_id 
        dict['title'] = self.title
        dict['song_artist'] = self.song_artist
        dict['duration'] = self.duration 
        dict['track_num'] = self.track_num
        return dict


class PlaylistSongReltn(Base):
    '''
    #
    '''
    __tablename__ = 'playlist_song_reltn'
    song_id = Column(Integer, ForeignKey('song.song_id'), primary_key=True)
    playlist_id = Column(Integer, ForeignKey('playlist.playlist_id'), primary_key=True)


class Playlist(Base):
    '''
    #
    '''
    __tablename__ = 'playlist'
    playlist_id = Column(Integer, primary_key=True)
    name = Column(String(256))
    _songs = relationship('Song', secondary=PlaylistSongReltn.__tablename__, backref='Playlist')

