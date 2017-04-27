import datetime

def RfgStrptime(ts_string):
    ts = None
    try:
        ts = datetime.datetime.strptime(ts_string, "%d-%m-%Y %H:%M")
    except ValueError:
        pass
    return ts
