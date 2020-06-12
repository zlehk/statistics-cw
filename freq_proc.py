import os
from CourseProject.raw import get_raw_data
from CourseProject.processing import process_freqs
from CourseProject.signal_info import SIGNAL_NUMBERS
import argparse
from argparse import SUPPRESS
from pylatex import Document, Section, Subsection, Package, Command, Figure, SubFigure
from pylatex.utils import NoEscape

WORK_DIR = os.path.dirname(os.path.abspath(__file__))


def handle_input_path(input_path, filenames):
    """Returns the list of absolute paths of SHT files"""
    sht_files = []

    if not os.path.exists(input_path):
        return None, None

    if os.path.isfile(input_path):
        if os.path.splitext(input_path)[1].lower() == '.sht':
            sht_files.append(input_path)
    else:
        if filenames is None:
            directory = os.listdir(input_path)
            sht_files = [os.path.join(input_path, f) for f in directory if os.path.splitext(f)[1].lower() == '.sht']
        else:
            modified_names = [name + '.sht' for name in filenames if os.path.splitext(name)[1].lower() == '']
            files = [os.path.join(input_path, f) for f in modified_names if os.path.splitext(f)[1].lower() == '.sht']
            sht_files = [f for f in files if os.path.exists(f)]

    sht_names = [os.path.splitext(os.path.basename(sf))[0] for sf in sht_files]
    return sht_files, sht_names


def handle_output_path(output_path):
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    return output_path


def handle_signal_numbers(signals):
    signal_numbers = []
    for s in signals:
        if s in SIGNAL_NUMBERS:
            signal_numbers.append(s)
        else:
            print('Exclude signal number: {}'.format(s))
    return signal_numbers


def gen_latex(sht_names, output_path, mode):
    doc = Document('Report')
    doc.documentclass = Command(
        'documentclass',
        options=['12pt'],
        arguments=['article'],
    )
    with doc.create(Section('Результаты')):
        for sht_name in sht_names:
            with doc.create(Subsection(sht_name)):
                if mode == 'raw':
                    with doc.create(Figure(position='h!')) as raw_pic:
                        raw_pic.add_image(os.path.join(output_path, 'raw_' + sht_name + '.png'), width='250px')
                        raw_pic.add_caption('Сырые данные с показаний датчиков, ' + sht_name)
                elif mode == 'freqs':
                    with doc.create(Figure(position='h!')) as freqs_pic:
                        freqs_pic.add_image(os.path.join(output_path, sht_name + '.png'), width='250px')
                        freqs_pic.add_caption('Частотный портрет для отобранных сигналов, ' + sht_name)
                else:
                    with doc.create(Figure(position='h!')) as pic:
                        with doc.create(SubFigure(position='b',
                                                  width=NoEscape(r'0.45\linewidth'))) as small_raw_pic:
                            small_raw_pic.add_image(os.path.join(output_path, 'raw_' + sht_name + '.png'),
                                                    width=NoEscape(r'\linewidth'))
                        with doc.create(SubFigure(position='b',
                                                  width=NoEscape(r'0.45\linewidth'))) as small_freqs__pic:
                            small_freqs__pic.add_image(os.path.join(output_path, sht_name + '.png'),
                                                       width=NoEscape(r'\linewidth'))
                    pic.add_caption(
                        'Сырые данные с показаний датчиков (cлева), ' +
                        'Частотный портрет для отобранных сигналов (справа), ' + sht_name)

    doc.packages.append(Package('babel',
                                options=['russian']))
    doc.packages.append(
        Package('geometry', options=['left=40mm, top=35mm, right=35mm, bottom=35mm, nohead, footskip=10mm']))

    doc.generate_pdf(filepath=os.path.join(output_path, 'Report'), clean_tex=False, compiler='pdflatex')
    doc.generate_tex(filepath=os.path.join(output_path, 'Report'))


def check_args():
    parser = argparse.ArgumentParser(description='SHT data processing', usage=SUPPRESS)

    parser.add_argument('--input', '-i', action='store', default=WORK_DIR + '\\SHT\\', type=str,
                        help='Directory with SHT files')
    parser.add_argument('--filenames', '-f', nargs='+', type=str,
                        help='Specify SHT files in INPUT directory')
    parser.add_argument('--output', '-o', action='store', default=WORK_DIR + '\\OUT\\', type=str,
                        help='Directory for results')

    parser.add_argument('--signals', '-s', nargs='+', default=[18, 19, 20, 26], type=int,
                        help='Available signals: 18, 19, 20, 26')
    parser.add_argument('--borders', '-b', nargs=2, type=int, default=None,
                        help='Borders for detection')

    parser.add_argument('--latex', choices=('raw', 'freqs', 'both'), default='both')

    args = parser.parse_args()
    return args.__dict__


def process():
    args = check_args()

    sht_files, sht_names = handle_input_path(args['input'], args['filenames'])
    if sht_files is None:
        print('ERROR: wrong SHT file path:\n' + args['input'])
        return
    if sht_files is []:
        print('WARNING: there are no SHT files:\n' + args['input'])

    output_path = handle_output_path(args['output'])

    signal_numbers = handle_signal_numbers(args['signals'])
    if signal_numbers is []:
        print('ERROR: signal numbers do not match possible:\n' + args['signals'])
        return

    get_raw_data(sht_files, signal_numbers, output_path)
    process_freqs(sht_files, signal_numbers, output_path, empirical_indexes=args['borders'])

    gen_latex(sht_names, output_path, args['latex'])


if __name__ == '__main__':
    process()
