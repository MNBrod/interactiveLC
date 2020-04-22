import lightkurve as lk
class LC:
    def __init__(self):
        self.data = None
        self.time = None
        self.name = None
        self.lc = None
        self.min_t = .5
        self.max_t = 3
        self.freq = 1000
    
    def set_time(self, times):
        self.time = times

    def set_data(self, d):
        self.data = d

    def set_name(self, n):
        self.name = n

    def init_lc(self):
        self.lc = lk.LightCurve(time=self.time, flux=self.data)
    
    def get_periodogram(self):
        return self.lc.to_periodogram(method='bls', minimum_period=self.min_t, maximum_period=self.max_t, frequency_factor=self.freq)

