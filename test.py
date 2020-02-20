import math
import Wavelet

waveletn = 256
waveletnc = 20  # 保留的分量数
wavelettest = Wavelet.Wavelet(waveletn)
waveletorigindata = []
waveletdata = []
for i in range(0, waveletn):
    waveletorigindata.append(math.sin(i) * math.exp(-math.pow((i - 100) / 50, 2)) + 1)
    waveletdata.append(waveletorigindata[-1])

Wavelet.wavelettest.transform_forward(waveletdata, 1)
newdata = sorted(waveletdata, key=lambda ele: abs(ele), reverse=True)
for i in range(waveletnc, waveletn):  # 筛选出前 waveletnc个分量保留
    for j in range(0, waveletn):
        if (abs(newdata[i] - waveletdata[j]) < 1e-6):
            waveletdata[j] = 0.0
            break

Wavelet.wavelettest.transform_inverse(waveletdata, 1)
waveleterr = 0.0
for i in range(0, waveletn):
    print(waveletorigindata[i], ",", waveletdata[i])
    waveleterr += abs(waveletorigindata[i] - waveletdata[i]) / abs(waveletorigindata[i])
print("error: ", waveleterr / waveletn)
