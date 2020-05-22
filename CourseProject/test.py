import sys
import os
from matplotlib import pyplot

SHT_NUMBER = 38515
SIGNAL_NUMBERS = [18, 19, 20, 26]
SENSOR_NAMES = ['SXR 15 $\mu$m', 'SXR 27 $\mu$m', 'SXR 50 $\mu$m', 'SXR 80 $\mu$m']
PATH_TO_SHT_FILE = "../SHT/sht" + str(SHT_NUMBER) + ".sht"

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

sht_reader = pyglobus.util.ShtReader(PATH_TO_SHT_FILE)
fig, ax = pyplot.subplots(nrows=2, ncols=2)
for ind in range(0, len(SIGNAL_NUMBERS)):
    signal_name = sht_reader.get_signal_name(SIGNAL_NUMBERS[ind])
    signal = sht_reader.get_signals(signal_name)[0]

    x, y = signal.get_data_x(), signal.get_data_y()

    pyplot.subplot(2, 2, ind + 1)

    pyplot.plot(x, y)
    pyplot.xlim(0.15, 0.20)
    pyplot.xlabel('Time, s')
    pyplot.ylabel('V')
    pyplot.title(SENSOR_NAMES[ind])

pyplot.tight_layout()
if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)
fig.savefig(OUT_DIR + 'sht' + str(SHT_NUMBER) + '.png')
