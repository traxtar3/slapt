from .orbital import Orbital, get_observer_look
from datetime import datetime, timedelta, date
import time
from numpy import fabs
import pandas as pd
import numpy as np
import re
from .getTLE import getTLE


timeFormat = '%j %H:%M:%S'


def get_site_passes(satno, site, duration, filename):  # Duration in hours from current time,  # filename = file with TLEs in it
    now = datetime.utcnow()  # set time to current time
    sat = Orbital(satellite='None', line1=getTLE(satno, filename)[0], line2=getTLE(satno, filename)[1])
    x = Orbital.get_next_passes(sat, now, duration, site[1], site[0], site[2], tol=0.001, horizon=site[3])  # builds list of all passes that break 3 degrees
    # passes = []  # begins empty list for passes
    s = pd.DataFrame(columns=['Site', 'PassStart', 'Az', 'El', 'MaxEl', 'Length', 'SCC'])  # initial dataframe build

    for i in x:
        # print(i[0].strftime('%d-%b  %H:%M:%S'))
        # print("\n", satno)
        en = Orbital.get_observer_look(sat, i[0], site[1], site[0], site[2])  # Gets entry Az & El at 3 degree entry
        # print(en[1])
        ex = Orbital.get_observer_look(sat, i[1], site[1], site[0], site[2])  # Gets exitAz & El at 3 degree exit
        hi = Orbital.get_observer_look(sat, i[2], site[1], site[0], site[2])  # Gets exitAz & El for entire pases *even outside fences*
        p1 = Orbital.get_observer_look(sat, i[0], site[1], site[0], site[2])[0]  # az at 3 degree entry
        p2 = Orbital.get_observer_look(sat, i[0] + timedelta(seconds=1), site[1], site[0], site[2])[0]  # p1 1 seconds later
        p3 = Orbital.get_observer_look(sat, i[1], site[1], site[0], site[2])[0]  # az at 3 degree exit
        # print(site[8], "Pass Start:", i[0], "Enter Az", en[0], "Pass Term:", i[1], "Exit Az:", ex[0], "MaxEl:", hi[1])  # prints passes (used for dev)

        if site[4] < en[0] < site[5] or site[6] < en[0] < site[7]:  # if satellite enters FOV on face *checkpass*

            len = int((i[1] - i[0]).total_seconds())  # length of pass in seconds
            # passes.append(i[0])  # appedns check passes to passes list
            # s = s.append({'Site': site[8], 'PassStart': i[0], 'EnterAz': en[0], 'Length': len, 'SCC': satno}, ignore_index=True)  # adds pass to dataframe
            # print("CheckPass")

            s = s.append({'Site': site[8], 'PassStart': i[0].strftime(timeFormat), 'Az': en[0], 'El': en[1], 'MaxEl': hi[1], 'Length': len, 'SCC': satno}, ignore_index=True)  # adds pass to dataframe

        elif not site[4] < en[0] < site[5]:  # if enters FOV not on face1
            # print("Fence Pass | Az:", en[0])  # prints pass info (used for dev)
            if (p1 - p2) < 0:  # if the azimuth is growing after 5 seconds
                rx = i[0]  # req'd  since i[0] can't be added to later
                q1 = p1
                while q1 <= site[6]:  # looks for when azimuth breaches sides of coverage
                    q1 = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[0]  # gets new azimuth after rx added seconds
                    rx = rx + timedelta(seconds=10)  # sets time for 10s later to retrieve azimuth at that time
                elv = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[1]
                pe = elv
                px = rx
                topel = []
                while pe > site[3]:
                    pe = Orbital.get_observer_look(sat, px, site[1], site[0], site[2])[1]
                    topel.append(pe)
                    px = px + timedelta(seconds=10)
                    # pe = Orbital.get_observer_look(sat, px, site[1], site[0], site[2])[1]
                if topel:
                    # print(("topel:", max(topel)))
                    topel = max(topel)
                else:
                    topel = hi[1]
                # print("Fence Time:", rx, "Az:", q1, "El:", elv)
                len = int((i[1] - rx).total_seconds())
                # passes.append(i[0])  # length of pass in seconds
                s = s.append({'Site': site[8], 'PassStart': rx.strftime(timeFormat), 'Az': q1, 'El': elv, 'MaxEl': topel, 'Length': len, 'SCC': satno}, ignore_index=True)  # adds pass to dataframe

            if (p1 - p2) > 0:  # if the azimuth is shrinking after 5 seconds
                rx = i[0]  # req'd  since i[0] can't be added to later
                q1 = p1
                while q1 >= site[6]:  # looks for when azimuth breaches sides of coverage
                    q1 = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[0]  # gets new azimuth
                    rx = rx + timedelta(seconds=10)
                elv = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[1]
                pe = elv
                px = rx
                topel = []
                while pe > site[3]:
                    pe = Orbital.get_observer_look(sat, px, site[1], site[0], site[2])[1]
                    topel.append(pe)
                    px = px + timedelta(seconds=10)
                    # pe = Orbital.get_observer_look(sat, px, site[1], site[0], site[2])[1]
                if topel:
                    # print(("topel:", max(topel)))
                    topel = max(topel)
                else:
                    topel = hi[1]
                # print("Fence Time:", rx, "Az:", q1, "El:", elv)
                len = int((i[1] - rx).total_seconds())
                # passes.append(i[0])  # length of pass in seconds
                s = s.append({'Site': site[8], 'PassStart': rx.strftime(timeFormat), 'Az': q1, 'El': elv, 'MaxEl': topel, 'Length': len, 'SCC': satno}, ignore_index=True)  # adds pass to dataframe

        elif not site[6] < en[0] < site[7]:  # if enters FOV not on face2

            if (p1 - p2) < 0:  # if the azimuth is growing after 5 seconds
                rx = i[0]  # req'd  since i[0] can't be added to later
                q1 = p1
                while q1 <= site[6]:  # looks for when azimuth breaches sides of coverage
                    q1 = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[0]  # gets new azimuth
                    rx = rx + timedelta(seconds=10)  # sets time for 10s later to retrieve azimuth at that time
                elv = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[1]
                pe = elv
                px = rx
                topel = []
                while pe > site[3]:
                    pe = Orbital.get_observer_look(sat, px, site[1], site[0], site[2])[1]
                    topel.append(pe)
                    px = px + timedelta(seconds=10)
                    # pe = Orbital.get_observer_look(sat, px, site[1], site[0], site[2])[1]
                if topel:
                    # print(("topel:", max(topel)))
                    topel = max(topel)
                else:
                    topel = hi[1]
                # print("Fence Time:", rx, "Az:", q1, "El:", elv)
                len = int((i[1] - rx).total_seconds())
                # passes.append(i[0])  # length of pass in seconds
                s = s.append({'Site': site[8], 'PassStart': rx.strftime(timeFormat), 'Az': q1, 'El': elv, 'MaxEl': topel, 'Length': len, 'SCC': satno}, ignore_index=True)  # adds pass to dataframe

            if (p1 - p2) > 0:  # if the azimuth is shrinking after 5 seconds
                rx = i[0]  # req'd  since i[0] can't be added to later
                q1 = p1
                while q1 >= site[6]:  # looks for when azimuth breaches sides of coverage
                    q1 = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[0]  # gets new azimuth
                    rx = rx + timedelta(seconds=10)  # sets time for 10s later to retrieve azimuth at that time
                elv = Orbital.get_observer_look(sat, rx, site[1], site[0], site[2])[1]
                pe = elv
                px = rx
                topel = []
                while pe > site[3]:
                    pe = Orbital.get_observer_look(sat, px, site[1], site[0], site[2])[1]
                    topel.append(pe)
                    px = px + timedelta(seconds=10)
                    # pe = Orbital.get_observer_look(sat, px, site[1], site[0], site[2])[1]
                if topel:
                    # print(("topel:", max(topel)))
                    topel = max(topel)
                else:
                    topel = hi[1]
                # print("Fence Time:", rx, "Az:", q1, "El:", elv)
                len = int((i[1] - rx).total_seconds())
                # passes.append(i[0])  # length of pass in seconds
                s = s.append({'Site': site[8], 'PassStart': rx.strftime(timeFormat), 'Az': q1, 'El': elv, 'MaxEl': topel, 'Length': len, 'SCC': satno}, ignore_index=True)  # adds pass to dataframe
        if len < 0:
            # print("Not a Pass")
            pass
        elif len < 180:
            # print("Pass Length: ", len, "sec (short)")
            pass
        # else:
        #     print("Pass Length: ", len, "sec")

    s = s.drop(s[s.Length < 0].index)
    print(s)

    final = pd.DataFrame()
    # final = final.append(s.loc[(s.El == site[3])])
    final = final.append(s.loc[(s.Az > (site[4] - 3)) & (s.Az < (site[5] + 3))])
    final = final.append(s.loc[(s.Az > (site[6] - 3)) & (s.Az < (site[7] + 3))])
    final.sort_values(by=['PassStart'])
    # print(final)

    final = final.drop(s[s.Length < 0].index)
    # print("Done")
    return final


if __name__ == '__main__':
    from orbital import Orbital, get_observer_look
    from sites import BLE, CAV, CLR, COD, EGL, FYL, THL
    # print(get_site_passes(25544, CAV, 48, 'tle.txt'))  # Duration in hours from current time,  # filename = file with TLEs in it
    print(get_site_passes(25544, BLE, 48, 'tle.txt'))  # Duration in hours from current time,  # filename = file with TLEs in it
