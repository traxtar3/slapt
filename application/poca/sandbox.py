from util import convertTLE, twobody2, jsattime, inverseDt
from datetime import datetime, timedelta
from math import sqrt, pow
import pandas as pd


def getRSS(esv1, esv2, delta, increment, tol, filename):
    begin = jsattime(datetime.utcnow())
    end = jsattime(datetime.utcnow() + timedelta(hours=delta))
    point = begin
    rsslist = []
    # df = pd.DataFrame(rsslist)
    df = pd.DataFrame(columns=['RTime', 'RSS'])
    while point < end:
        # print(point)
        sat1 = twobody2(convertTLE(esv1, filename), point)
        sat2 = twobody2(convertTLE(esv2, filename), point)

        rss = sqrt((pow((sat1[0] - sat2[0]), 2)) + (pow((sat1[1] - sat2[1]), 2)) + (pow((sat1[2] - sat2[2]), 2)))
        thing = inverseDt(point)
        rsslist.append(rss)
        # print(rss)
        df = df.append({'RTime': thing, 'RSS': rss}, ignore_index=True)
        point = point + (increment)

    # print(min(rsslist))
    # print(df)
    # print(min(df['RSS']))
    # print(df[df.RSS == df.RSS.min()])
    end = df[df.RSS == df.RSS.min()]

    s = df[df.RSS == df.RSS.min()]
    s = s.append(df[df.RSS < (df.RSS.min() + tol)])

    return s


if __name__ == '__main__':

    filename = 'tle.txt'
    esv1 = 25544
    esv2 = 27880
    delta = 24
    increment = 1200
    tol = 200
    print(getRSS(esv1, esv2, delta, increment, tol, filename))
