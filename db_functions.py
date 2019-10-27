from models import Point, Channel, Security, Ssid, Measure, Bssid

def save_measure_in_db(session, data, point):
    objects = []
    value = data.pop(0)
    
    my_ssid = Ssid(value[0])
    my_bssid = Bssid(value[1])
    my_measure = Measure(value[2])
    my_channel = Channel(value[3])
    my_security = Security(value[4])
    my_point = Point(point)
    
    entry = session.query(Ssid).filter(Ssid.ssid.like(value[0])).first()
    if entry is None:
        my_ssid.measure.append(my_measure)
        objects.append(my_ssid)
    else:
        entry.measure.append(my_measure)

    entry = session.query(Bssid).filter(Bssid.bssid.like(value[1])).first()
    if entry is None:
        my_bssid.measure.append(my_measure)
        objects.append(my_bssid)
    else:
        entry.measure.append(my_measure)

    entry = session.query(Channel).filter(Channel.channel.like(value[3])).first()
    if entry is None:
        my_channel.measure.append(my_measure)
        objects.append(my_channel)
    else:
        entry.measure.append(my_measure)

    entry = session.query(Security).filter(Security.security_type.like(value[4])).first()
    if entry is None:
        my_security.measure.append(my_measure)
        objects.append(my_security)
    else:
        entry.measure.append(my_measure)
    
    entry = session.query(Point).filter(Point.x_location==point.x).filter(Point.y_location==point.y).first()
    if entry is None:
        my_point.measure.append(my_measure)
        objects.append(my_point)
    else:
        entry.measure.append(my_measure)

    objects.append(my_measure)

    session.add_all(objects)
    session.commit()
    if len(data) != 0:
        save_measure_in_db(session, data, point)
    else:
        return
