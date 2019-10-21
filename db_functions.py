from models import Point, Channel, Security, Ssid, Measure, Bssid

def create_measure(session, data):
    measure = data.pop(0)
    objects = [Ssid(measure[0]), Bssid(measure[1]), Measure(measure[2]), Channel(measure[3]), Security(measure[4])]
    session.add_all(objects)
    session.commit()
    if len(data) != 0:
        create_measure(session, data)
    else:
        return