import numpy
import os
import sys

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(WORK_DIR)
PYGLOBUS_DIR = PARENT_DIR + '\\pyglobus\\python\\'

sys.path.append(PYGLOBUS_DIR)

try:
    import pyglobus
except ImportError as error:
    print('Unable to import pyglobus from ' + PYGLOBUS_DIR + ' exiting')
    sys.exit(-1)

SIGNAL_SAMPLING_RATE = int(1e6)
HIGH_PASS_CUTOFF = 400
SMOOTHED_DD1_ORDER = 30
LOW_PASS_CUTOFF = 5000
SAWTOOTH_DETECTION_THRESHOLD = 0.0005
ROI_DETECTOR_MEAN_SCALE = 1


def get_sawtooth_indexes(signal):
    data = numpy.array((signal.get_data_x(), signal.get_data_y()))

    roi = pyglobus.sawtooth.get_signal_roi(data[1], mean_scale=ROI_DETECTOR_MEAN_SCALE)
    y = numpy.copy(data[1, roi[0]:roi[1]])

    pyglobus.dsp.high_pass_filter(y, HIGH_PASS_CUTOFF, SIGNAL_SAMPLING_RATE)

    y = pyglobus.dsp.first_order_diff_filter(y, SMOOTHED_DD1_ORDER)
    y = numpy.abs(y)

    pyglobus.dsp.low_pass_filter(y, LOW_PASS_CUTOFF, SIGNAL_SAMPLING_RATE)

    start_ind, end_ind = pyglobus.sawtooth.get_sawtooth_indexes(y, SAWTOOTH_DETECTION_THRESHOLD)
    return start_ind + roi[0], end_ind + roi[0]
