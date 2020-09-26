import re
from .propagation import sgp4
from .inout import twoline2rv
from .earth_gravity import EarthGravity, wgs84
from math import pi, sqrt, floor, pow
from numpy import dot, linalg, arange, copy, char
from math import fabs as abs
from .inout import jday
from datetime import datetime
from operator import attrgetter
from .ext import invjday


def jsattime(dtTimeObj):
    attrs = ('year', 'month', 'day', 'hour', 'minute', 'second')
    d = dtTimeObj
    d_tuple = attrgetter(*attrs)(d)

    d_tuple = list(d_tuple)
    # print(d_tuple)
    x = jday(d_tuple[0], d_tuple[1], d_tuple[2], d_tuple[3], d_tuple[4], d_tuple[5])
    end = x * 86400
    return end


# start = datetime.now()
# currentJsec = jsattime(start)
# print (currentJsec)
# print("212456679584.23526")


def convertTLE(satno, filename):
    # sat_dic = {}
    # N = 1
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
    searchfile.close()
    if L1:
        # use Vallado's sgp4 code to input TLE and output r,v
        satout = sgp4(twoline2rv(L1, L2, wgs84), 0)
        # set up to convert to touple
        position = satout[0]
        velocity = satout[1]
        # convert jday at beginning of TLE to seconds
        jsec = (twoline2rv(L1, L2, wgs84)).jdsatepoch * 86400

        end = jsec, position[0], position[1], position[2], velocity[0], velocity[1], velocity[2]
        return end

    else:
        pass
        # print(satno, "TLE not found, skipping")


def twobody2(sat1, point):

    # stop = sat2

    ri = [sat1[1], sat1[2], sat1[3]]
    vi = [sat1[4], sat1[5], sat1[6]]

    tau = (point - sat1[0])
    # tau = -500

    mu = 398600.4415
    tolerance = 1e-12
    u = 0
    imax = 20
    orbits = 0
    tdesired = copy(tau)
    threshold = tolerance * abs(tdesired)
    r0 = linalg.norm(ri)
    n0 = dot(ri, vi)
    beta = 2 * (mu / r0) - dot(vi, vi)
    if (beta != 0):
        umax = + 1 / sqrt(abs(beta))
        umin = - 1 / sqrt(abs(beta))
    if (beta > 0):
        orbits = beta * tau - 2 * n0
        orbits = 1 + (orbits * sqrt(beta)) / (pi * mu)
        orbits = floor(orbits / 2)
    for i in arange(1, imax, 1).reshape(-1):
        q = beta * u * u
        q = q / (1 + q)
        n = 0
        r = 1
        l = 1
        s = 1
        d = 3
        gcf = 1
        k = - 5
        gold = 0

        while (gcf != gold):
            k = - k
            l = l + 2
            d = d + 4 * l
            n = n + (1 + k) * l
            r = d / (d - n * r * q)
            s = (r - 1) * s
            gold = copy(gcf)
            gcf = gold + s

        h0 = 1 - 2 * q
        h1 = 2 * u * (1 - q)
        u0 = 2 * h0 * h0 - 1
        u1 = 2 * h0 * h1
        u2 = 2 * h1 * h1
        u3 = 2 * h1 * u2 * gcf / 3

        if (orbits != 0):
            u3 = u3 + 2 * pi * orbits / (beta * sqrt(beta))

        r1 = r0 * u0 + n0 * u1 + mu * u2
        dt = r0 * u1 + n0 * u2 + mu * u3
        slope = 4 * r1 / (1 + beta * u * u)
        terror = tdesired - dt

        if (abs(terror) < threshold):
            break
        if ((i > 1) and (u == uold)):
            break
        if ((i > 1) and (dt == dtold)):
            break

        uold = copy(u)
        dtold = copy(dt)
        ustep = terror / slope

        if (ustep > 0):
            umin = copy(u)
            u = u + ustep
            if (u > umax):
                u = (umin + umax) / 2
        else:
            umax = copy(u)
            u = u + ustep
            if (u < umin):
                u = (umin + umax) / 2
        if (i == imax):
            print('\\n\\nmax iterations in twobody2 function')

    usaved = copy(u)
    f = 1.0 - (mu / r0) * u2
    gg = 1.0 - (mu / r1) * u2
    g = r0 * u1 + n0 * u2
    ff = - mu * u1 / (r0 * r1)

    # Had to re-arrange things to make it work
    for i in arange(1):  # .reshape(-1):
        posi = f * ri[i] + g * vi[i]
        veli = ff * ri[i] + gg * vi[i]
    for j in arange(2).reshape(-1):
        posj = f * ri[j] + g * vi[j]
        velj = ff * ri[j] + gg * vi[j]
    for k in arange(3).reshape(-1):
        posk = f * ri[k] + g * vi[k]
        velk = ff * ri[k] + gg * vi[k]

    # Make "pretty" output
    position = [posi, posj, posk]
    velocity = [veli, velj, velk]
    return position


def inverseDt(dtTimeObj):
    ref0 = invjday(dtTimeObj / 86400)
    ref0 = list(ref0)
    ref0[5] = int(ref0[5])
    ref0 = tuple(ref0)
    # convert ref0 to a datetime object
    ref2 = datetime(*ref0)
    return ref2


if __name__ == '__main__':
    TLE = 'tle.txt'
    esv = 25544
    # print(convertTLE(esv, TLE))
    point = jsattime(datetime.utcnow())
    print(twobody2(convertTLE(esv, TLE), point))
    # print(start)
