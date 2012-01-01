import numpy

KK = numpy.pi / 180


class SurveyList(object):
    def __init__(self):
        pass


class Survey(object):
    """
    Each row in the CSV is considered a 'Survey' object.
    The `depth`, `Inc`, `Azi` are given and the `TVD`, `EW`, `NS`, and `DogLeg` are computed values.

    `TVD`, `EW`, `NS`, and `DogLeg` are computed from the previous `Survey` object and the current
    `depth`, `Inc`, and `Azi`

    """

    def __init__(self, depth, inc, azi, tvd=None, ew=None, ns=None, dogleg=None):
        self.depth = depth
        self.inc = inc
        self.azi = azi

        self.tvd = tvd
        self.ew = ew
        self.ns = ns
        self.dogleg = dogleg
        self.m_dlinterval = 100

    def __repr__(self):
        return "<Survey Point(%s, %s, %s,%s, %s, %s, %s)>" % (
            self.depth, self.inc, self.azi, self.tvd, self.ew, self.ns, self.dogleg)

    def next(self, d, i, a):
        s = Survey(d, i, a)
        dogleg = self.next_dogleg(i, a)
        s.dogleg = (self.m_dlinterval * dogleg) / (d - self.depth)
        m_rf = self.srv_rf(i, a, d)
        s.tvd = self.tvd + self.next_tvd(m_rf, i)
        s.ew = self.ew + self.next_ew(m_rf, i, a)
        s.ns = self.ns + self.next_ns(m_rf, i, a)

        return s

    def next_tvd(self, mrf, i):
        """
        Given an inclination, calculate the next `TVD`
        """
        return mrf * (numpy.cos(self.inc * KK) + numpy.cos(i * KK))

    def next_ns(self, mrf, i, a):
        """
        Given an inclination and an azimeth caculate the next `NS`
        """
        return mrf * (numpy.sin(self.inc * KK) * numpy.cos(self.azi * KK) + numpy.sin(i * KK) * numpy.cos(a * KK))

    def next_ew(self, mrf, i, a):
        """
        given an inclination and an azimeth calculate the next `EW`
        """
        return mrf * (numpy.sin(self.inc * KK) * numpy.sin(self.azi * KK) + numpy.sin(i * KK) * numpy.sin(a * KK))

    def next_dogleg(self, i, a):
        """
        return Math.Acos(
            Math.Cos((I2 - I1) * kk) -
            Math.Sin(I1 * kk) *
            Math.Sin(I2 * kk) *
            (1 - Math.Cos((A2 - A1)*kk))
        )/kk;
        """
        return numpy.arccos(numpy.cos((i - self.inc) * KK) - numpy.sin(self.inc * KK) * numpy.sin(i * KK) * (1 - numpy.cos((a - self.azi) * KK))) / KK

    def srv_rf(self, i, a, d):
        """
        I don't know what this value is
        """
        cl = d - self.depth
        dl = self.next_dogleg(i, a)
        x = dl * (numpy.pi / 360)
        if x == 0:
            rf = 1
        else:
            rf = numpy.tan(x) / x

        return rf * cl / 2

    def m_rf(self, i, a, d):
        return self.srv_rf(self.inc, i, self.azi, a, self.depth, d)

