import os
import sys
import json
from matplotlib import pyplot

SIGNAL_NUMBERS = [18, 19, 20, 26]
SENSOR_NAMES = ['signal = 18, SXR 15 $\mu$m',
                'signal = 19, SXR 27 $\mu$m',
                'signal = 20, SXR 50 $\mu$m',
                'signal = 26, SXR 80 $\mu$m']

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(WORK_DIR)
PYGLOBUS_DIR = PARENT_DIR + '\\pyglobus\\python\\'
OUT_DIR = WORK_DIR + '\\raw\\'

sys.path.append(PYGLOBUS_DIR)

try:
    import pyglobus
except ImportError as error:
    print('Unable to import pyglobus from ' + PYGLOBUS_DIR + ' exiting')
    sys.exit(-1)

# Read using pyglobus
data_file = open('data.json')
data = json.load(data_file)
for sht_data in data['sht_data']:
    sht_number = sht_data[0]
    path_to_sht_file = "../SHT/sht" + str(sht_number) + ".sht"

    if not os.path.isfile(path_to_sht_file):
        print('WARNING: unable process file\n' +
              path_to_sht_file)
        continue

    sht_reader = pyglobus.util.ShtReader(path_to_sht_file)
    fig, ax = pyplot.subplots(nrows=2, ncols=2)
    for ind in range(0, len(SIGNAL_NUMBERS)):
        signal_name = sht_reader.get_signal_name(SIGNAL_NUMBERS[ind])
        signal = sht_reader.get_signals(signal_name)[0]

        x, y = signal.get_data_x(), signal.get_data_y()

        pyplot.subplot(2, 2, ind + 1)

        pyplot.plot(x, y)
        pyplot.xlim(0.10, 0.25)
        pyplot.xlabel('Time, s')
        pyplot.ylabel('V')
        pyplot.title(SENSOR_NAMES[ind])

    pyplot.tight_layout()
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)
    fig.savefig(OUT_DIR + 'sht' + str(sht_number) + '.png')
