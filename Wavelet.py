import math


class wave:
    def __init__(self):
        M_SQRT1_2 = math.sqrt(0.5)
        self.h1 = [M_SQRT1_2, M_SQRT1_2]
        self.g1 = [M_SQRT1_2, -M_SQRT1_2]
        self.h2 = [M_SQRT1_2, M_SQRT1_2]
        self.g2 = [M_SQRT1_2, -M_SQRT1_2]
        self.nc = 2
        self.offset = 0

    def __del__(self):
        return


class Wavelet:
    def __init__(self, n):
        self._haar_centered_Init()
        self._scratch = []
        for i in range(0, n):
            self._scratch.append(0.0)
        return

    def __del__(self):
        return

    def transform_inverse(self, list, stride):
        self._wavelet_transform(list, stride, -1)
        return

    def transform_forward(self, list, stride):
        self._wavelet_transform(list, stride, 1)
        return

    def _haarInit(self):
        self._wave = wave()
        self._wave.offset = 0
        return

    def _haar_centered_Init(self):
        self._wave = wave()
        self._wave.offset = 1
        return

    def _wavelet_transform(self, list, stride, dir):
        n = len(list)
        if (len(self._scratch) < n):
            print("not enough workspace provided")
            exit()
        if (not self._ispower2(n)):
            print("the list size is not a power of 2")
            exit()

        if (n < 2):
            return

        if (dir == 1):  # 正变换
            i = n
            while (i >= 2):
                self._step(list, stride, i, dir)
                i = i >> 1

        if (dir == -1):  # 逆变换
            i = 2
            while (i <= n):
                self._step(list, stride, i, dir)
                i = i << 1
        return

    def _ispower2(self, n):
        power = math.log(n, 2)
        intpow = int(power)
        intn = math.pow(2, intpow)
        if (abs(n - intn) > 1e-6):
            return False
        else:
            return True

    def _step(self, list, stride, n, dir):
        for i in range(0, len(self._scratch)):
            self._scratch[i] = 0.0

        nmod = self._wave.nc * n
        nmod -= self._wave.offset
        n1 = n - 1
        nh = n >> 1

        if (dir == 1):  # 正变换
            ii = 0
            i = 0
            while (i < n):
                h = 0
                g = 0
                ni = i + nmod
                for k in range(0, self._wave.nc):
                    jf = n1 & (ni + k)
                    h += self._wave.h1[k] * list[stride * jf]
                    g += self._wave.g1[k] * list[stride * jf]
                self._scratch[ii] += h
                self._scratch[ii + nh] += g
                i += 2
                ii += 1

        if (dir == -1):  # 逆变换
            ii = 0
            i = 0
            while (i < n):
                ai = list[stride * ii]
                ai1 = list[stride * (ii + nh)]
                ni = i + nmod
                for k in range(0, self._wave.nc):
                    jf = n1 & (ni + k)
                    self._scratch[jf] += self._wave.h2[k] * ai + self._wave.g2[k] * ai1
                i += 2
                ii += 1

        for i in range(0, n):
            list[stride * i] = self._scratch[i]
