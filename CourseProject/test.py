import sys
import os
from matplotlib import pyplot

SHT_NUMBER = 38515
SIGNAL_NUMBER = 18
PATH_TO_SHT_FILE = "../SHT/sht" + str(SHT_NUMBER) + ".sht"

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(WORK_DIR)
PYGLOBUS_DIR = PARENT_DIR + '\\pyglobus\\python\\'

sys.path.append(PYGLOBUS_DIR)

try:
    import pyglobus
except ImportError as error:
    print('Unable to import pyglobus from ' + PYGLOBUS_DIR + ' exiting')
    sys.exit(-1)

# Read using pyglobus

sht_reader = pyglobus.util.ShtReader(PATH_TO_SHT_FILE)
signal_name = sht_reader.get_signal_name(SIGNAL_NUMBER)
signal = sht_reader.get_signals(signal_name)[0]

x, y = signal.get_data_x(), signal.get_data_y()

pyplot.figure()
pyplot.plot(x, y)
pyplot.xlim(0.15, 0.20)

pyplot.show()
