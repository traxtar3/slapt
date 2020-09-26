import numpy as np
from .getTLE import getTLE
import datetime


def _read_tle_decimal(rep):
    """Convert *rep* to decimal value."""
    if rep[0] in ["-", " ", "+"]:
        digits = rep[1:-2].strip()
        val = rep[0] + "." + digits + "e" + rep[-2:]
    else:
        digits = rep[:-2].strip()
        val = "." + digits + "e" + rep[-2:]

    return float(val)


def getPIE(satno, filename):
    Line1 = getTLE(satno, filename)[0]
    Line2 = getTLE(satno, filename)[1]

    CK2 = 5.413080e-4
    XKE = 0.743669161e-1
    XMNPDA = 1440.0

    # def __init__(self, tle):
    satnumber = Line1[2:7]
    excentricity = int(Line2[26:33]) * 10 ** -7
    mean_motion = float(Line2[52:63]) * (np.pi * 2 / XMNPDA)
    mean_motion_derivative = float(Line1[33:43]) * \
        np.pi * 2 / XMNPDA ** 2
    mean_motion_sec_derivative = _read_tle_decimal(Line1[44:52]) * \
        np.pi * 2 / XMNPDA ** 3
    n_0 = mean_motion
    k_e = XKE
    k_2 = CK2
    i_0 = np.deg2rad((float(Line2[8:16])))
    e_0 = excentricity

    a_1 = (k_e / n_0) ** (2.0 / 3)
    delta_1 = ((3 / 2.0) * (k_2 / a_1**2) * ((3 * np.cos(i_0)**2 - 1) /
                                             (1 - e_0**2)**(2.0 / 3)))

    a_0 = a_1 * (1 - delta_1 / 3 - delta_1**2 - (134.0 / 81) * delta_1**3)

    delta_0 = ((3 / 2.0) * (k_2 / a_0**2) * ((3 * np.cos(i_0)**2 - 1) /
                                             (1 - e_0**2)**(2.0 / 3)))

    # original mean motion
    n_0pp = n_0 / (1 + delta_0)
    original_mean_motion = n_0pp

    # semi major axis
    a_0pp = a_0 / (1 - delta_0)
    # semi_major_axis = a_0pp

    period = np.pi * 2 / n_0pp
    inclination = (float(Line2[8:16]))
    elset = int(Line2[63:68])
    epoch_year = str(Line1[18:20])
    epoch_day = float(Line1[20:32])
    epoch = np.datetime64(datetime.datetime.strptime(epoch_year, "%y") +
                          datetime.timedelta(days=epoch_day - 1), 'us')
    # epoch = Line1[18:32]
    return period, inclination, elset, a_0pp, epoch


if __name__ == '__main__':
    SCC = 25544
    Period = getPIE(SCC, 'tle.txt')[0]
    Inclination = getPIE(SCC, 'tle.txt')[1]
    Elset = getPIE(SCC, 'tle.txt')[2]
    SemiMA = getPIE(SCC, 'tle.txt')[3]
    Epoch = getPIE(SCC, 'tle.txt')[4]
    print(getPIE(SCC, 'tle.txt'))
    print(Period, Inclination, Elset, SemiMA, Epoch)
