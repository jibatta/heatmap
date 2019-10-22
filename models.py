from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Point(Base):
    __tablename__ = 'point'
    id = Column(Integer, primary_key = True)
    x_location = Column(Integer)
    y_location = Column(Integer)
    measure = relationship('Measure', backref='point')

    def __repr__(self):
        return "point {} - {}".format(self.x_location,self.y_location)

    def __init__(self, point):
        self.x_location = point.x
        self.y_location = point.y


class Ssid(Base):
    __tablename__ = 'ssid'
    id = Column(Integer, primary_key = True)
    ssid = Column(String)
    measure = relationship('Measure', backref='ssid')

    def __repr__(self):
        return "ssid {}".format(self.ssid)

    def __init__(self, ssid):
        self.ssid = ssid


class Channel(Base):
    __tablename__ = 'channel'
    id = Column(Integer, primary_key = True)
    channel = Column(String)
    measure = relationship('Measure', backref='channel')

    def __repr__(self):
        return "channel {}".format(self.channel)

    def __init__(self, channel):
        self.channel = channel


class Bssid(Base):
    __tablename__ = 'bssid'
    id = Column(Integer, primary_key = True)
    bssid = Column(String)
    measure = relationship('Measure', backref='bssid')

    def __repr__(self):
        return "bssid {}".format(self.bssid)

    def __init__(self, bssid):
        self.bssid = bssid


class Security(Base):
    __tablename__ = 'security'
    id = Column(Integer, primary_key = True)
    security_type = Column(String)
    measure = relationship('Measure', backref='security')

    def __repr__(self):
        return "security {}".format(self.security_type)
    
    def __init__(self, security_type):
        self.security_type = security_type


class Measure(Base):
    __tablename__ = 'measure'
    id = Column(Integer, primary_key = True)
    point_id = Column(Integer, ForeignKey('point.id'))
    ssid_id = Column(Integer, ForeignKey('ssid.id'))
    channel_id = Column(Integer, ForeignKey('channel.id'))
    bssid_id = Column(Integer, ForeignKey('bssid.id'))
    security_id = Column(Integer, ForeignKey('security.id'))
    rssi = Column(String)

    def __repr__(self):
        return "rssi {}".format(self.rssi)

    def __init__(self, rssi):
        self.rssi = rssi
