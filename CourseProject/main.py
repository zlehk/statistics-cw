import os
import sys
import json
from numpy import char, array
from matplotlib import pyplot
from CourseProject.frequency_processing import calculate_frequency
from CourseProject.sawtooth_detection import get_sawtooth_indexes

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(WORK_DIR)
PYGLOBUS_DIR = PARENT_DIR + '\\pyglobus\\python\\'
SHT_DIR = PARENT_DIR + '\\SHT\\'
OUT_DIR = WORK_DIR + '\\out\\'

sys.path.append(PYGLOBUS_DIR)

try:
    import pyglobus
except ImportError as error:
    print('Unable to import pyglobus from ' + PYGLOBUS_DIR + ' exiting')
    sys.exit(-1)

MINIMUM_SAWTOOTH_LENGTH = 20000  # in steps


def get_borders(freqs):
    l_border_t = 0
    r_border_t = float('inf')
    for freq in freqs:
        if l_border_t < min(freq[0]):
            l_border_t = min(freq[0])
        if r_border_t > max(freq[0]):
            r_border_t = max(freq[0])
    assert (l_border_t < r_border_t)

    b_border_f = float('inf')
    u_border_f = 0
    for freq in freqs:
        a_ind = 0
        b_ind = len(freq[0])
        for i in range(0, len(freq[0])):
            if freq[0][i] >= l_border_t:
                a_ind = i
                break
        for i in range(len(freq[0]) - 1, 0, -1):
            if freq[0][i] <= r_border_t:
                b_ind = i
                break
        temp = array(freq[1])[a_ind:b_ind]
        if b_border_f > min(temp):
            b_border_f = min(temp)
        if u_border_f < max(temp):
            u_border_f = max(temp)
    assert (b_border_f < u_border_f)

    return l_border_t, r_border_t, b_border_f, u_border_f


def process_freqs():
    data_file = open('data.json')
    data = json.load(data_file)

    for sht_data in data['sht_data']:
        sht_number = sht_data[0]
        signal_numbers = sht_data[1]
        sht_file_name = 'sht' + str(sht_number) + '.SHT'
        sht_abs_path = SHT_DIR + sht_file_name
        freqs = []
        sawtooth_signals_numbers = []

        fig = pyplot.figure()
        for signal_number in signal_numbers:
            sht_reader = pyglobus.util.ShtReader(sht_abs_path)
            signal_name = sht_reader.get_signal_name(signal_number)
            signal = sht_reader.get_signals(signal_name)[0]
            sawtooth_indexes = get_sawtooth_indexes(signal)
            if sawtooth_indexes[1] - sawtooth_indexes[0] > MINIMUM_SAWTOOTH_LENGTH:
                sawtooth_signals_numbers.append(signal_number)
                freq = calculate_frequency(signal, sawtooth_indexes)
                freqs.append(freq)
                pyplot.plot(freq[0], freq[1], '-o', markersize=3)
            else:
                print('WARNING: unable to detect sawtooth sequence of minimum length for data:\n' +
                      sht_file_name + '\n'
                      'processing signal number: ' +
                      str(signal_number))

        l_border_t, r_border_t, b_border_f, u_border_f = get_borders(freqs)
        pyplot.xlim(l_border_t, r_border_t)
        pyplot.ylim(b_border_f - 50, u_border_f + 50)
        pyplot.legend(char.mod('%d', sawtooth_signals_numbers))
        pyplot.xlabel('Time, s')
        pyplot.ylabel('Frequency, Hz')
        pyplot.title('Frequency of ' + sht_file_name + ' data')
        if not os.path.exists(OUT_DIR):
            os.makedirs(OUT_DIR)
        fig.savefig(OUT_DIR + 'sht' + str(sht_number) + '.png')


if __name__ == '__main__':
    process_freqs()
