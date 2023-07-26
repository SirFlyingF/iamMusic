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
    song_name = Column(String(64), nullable=False)
    path = Column(String(256), nullable=False)
    song_artist = Column(String(64))
    duration = Column(Integer, nullable=False) # Song length in sec
    track_num = Column(Integer)
    album_name = Column(String(64))
    album_artist = Column(String(64))
    #_playlists = relationship('Playlist', secondary=PlaylistSongReltn, backref='Song')

    def __init__(self):
        super().__init__()

    def __serial__(self):
        dict = {}
        dict['song_id'] = self.song_id 
        dict['song_name'] = self.song_name
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
    _songs = relationship('Song', secondary=PlaylistSongReltn, backref='Playlist')

    def __init__(self):
        super().__init__()
