'''
@author: Hung-hsuan
'''
import math
import numpy as np
import random


class Zipf():
    def get_zipf(self, num):
        self.num = num
        a = 0.8
        p = []
        sum = 0.0
        for i in range(1, self.num):
            for j in range(1, self.num):
                sum = sum+(math.pow(j, -a))
            fm = sum * (math.pow(i, a))
            sum = 0
            s = 1/fm
            p.append(s)
        return p

    def get_possion(self):
        self.vehicle_request_num = 0
        lam = int(random.randint(0, 3))
        self.vehicle_request_num = np.random.poisson(lam=lam, size=1)
        return self.vehicle_request_num
