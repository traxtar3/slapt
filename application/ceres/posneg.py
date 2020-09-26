from .sites import BLE, CAV, CLR, COD, EGL, FYL, THL

# from pyorbital.orbital import Orbital, get_observer_look
from .orbital import Orbital, get_observer_look
from datetime import datetime, timedelta, date
import time
from numpy import fabs
import pandas as pd
import numpy as np
import re
from .passes import get_site_passes
from .getTLE import getTLE
from .getpie import getPIE


timeFormat = '%j %H:%M:%S'


def checkTLE(SCC, TLEfile):  # gets new TLE file if more than 7 days old
    pie = getPIE(SCC, TLEfile)
    if np.datetime64('now') - pie[4] > timedelta(days=1):
        print(SCC, "TLE is over a week old, getting new TLEs")  # User warning
        import sys
        sys.path.append('/Users/traxtar3/Dropbox/Coding/Python/Projects/getTLEfile')
        from pw import username, password
        from tleRetrive import useapi
        import os
        useapi((username, password), TLE)  # Updates TLE File

    if pie[0] > 225:  # check to see if period is too large, SGP4 is hard coded to hate 255+ min period
        print("Period too large")  # will need to set up later for sdt.out for web
        # exit()


def PosNegPassToTable(ESVs, places, CALC_HRS, TLEfile, fileout=None):  # multiple ESVs for one site
    appended_data = []
    esvlist1 = []
    esvlist2 = []
    # piedata = pd.DataFrame(columns=['SCC', 'Period', 'Inclination', 'Elset'])
    piedata = pd.DataFrame(columns=['SCC', 'Period', 'Inclination'])
    for i in ESVs:
        try:
            esvlist1.append(getTLE(i, TLEfile)[2])
        except Exception:
            pass
    for w in esvlist1:
        # if int(w) > 10000 and getPIE(w, TLEfile)[0] < 225:
        if getPIE(w, TLEfile)[0] < 225:
            esvlist2.append(w)

        else:
            print(w, "has a period < 225, skipping")
    for esv in esvlist2:
        # checkTLE(esv, TLEfile)
        for i in places:

            print(esv, i, CALC_HRS, TLEfile)
            run = get_site_passes(esv, i, CALC_HRS, TLEfile)
            appended_data.append(run)
        pie = getPIE(esv, TLEfile)
        # piedata = piedata.append({'SCC': str(esv), 'Period': round(pie[0], 2), 'Inclination': round(pie[1], 2), 'Elset': str(pie[2])}, ignore_index=True)
        piedata = piedata.append({'SCC': str(esv), 'Period': round(pie[0], 2), 'Inclination': round(pie[1], 2)}, ignore_index=True)
    final_data = pd.concat(appended_data)
    final_data = final_data.round({'EnterAz': 3})
    final_data = final_data.sort_values(by=['PassStart'])
    # final_data = final_data[['SCC', 'Site', 'PassStart', 'EnterAz', 'Length']]
    final_data = final_data[['Site', 'SCC', 'PassStart', 'Az', 'El', 'MaxEl', 'Length']]
    final_data = final_data[final_data.El > 0]
    final_data = final_data.round(2)
    # final_data = final_data[final_data.El == 3]
    final_data = final_data.replace({'El': {3.00: 'CheckPass'}})
    # final_data.replace({'El': {99999: "CheckPass"}})
    # df.replace({'A': {0: 100, 4: 400}})

    final_data.reset_index(drop=True, inplace=True)
    final_data.to_csv(fileout, index=False)
    final_data.drop_duplicates(keep=False, inplace=True)

    return final_data, piedata


if __name__ == '__main__':
    places = (BLE, CAV, CLR, COD, EGL, THL, FYL)
    CALC_HRS = 24
    TLE = 'tle.txt'
    esvs = [25544, 45589, 44861, 43931]
    esvs = [25544, 42915, 10000]

    # print(get_site_passes(25544, COD, 48, 'tle.txt'))  # Duration in hours from current time,  # filename = file with TLEs in it
    # print(combined(esvs, places, CALC_HRS, TLE))
    places = [BLE, COD]
    try:
        df = PosNegPassToTable(esvs, places, CALC_HRS, TLE)
        print(df)
    except ValueError:
        df = ["Object Not Found", ""]
        print(df)

    # try:
    #     x = PosNegPassToTable(esvs, places, CALC_HRS, TLE)
    #     # print(x[0].SCC.unique())
    #     print(x)
    # except ValueError:
    #     # pd.DataFrame("Result Not Found")
    #     x = ["Object Not Found"]
    # print(x)
    # print(passToTables(SCC, places, CALC_HRS, TLE))
