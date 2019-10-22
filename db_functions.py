from models import Point, Channel, Security, Ssid, Measure, Bssid

def create_measure(session, data):
    objects = []
    value = data.pop(0)
    # Somehow I should send foreign keys to measure
    objects.append(Measure(value[2]))
    entry = session.query(Ssid).filter(Ssid.ssid.like(value[0])).first()
    if entry is None:
        objects.append(Ssid(value[0]))
    entry = session.query(Bssid).filter(Bssid.bssid.like(value[1])).first()
    if entry is None:
        objects.append(Bssid(value[1]))
    entry = session.query(Channel).filter(Channel.channel.like(value[3])).first()
    if entry is None:
        objects.append(Channel(value[3]))
    entry = session.query(Security).filter(Security.security_type.like(value[4])).first()
    if entry is None:
        objects.append(Security(value[4]))
    session.add_all(objects)
    session.commit()
    if len(data) != 0:
        create_measure(session, data)
    else:
        return

def create_point(session, point):
    entry = session.query(Point).filter(Point.x_location.like(point.x)).filter(Point.y_location.like(point.y)).first()
    if entry is None:
        session.add(Point(point))
        session.commit()
    else:
        return