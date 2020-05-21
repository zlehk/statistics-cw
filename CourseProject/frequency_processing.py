from scipy import signal
from numpy import where, diff, sign, convolve, ones

MOVING_AVERAGE_WINDOW_SIZE = 5


def moving_average(x, w):
    return convolve(a=x, v=ones(w), mode='valid') / w


def butter_filter(samples, cutoff, fs, btype, order=5):
    b, a = signal.butter(N=order, Wn=cutoff / (0.5 * fs), btype=btype, analog=False)
    return signal.filtfilt(b, a, samples)


def calculate_frequency(input_signal, roi):
    t = input_signal.get_data_x()[roi[0]:roi[1]]
    y = input_signal.get_data_y()[roi[0]:roi[1]]

    samples_rate = 1.0 / (t[1] - t[0])

    y = butter_filter(y, cutoff=250, fs=samples_rate, btype='high')
    y = butter_filter(y, cutoff=2000, fs=samples_rate, btype='low')

    zero_crossings = where(diff(sign(y)))[0]
    freq = []
    for i in range(len(zero_crossings) - 2):
        freq.append(1 / (t[zero_crossings[i + 2]] - t[zero_crossings[i]]))

    t = t[zero_crossings][:-(MOVING_AVERAGE_WINDOW_SIZE + 1)]
    y = moving_average(freq, MOVING_AVERAGE_WINDOW_SIZE)

    return t, y
