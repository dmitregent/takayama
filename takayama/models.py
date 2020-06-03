from sqlalchemy import Column, Integer, String, DateTime

from takayama.database import Base, db_session


class Scrobble(Base):
    __tablename__ = 'scrobble_easy'
    query = db_session.query_property()
    id = Column(Integer, primary_key=True)
    artist = Column(String)
    name = Column(String)
    album = Column(String)
    played_at = Column(DateTime)
    played_year = Column(Integer)
    played_month = Column(Integer)
    played_day = Column(Integer)

    def __init__(self,
                 artist=None,
                 name=None,
                 album=None,
                 played_at=None,
                 played_year=None,
                 played_month=None,
                 played_day=None):
        self.artist = artist
        self.name = name
        self.album = album
        self.played_at = played_at
        self.played_year = played_year
        self.played_month = played_month
        self.played_day = played_day

    def __repr__(self):
        return 'scrobble %r' % self.name

    @property
    def serialize(self):
        return {
            'id': self.id,
            'artist': self.artist,
            'name': self.name,
            'album': self.album,
            'played_at': self.played_at
        }
