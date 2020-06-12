import os
import sys
from matplotlib import pyplot
from CourseProject.signal_info import SIGNAL_NAMES

SENSOR_NAMES = {18: 'signal = 18, SXR 15 ${\mu}m$',
                19: 'signal = 19, SXR 27 ${\mu}m$',
                20: 'signal = 20, SXR 50 ${\mu}m$',
                26: 'signal = 26, SXR 80 ${\mu}m$'}

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(WORK_DIR)
PYGLOBUS_DIR = PARENT_DIR + '\\pyglobus\\python\\'

sys.path.append(PYGLOBUS_DIR)

try:
    import pyglobus
except ImportError as error:
    print('Unable to import pyglobus from ' + PYGLOBUS_DIR + ' exiting')
    sys.exit(-1)


def get_raw_data(sht_files, signal_numbers, output_path):

    for sht_file in sht_files:
        sht_reader = pyglobus.util.ShtReader(sht_file)
        fig, ax = pyplot.subplots(nrows=2, ncols=2)

        for ind in range(0, len(signal_numbers)):
            signal_name = SIGNAL_NAMES[signal_numbers[ind]]
            signal = sht_reader.get_signals(signal_name)[0]

            x, y = signal.get_data_x(), signal.get_data_y()

            pyplot.subplot(2, 2, ind + 1)

            pyplot.plot(x, y, linewidth=0.4)
            # pyplot.xlim(0.13, 0.25)
            pyplot.xlabel('Time, s')
            pyplot.ylabel('V')
            pyplot.title(SENSOR_NAMES[signal_numbers[ind]])

        pyplot.tight_layout()
        fig.savefig(os.path.join(output_path, 'raw_' + os.path.splitext(os.path.basename(sht_file))[0] + '.png'))
