import io
import logging
import datetime
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen
import os
import glob
import numpy as np


def read(platform, tle_file=None, line1=None, line2=None):
    """Read TLE for `platform` from `tle_file`

    File is read from `line1` to `line2`, from the newest file provided in the
    TLES pattern, or from internet if none is provided.
    """
    return Tle(platform, tle_file=tle_file, line1=line1, line2=line2)


class Tle(object):
    """Class holding TLE objects."""

    def __init__(self, platform, tle_file=None, line1=None, line2=None):
        self._platform = platform.strip().upper()
        self._tle_file = tle_file
        self._line1 = line1
        self._line2 = line2

        self.satnumber = None
        self.classification = None
        self.id_launch_year = None
        self.id_launch_number = None
        self.id_launch_piece = None
        self.epoch_year = None
        self.epoch_day = None
        self.epoch = None
        self.mean_motion_derivative = None
        self.mean_motion_sec_derivative = None
        self.bstar = None
        self.ephemeris_type = None
        self.element_number = None
        self.inclination = None
        self.right_ascension = None
        self.excentricity = None
        self.arg_perigee = None
        self.mean_anomaly = None
        self.mean_motion = None
        self.orbit = None

        self._read_tle()
        self._checksum()
        self._parse_tle()

    @property
    def line1(self):
        """Return first TLE line."""
        return self._line1

    @property
    def line2(self):
        """Return second TLE line."""
        return self._line2

    @property
    def platform(self):
        """Return satellite platform name."""
        return self._platform

    def _checksum(self):
        """Performs the checksum for the current TLE."""
        for line in [self._line1, self._line2]:
            check = 0
            for char in line[:-1]:
                if char.isdigit():
                    check += int(char)
                if char == "-":
                    check += 1

            if (check % 10) != int(line[-1]):
                raise ChecksumError(self._platform + " " + line)

    def _read_tle(self):
        """Read TLE data."""
        if self._line1 is not None and self._line2 is not None:
            tle = self._line1.strip() + "\n" + self._line2.strip()
        else:
            def _open(filename):
                return io.open(filename, 'rb')

            if self._tle_file:
                urls = (self._tle_file,)
                open_func = _open
            elif "TLES" in os.environ:
                # TODO: get the TLE file closest in time to the actual satellite
                # overpass, NOT the latest!
                urls = (max(glob.glob(os.environ["TLES"]),
                            key=os.path.getctime), )
                LOGGER.debug("Reading TLE from %s", urls[0])
                open_func = _open
            else:
                LOGGER.debug("Fetch TLE from the internet.")
                urls = TLE_URLS
                open_func = urlopen

            tle = ""
            designator = "1 " + SATELLITES.get(self._platform, '')
            for url in urls:
                fid = open_func(url)
                for l_0 in fid:
                    l_0 = l_0.decode('utf-8')
                    if l_0.strip() == self._platform:
                        l_1 = next(fid).decode('utf-8')
                        l_2 = next(fid).decode('utf-8')
                        tle = l_1.strip() + "\n" + l_2.strip()
                        break
                    if(self._platform in SATELLITES and
                       l_0.strip().startswith(designator)):
                        l_1 = l_0
                        l_2 = next(fid).decode('utf-8')
                        tle = l_1.strip() + "\n" + l_2.strip()
                        LOGGER.debug("Found platform %s, ID: %s",
                                     self._platform,
                                     SATELLITES[self._platform])
                        break
                fid.close()
                if tle:
                    break

            if not tle:
                raise KeyError("Found no TLE entry for '%s'" % self._platform)

        self._line1, self._line2 = tle.split('\n')

    def _parse_tle(self):
        """Parse values from TLE data."""

        def _read_tle_decimal(rep):
            """Convert *rep* to decimal value."""
            if rep[0] in ["-", " ", "+"]:
                digits = rep[1:-2].strip()
                val = rep[0] + "." + digits + "e" + rep[-2:]
            else:
                digits = rep[:-2].strip()
                val = "." + digits + "e" + rep[-2:]

            return float(val)

        self.satnumber = self._line1[2:7]
        self.classification = self._line1[7]
        self.id_launch_year = self._line1[9:11]
        self.id_launch_number = self._line1[11:14]
        self.id_launch_piece = self._line1[14:17]
        self.epoch_year = self._line1[18:20]
        self.epoch_day = float(self._line1[20:32])
        self.epoch = \
            np.datetime64(datetime.datetime.strptime(self.epoch_year, "%y") +
                          datetime.timedelta(days=self.epoch_day - 1), 'us')
        self.mean_motion_derivative = float(self._line1[33:43])
        self.mean_motion_sec_derivative = _read_tle_decimal(self._line1[44:52])
        self.bstar = _read_tle_decimal(self._line1[53:61])
        try:
            self.ephemeris_type = int(self._line1[62])
        except ValueError:
            self.ephemeris_type = 0
        self.element_number = int(self._line1[64:68])

        self.inclination = float(self._line2[8:16])
        self.right_ascension = float(self._line2[17:25])
        self.excentricity = int(self._line2[26:33]) * 10 ** -7
        self.arg_perigee = float(self._line2[34:42])
        self.mean_anomaly = float(self._line2[43:51])
        self.mean_motion = float(self._line2[52:63])
        self.orbit = int(self._line2[63:68])

    def __str__(self):
        import pprint
        import sys
        if sys.version_info < (3, 0):
            from StringIO import StringIO
        else:
            from io import StringIO
        s_var = StringIO()
        d_var = dict(([(k, v) for k, v in
                       list(self.__dict__.items()) if k[0] != '_']))
        pprint.pprint(d_var, s_var)
        return s_var.getvalue()[:-1]
