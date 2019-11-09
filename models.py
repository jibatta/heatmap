from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Draw_Point(Base):
    __tablename__ = 'draw'
    id = Column(Integer, primary_key = True)
    x_location = Column(Integer)
    y_location = Column(Integer)
    
    def __repr__(self):
        return self.x_location, self.y_location

    def __init__(self, point):
        self.x_location = point.x
        self.y_location = point.y

class Point(Base):
    __tablename__ = 'point'
    id = Column(Integer, primary_key = True)
    x_location = Column(Integer)
    y_location = Column(Integer)
    measure = relationship('Measure')

    def __repr__(self):
        return "{} - {}".format(self.x_location,self.y_location)

    def __init__(self, point):
        self.x_location = point.x
        self.y_location = point.y


class Ssid(Base):
    __tablename__ = 'ssid'
    id = Column(Integer, primary_key = True)
    ssid_value = Column(String)
    measure = relationship('Measure')

    def __repr__(self):
        return "{}".format(self.ssid_value)

    def __init__(self, ssid):
        self.ssid_value = ssid


class Channel(Base):
    __tablename__ = 'channel'
    id = Column(Integer, primary_key = True)
    channel_number = Column(String)
    measure = relationship('Measure')

    def __repr__(self):
        return "{}".format(self.channel_number)

    def __init__(self, channel):
        self.channel_number = channel


class Bssid(Base):
    __tablename__ = 'bssid'
    id = Column(Integer, primary_key = True)
    bssid_value = Column(String)
    measure = relationship('Measure')

    def __repr__(self):
        return "{}".format(self.bssid_value)

    def __init__(self, bssid):
        self.bssid_value = bssid


class Security(Base):
    __tablename__ = 'security'
    id = Column(Integer, primary_key = True)
    security_type = Column(String)
    measure = relationship('Measure')

    def __repr__(self):
        return "{}".format(self.security_type)
    
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
        return "{}".format(self.rssi)

    def __init__(self, rssi):
        self.rssi = rssi
