from .util import convertTLE, twobody2, jsattime, inverseDt
from datetime import datetime, timedelta
from math import sqrt, pow
import pandas as pd
from .inout import twoline2rv
from .earth_gravity import EarthGravity, wgs84


def getTime(satno, filename):
    ln1 = str("1 " + str(satno))  # Sets up search query for TLE finder
    while len(ln1) < 7:
        ln1 = re.sub(' ', '  ', ln1, 1)
    ln2 = str("2 " + str(satno))
    while len(ln2) < 7:
        ln2 = re.sub(' ', '  ', ln2, 1)
    # ln1 = re.sub(' +', ' ', ln1)
    L1, L2 = '', ''
    searchfile = open(filename, "r")  # Opens TLE file for TLE that matches satno
    # print(str(ln1))
    for line in searchfile:
        if ln1 in line:
            L1 = line

        if ln2 in line:
            L2 = line

    jsec = (twoline2rv(L1, L2, wgs84)).jdsatepoch * 86400
    end = inverseDt(jsec)
    # print(datetime.utcnow())
    # print(end)
    # print(datetime.utcnow() - end)
    return end


def getRSS(esv1, esv2, delta, increment, tol, filename):
    begin = jsattime(datetime.utcnow())
    end = jsattime(datetime.utcnow() + timedelta(hours=delta))
    point = begin
    rsslist = []
    # df = pd.DataFrame(rsslist)
    df = pd.DataFrame(columns=['Time', 'km'])
    while point < end:
        # print(point)
        sat1 = twobody2(convertTLE(esv1, filename), point)
        sat2 = twobody2(convertTLE(esv2, filename), point)

        rss = sqrt((pow((sat1[0] - sat2[0]), 2)) + (pow((sat1[1] - sat2[1]), 2)) + (pow((sat1[2] - sat2[2]), 2)))
        thing = inverseDt(point)
        rsslist.append(rss)
        # print(rss)
        df = df.append({'Time': thing, 'km': rss}, ignore_index=True)
        point = point + (increment)
        # print(sat1, sat2, thing, rss)

    # print(min(rsslist))
    # print(df)
    # print(min(df['km']))
    # print(df[df.RSS == df.km.min()])
    end = df[df.km == df.km.min()]

    s = df[df.km == df.km.min()]
    s = s.append(df[df.km < (df.km.min() + tol)])
    s.drop_duplicates(keep='first', inplace=True)

    return s


if __name__ == '__main__':

    filename = 'tle.txt'
    esv1 = 25544
    esv2 = 27880
    delta = 24
    increment = 1200
    tol = 200
    # print(getRSS(esv1, esv2, delta, increment, tol, filename))
    print(getTime(esv1, filename))
