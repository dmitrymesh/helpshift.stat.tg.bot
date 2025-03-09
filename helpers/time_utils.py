import datetime

def time_to_str(timestamp):
    return str(int(timestamp))[:10] + "000"

def unixtime_to_date(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
