import numpy as np
from numpy.lib.function_base import i0


def fx(x, f: str):
    return eval(f)


def lincount(min, max, data, lindiv_count: np.ndarray):
    if not isinstance(data, np.ndarray) or data.shape == ():
        if data < min or data > max:
            print("data out of range.")
            exit()
        elif data == max:
            lindiv_count[len(lindiv_count) -
                         1] = lindiv_count[len(lindiv_count)-1]+1
        else:
            seq = int(lindiv_count.size*(data-min)/(max-min))
            lindiv_count[seq] = lindiv_count[seq]+1
    else:
        for i in data:
            if i < min or i > max:
                print("data out of range.")
                exit()
            elif i == max:
                lindiv_count[len(lindiv_count) -
                             1] = lindiv_count[len(lindiv_count)-1]+1
            else:
                seq = int(len(lindiv_count)*(i-min)/(max-min))
                lindiv_count[seq] = lindiv_count[seq]+1
    return lindiv_count


def fxcount(min, max, data, f, div_count: np.ndarray):
    return lincount(fx(min, f), fx(max, f), fx(data, f), div_count)


def pdf(div_count: np.ndarray) -> np.ndarray:
    sum = 0
    for i in div_count:
        sum += i
    pdfRes = np.zeros(div_count.shape)
    for i in range(0, len(pdfRes), 1):
        pdfRes[i] = div_count[i] / sum
    return pdfRes


def cdf(div_count: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    cumulate_sum = np.zeros(div_count.shape)
    cdfRes = np.zeros(div_count.shape)
    sum = 0
    for i in div_count:
        sum += i

    cumulate_sum[0] = div_count[0]
    cdfRes[0] = cumulate_sum[0] / sum
    for i in range(1, len(cdfRes), 1):
        cumulate_sum[i] = cumulate_sum[i-1] + div_count[i]
        cdfRes[i] = cumulate_sum[i]/sum

    return cumulate_sum, cdfRes


def linDivCenter(min, max, n) -> np.ndarray:
    res = np.linspace(min, max, n, endpoint=False)
    res = res + (max - min) / n/2
    return res


def fDivCenter(min, max, f, n) -> np.ndarray:
    res = linDivCenter(fx(min, f), fx(max, f), n)
    return res
