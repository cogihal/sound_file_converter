# 
# Since pydub will remove ID3 tags, call ffmpeg directly
# 

import argparse
import os
import subprocess
import sys
import textwrap
import wave
from argparse import ArgumentParser
from argparse import _SubParsersAction as SubParsersAction  # type: ignore

import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment

from remove_chunk import remove_chunk


def color_red():
    print('\033[31m')
    pass


def color_normal():
    print('\033[0m')
    pass


class CustomHelpFormatter(argparse.RawTextHelpFormatter):
    def __init__(self, prog, indent_increment=2, max_help_position=8, width=None):
        super().__init__(prog, indent_increment, max_help_position, width)


def sub_command_parser_conv(subparsers: SubParsersAction, parent_parser_0: ArgumentParser, parent_parser_2: ArgumentParser):
    """
    sub command parser : conv
    """
    description = """
        File format conversion, mp3 to wav, or wav to mp3.
        The source file and the destination file must be different format.
    """
    help = """
        The 'conv' sub-command will convert file format, from mp3 to wav, or from wav to mp3.
        The source file and the destination file must be different format.
    """
    parser_convert = subparsers.add_parser('conv',
        formatter_class=CustomHelpFormatter,
        add_help=False,
        parents=[parent_parser_0, parent_parser_2],
        description=textwrap.dedent(description).strip(),
        help=textwrap.dedent(help).strip(),
    )


def sub_command_parser_vol(subparsers: SubParsersAction, parent_parser_0: ArgumentParser, parent_parser_2: ArgumentParser):
    """
    sub command parser : vol
    """
    description = """
        Volume level up / down by dB
        The source file and the destination file must be same format.
    """
    help = """
        The 'vol' sub-command will change volume level by dB.
        The source file and the destination file must be same format.
    """
    parser_volume = subparsers.add_parser('vol',
        formatter_class=CustomHelpFormatter,
        add_help=False,
        parents=[parent_parser_0, parent_parser_2],
        description=textwrap.dedent(description).strip(),
        help=textwrap.dedent(help).strip(),
    )

    help = """
        Change volume level by dB.
        Positive value will increase volume level, and negative value will decrease volume level.
    """
    parser_volume.add_argument('--dB', '--db', type=float, metavar='dB', required=True, help=textwrap.dedent(help).strip())


def sub_command_parser_channel(subparsers: SubParsersAction, parent_parser_0: ArgumentParser, parent_parser_2: ArgumentParser):
    """
    sub command parser : channel
    """
    description = """
        Change channel, stereo to monaural or monaural to stereo.
        The source file and the destination file must be same format.
    """
    help = """
        The 'channel' sub-command will change channel, stereo to monaural or monaural to stereo.
        The source file and the destination file must be same format.
    """
    parser_channel = subparsers.add_parser('channel',
        formatter_class=CustomHelpFormatter,
        add_help=False,
        parents=[parent_parser_0, parent_parser_2],
        description=textwrap.dedent(description).strip(),
        help=textwrap.dedent(help).strip(),
    )

    help = """
        Change channel.
        The value 1 means monaural, and the value 2 means stereo.
    """
    parser_channel.add_argument('--ch', type=int, metavar='channel', choices=[1,2], required=True, help=textwrap.dedent(help).strip())


def sub_command_parser_chunk(subparsers: SubParsersAction, parent_parser_0: ArgumentParser, parent_parser_2: ArgumentParser):
    """
    sub command parser : chunk
    """
    description = """
        Remove unnecessary chunk(s) from the wav file.
        The source file and the destination file must be wav format.
    """
    help = """
        The 'chunk' sub-command will remove unnecessary chunk(s) from the wav file.
        The source file and the destination file must be wav format.
    """
    parser_chunk = subparsers.add_parser('chunk',
        formatter_class=CustomHelpFormatter,
        add_help=False,
        parents=[parent_parser_0, parent_parser_2],
        description=textwrap.dedent(description).strip(),
        help=textwrap.dedent(help).strip(),
    )


def sub_command_parser_len(subparsers: SubParsersAction, parent_parser_0: ArgumentParser, parent_parser_1: ArgumentParser):
    """
    sub command parser : len
    """
    description = """
        Get time length of sound file.
    """
    help = """
        The 'len' sub-command will get time length of sound file.
    """
    parser_len = subparsers.add_parser('len',
        formatter_class=CustomHelpFormatter,
        add_help=False,
        parents=[parent_parser_0, parent_parser_1],
        description=textwrap.dedent(description).strip(),
        help=textwrap.dedent(help).strip(),
    )


def sub_command_parser_clip(subparsers: SubParsersAction, parent_parser_0: ArgumentParser, parent_parser_2: ArgumentParser):
    """
    sub command parser : clip
    """
    description = """
        Clipping sound file.
        Need to specify the start time and the end time.
        The source file and the destination file must be same format.
    """
    help = """
        The 'clip' sub-command will clip a part of sound file and save to another.
        Need to specify the start time and the end time.
        The source file and the destination file must be same format.
    """
    parser_clip = subparsers.add_parser('clip',
        formatter_class=CustomHelpFormatter,
        add_help=False,
        parents=[parent_parser_0, parent_parser_2],
        description=textwrap.dedent(description).strip(),
        help=textwrap.dedent(help).strip(),
    )

    help = """
        Start time for clipping by milli-seconds.
        If not specified, it means clipping from the beginning.
        Negative value means to specify the time from the end.
    """
    parser_clip.add_argument('--start', '-s', type=int, metavar='start(msec)', help=textwrap.dedent(help).strip())

    help = """
        End time for clipping by milli-seconds.
        If not specified, it means clipping to the end.
        Negative value means to specify the time from the end.
    """
    parser_clip.add_argument('--end', '-e', type=int, metavar='end(msec)', help=textwrap.dedent(help).strip())


def sub_command_parser_join(subparsers: SubParsersAction, parent_parser_0: ArgumentParser, parent_parser_3: ArgumentParser):
    """
    sub command parser : join
    """
    description = """
        Join 2 files into 1 file.
        The source file and the destination file must be wav format.
    """
    help = """
        The 'join' sub-command will join 2 files into 1 file.
        The 2nd file will be added to the end of the 1st file.
        The source file and the destination file must be wav format.
    """
    parser_join = subparsers.add_parser('join',
        formatter_class=CustomHelpFormatter,
        add_help=False,
        parents=[parent_parser_0, parent_parser_3],
        description=textwrap.dedent(description).strip(),
        help=textwrap.dedent(help).strip(),
    )


def sub_command_parser_samrate(subparsers: SubParsersAction, parent_parser_0: ArgumentParser, parent_parser_2: ArgumentParser):
    """
    sub command parser : samrate
    """
    description = """
        Change sampling rate.
        The source file and the destination file must be same format.
    """
    help = """
        The 'samrate' sub-command will change sampling rate.
        The source file and the destination file must be same format.
    """
    parser_samrate = subparsers.add_parser('samrate',
        formatter_class=CustomHelpFormatter,
        add_help=False,
        parents=[parent_parser_0, parent_parser_2],
        description=textwrap.dedent(description).strip(),
        help=textwrap.dedent(help).strip(),
    )

    help = """
        Change sampling rate by Hz.
        For example, 44100 means 44.1kHz, 48000 means 48kHz.
    """
    parser_samrate.add_argument('--samrate', '-sr', type=int, metavar='sampling rate', required=True, help=textwrap.dedent(help).strip())


def sub_command_parser_graph(subparsers: SubParsersAction, parent_parser_0: ArgumentParser, parent_parser_1: ArgumentParser):
    """
    sub command parser : graph
    """
    description = """
        Show waveform graph.
        The source file must be a wav format.
    """
    help = """
        The 'graph' sub-command will show the waveform graph.
        The source file must be a wav format.
    """
    parser_graph = subparsers.add_parser('graph',
        formatter_class=CustomHelpFormatter,
        add_help=False,
        parents=[parent_parser_0, parent_parser_1],
        description=textwrap.dedent(description).strip(),
        help=textwrap.dedent(help).strip(),
    )


def arguments_parser(argv=None):
    # 
    # parent parser 0 : for help message
    # 
    parent_parser_0 = argparse.ArgumentParser(add_help=False)
    parent_parser_0.add_argument('-h', '--help', action='help', help='Show this help message and exit.')

    # 
    # parent parser 1 : for 1 file (src)
    # 
    parent_parser_1 = argparse.ArgumentParser(add_help=False)
    help = """
        Specify the target file name to process.
    """
    parent_parser_1.add_argument('target_file', type=str, metavar='target-file', help=textwrap.dedent(help).strip())

    # 
    # parent parser 2 : for 2 files (src and dst)
    # 
    parent_parser_2 = argparse.ArgumentParser(add_help=False)
    help = """
        Overwrite destination file if the file exists.
    """
    parent_parser_2.add_argument('--overwrite', action='store_true', help=textwrap.dedent(help).strip())

    help = """
        Specify the source file name to process.
    """
    parent_parser_2.add_argument('source_file', type=str, metavar='source-file', help=textwrap.dedent(help).strip())

    help = """
        Specify the destination file name to save.
    """
    parent_parser_2.add_argument('destination_file', type=str, metavar='destination-file', help=textwrap.dedent(help).strip())

    # 
    # parent parser 3 : for 3 files (src1, src2, and dst)
    # 
    parent_parser_3 = argparse.ArgumentParser(add_help=False)
    help = """
        Overwrite destination file if the file exists.
    """
    parent_parser_3.add_argument('--overwrite', action='store_true', help=textwrap.dedent(help).strip())

    help = """
        Specify the source file name 1 to process.
    """
    parent_parser_3.add_argument('source_file_1', type=str, metavar='source-file-1', help=textwrap.dedent(help).strip())

    help = """
        Specify the source file name 2 to process.
    """
    parent_parser_3.add_argument('source_file_2', type=str, metavar='source-file-2', help=textwrap.dedent(help).strip())

    help = """
        Specify the destination file name to save.
    """
    parent_parser_3.add_argument('destination_file', type=str, metavar='destination-file', help=textwrap.dedent(help).strip())

    # 
    # main parser
    # 
    parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter, add_help=False)
    parser.add_argument('-h', '--help', action='help', help='Show this help message and exit.')

    # 
    # sub parser
    # 
    subparsers = parser.add_subparsers(dest='sub_command_name', help='There are available sub commands as follows :')

    sub_command_parser_conv(subparsers, parent_parser_0, parent_parser_2)
    sub_command_parser_vol(subparsers, parent_parser_0, parent_parser_2)
    sub_command_parser_channel(subparsers, parent_parser_0, parent_parser_2)
    sub_command_parser_chunk(subparsers, parent_parser_0, parent_parser_2)
    sub_command_parser_len(subparsers, parent_parser_0, parent_parser_1)
    sub_command_parser_clip(subparsers, parent_parser_0, parent_parser_2)
    sub_command_parser_join(subparsers, parent_parser_0, parent_parser_3)
    sub_command_parser_samrate(subparsers, parent_parser_0, parent_parser_2)
    sub_command_parser_graph(subparsers, parent_parser_0, parent_parser_1)

    args = parser.parse_args(argv)

    return args


def format_converter(source_file, destination_file, overwrite=False):
    # File exists check
    if not os.path.exists(source_file):
        color_red()
        print('Error: Source file does not exist.', file=sys.stderr)
        color_normal()
        return
    if os.path.exists(destination_file) and not overwrite:
        color_red()
        print('Error: Destination file already exists.', file=sys.stderr)
        color_normal()
        return

    # File format check
    _, src_ext = os.path.splitext(source_file)
    _, dst_ext = os.path.splitext(destination_file)
    if src_ext == dst_ext:
        color_red()
        print('Error: Source file and destination file are the same format.', file=sys.stderr)
        color_normal()
        return
    elif not src_ext == '.mp3' and not src_ext == '.wav':
        color_red()
        print('Error: Invalid source file format.', file=sys.stderr)
        color_normal()
        return
    elif not dst_ext == '.wav' and not dst_ext == '.mp3':
        color_red()
        print('Error: Invalid destination file format.', file=sys.stderr)
        color_normal()
        return

    # File format conversion
    # AudioSegment.from_file(source_file).export(destination_file, format=dst_ext[1:])
    if src_ext == '.mp3' and dst_ext == '.wav':
        command = f'ffmpeg -vn -y -loglevel fatal -i {source_file} -acodec pcm_s16le {destination_file}'
    elif src_ext == '.wav' and dst_ext == '.mp3':
        command = f'ffmpeg -vn -y -loglevel fatal -i {source_file} {destination_file}'
    else:
        return
    subprocess.run(command, shell=True)


def volume_changer(source_file, destination_file, dB, overwrite=False):
    # File exists check
    if not os.path.exists(source_file):
        color_red()
        print('Error: Source file does not exist.', file=sys.stderr)
        color_normal()
        return
    if os.path.exists(destination_file) and not overwrite:
        color_red()
        print('Error: Destination file already exists.', file=sys.stderr)
        color_normal()
        return

    # File format check
    _, src_ext = os.path.splitext(source_file)
    _, dst_ext = os.path.splitext(destination_file)
    if not src_ext == '.mp3' and not src_ext == '.wav':
        color_red()
        print('Error: Invalid source file format.', file=sys.stderr)
        color_normal()
        return
    elif not dst_ext == '.wav' and not dst_ext == '.mp3':
        color_red()
        print('Error: Invalid destination file format.', file=sys.stderr)
        color_normal()
        return

    if src_ext != dst_ext:
        color_red()
        print('Error: Source file and destination file are different format.', file=sys.stderr)
        color_normal()
        return

    # Volume level change
    # sound = AudioSegment.from_file(source_file)
    # sound += dB
    # sound.export(destination_file, format=dst_ext[1:])
    if src_ext == '.mp3' and dst_ext == '.mp3':
        command = f'ffmpeg -vn -y -loglevel fatal -i {source_file} -af volume={dB}dB {destination_file}'
    elif src_ext == '.wav' and dst_ext == '.wav':
        command = f'ffmpeg -vn -y -loglevel fatal -i {source_file} -af volume={dB}dB {destination_file}'
    else:
        return
    subprocess.run(command, shell=True)


def channel_changer(source_file, destination_file, ch, overwrite=False):
    # File exists check
    if not os.path.exists(source_file):
        color_red()
        print('Error: Source file does not exist.', file=sys.stderr)
        color_normal()
        return
    if os.path.exists(destination_file) and not overwrite:
        color_red()
        print('Error: Destination file already exists.', file=sys.stderr)
        color_normal()
        return

    # File format check
    _, src_ext = os.path.splitext(source_file)
    _, dst_ext = os.path.splitext(destination_file)
    if not src_ext == '.mp3' and not src_ext == '.wav':
        color_red()
        print('Error: Invalid source file format.', file=sys.stderr)
        color_normal()
        return
    elif not dst_ext == '.wav' and not dst_ext == '.mp3':
        color_red()
        print('Error: Invalid destination file format.', file=sys.stderr)
        color_normal()
        return

    if src_ext != dst_ext:
        color_red()
        print('Error: Source file and destination file are different format.', file=sys.stderr)
        color_normal()
        return

    # Channel change
    sound = AudioSegment.from_file(source_file)
    c = sound.channels

    if ch == 1:
        if c == 1:
            color_red()
            print('Error: Source file is already monaural.', file=sys.stderr)
            color_normal()
            return
        # sound = sound.set_channels(1)
    elif ch == 2:
        if c == 2:
            color_red()
            print('Error: Source file is already stereo.', file=sys.stderr)
            color_normal()
            return
        # sound = sound.set_channels(2)

    # sound.export(destination_file, format=dst_ext[1:])
    if src_ext == '.mp3' and dst_ext == '.mp3':
        command = f'ffmpeg -vn -y -loglevel fatal -i {source_file} -ac {ch} {destination_file}'
    elif src_ext == '.wav' and dst_ext == '.wav':
        command = f'ffmpeg -vn -y -loglevel fatal -i {source_file} -ac {ch} {destination_file}'
    else:
        return
    subprocess.run(command, shell=True)


def chunk_remover(source_file, destination_file, overwrite=False):
    # File exists check
    if not os.path.exists(source_file):
        color_red()
        print('Error: Source file does not exist.', file=sys.stderr)
        color_normal()
        return
    if os.path.exists(destination_file) and not overwrite:
        color_red()
        print('Error: Destination file already exists.', file=sys.stderr)
        color_normal()
        return

    # File format check
    _, src_ext = os.path.splitext(source_file)
    _, dst_ext = os.path.splitext(destination_file)
    if not src_ext == '.wav':
        color_red()
        print('Error: Invalid source file format.', file=sys.stderr)
        color_normal()
        return
    elif not dst_ext == '.wav':
        color_red()
        print('Error: Invalid destination file format.', file=sys.stderr)
        color_normal()
        return

    # Chunk remove
    # remove_chunk(source_file, destination_file)
    # easier way
    import wave
    with wave.open(source_file, 'rb') as s, wave.open(destination_file, 'wb') as d:
        d.setparams(s.getparams())
        d.writeframes(s.readframes(s.getnframes()))


def length_getter(target_file):
    # File exists check
    if not os.path.exists(target_file):
        color_red()
        print('Error: Source file does not exist.', file=sys.stderr)
        color_normal()
        return

    # get length of source file
    sound = AudioSegment.from_file(target_file)
    length = len(sound)
    print(f'Time length of {target_file}: {length:,} msec')


def clipper(source_file, destination_file, start, end, overwrite=False):
    # File exists check
    if not os.path.exists(source_file):
        color_red()
        print('Error: Source file does not exist.', file=sys.stderr)
        color_normal()
        return

    if os.path.exists(destination_file) and not overwrite:
        color_red()
        print('Error: Destination file already exists.', file=sys.stderr)
        color_normal()
        return

    # File format check
    _, src_ext = os.path.splitext(source_file)
    _, dst_ext = os.path.splitext(destination_file)
    if not src_ext == '.mp3' and not src_ext == '.wav':
        color_red()
        print('Error: Invalid source file format.', file=sys.stderr)
        color_normal()
        return
    elif not dst_ext == '.wav' and not dst_ext == '.mp3':
        color_red()
        print('Error: Invalid destination file format.', file=sys.stderr)
        color_normal()
        return

    if src_ext != dst_ext:
        color_red()
        print('Error: Source file and destination file are different format.', file=sys.stderr)
        color_normal()
        return

    # get length of source file
    sound = AudioSegment.from_file(source_file)
    length = len(sound)

    # start time check
    if start is None:   start = 0
    if start < 0:       start = length + start
    # end time check
    if end is None:     end = length
    if end < 0:         end = length + end

    # time range check
    if start < 0 or start > length:
        color_red()
        print('Error: Start time is out of range.', file=sys.stderr)
        print(f'Length of {source_file}: {length} msec', file=sys.stderr)
        color_normal()
        return
    if end < 0 or end > length:
        color_red()
        print('Error: End time is out of range.', file=sys.stderr)
        print(f'Length of {source_file}: {length} msec', file=sys.stderr)
        color_normal()
        return
    if start >= end:
        color_red()
        print('Error: Start time is later than end time.', file=sys.stderr)
        print(f'Length of {source_file}: {length} msec', file=sys.stderr)
        color_normal()
        return
    if start == 0 and end == length:
        color_red()
        print('Error: Clip size is the same as original length.', file=sys.stderr)
        color_normal()
        return

    # Clip
    # sound = sound[start:end]
    # sound.export(destination_file, format=dst_ext[1:])
    start = start / 1000
    end = end / 1000
    if src_ext == '.mp3' and dst_ext == '.mp3':
        command = f'ffmpeg -vn -y -loglevel fatal -i {source_file} -ss {start} -to {end} {destination_file}'
    elif src_ext == '.wav' and dst_ext == '.wav':
        command = f'ffmpeg -vn -y -loglevel fatal -i {source_file} -ss {start} -to {end} {destination_file}'
    else:
        return
    subprocess.run(command, shell=True)


def joiner(source_file_1, source_file_2, destination_file, overwrite=False):
    # File exists check
    if not os.path.exists(source_file_1):
        color_red()
        print('Error: Source file 1 does not exist.', file=sys.stderr)
        color_normal()
        return
    if not os.path.exists(source_file_2):
        color_red()
        print('Error: Source file 2 does not exist.', file=sys.stderr)
        color_normal()
        return
    if os.path.exists(destination_file) and not overwrite:
        color_red()
        print('Error: Destination file already exists.', file=sys.stderr)
        color_normal()
        return

    # File format check
    _, src1_ext = os.path.splitext(source_file_1)
    _, src2_ext = os.path.splitext(source_file_2)
    _, dst_ext = os.path.splitext(destination_file)
    if not src1_ext == '.wav' and not src1_ext == '.mp3':
        color_red()
        print('Error: Invalid source file 1 format.', file=sys.stderr)
        color_normal()
        return
    elif not src2_ext == '.wav' and not src2_ext == '.mp3':
        color_red()
        print('Error: Invalid source file 2 format.', file=sys.stderr)
        color_normal()
        return
    elif not dst_ext == '.wav' and not dst_ext == '.mp3':
        color_red()
        print('Error: Invalid destination file format.', file=sys.stderr)
        color_normal()
        return

    if not (src1_ext == src2_ext and src1_ext == dst_ext and src2_ext == dst_ext):
        color_red()
        print('Error: Source file 1, source file 2, and destination file are not same format.', file=sys.stderr)
        color_normal()
        return

    # Join
    # sound1 = AudioSegment.from_file(source_file_1)
    # sound2 = AudioSegment.from_file(source_file_2)
    # sound = sound1 + sound2
    # sound.export(destination_file, format=dst_ext[1:])
    if src1_ext == '.mp3' and src2_ext == '.mp3' and dst_ext == '.mp3':
        command = f'ffmpeg -vn -y -loglevel fatal -i {source_file_1} -i {source_file_2} -filter_complex  concat=n=2:v=0:a=1 {destination_file}'
    elif src1_ext == '.wav' and src2_ext == '.wav' and dst_ext == '.wav':
        command = f'ffmpeg -vn -y -loglevel fatal -i {source_file_1} -i {source_file_2} -filter_complex  concat=n=2:v=0:a=1 {destination_file}'
    else:
        return
    subprocess.run(command, shell=True)


def samrate_changer(source_file, destination_file, samrate, overwrite=False):
    # File exists check
    if not os.path.exists(source_file):
        color_red()
        print('Error: Source file does not exist.', file=sys.stderr)
        color_normal()
        return
    if os.path.exists(destination_file) and not overwrite:
        color_red()
        print('Error: Destination file already exists.', file=sys.stderr)
        color_normal()
        return

    # File format check
    _, src_ext = os.path.splitext(source_file)
    _, dst_ext = os.path.splitext(destination_file)
    if not src_ext == '.mp3' and not src_ext == '.wav':
        color_red()
        print('Error: Invalid source file format.', file=sys.stderr)
        color_normal()
        return
    elif not dst_ext == '.wav' and not dst_ext == '.mp3':
        color_red()
        print('Error: Invalid destination file format.', file=sys.stderr)
        color_normal()
        return

    if src_ext != dst_ext:
        color_red()
        print('Error: Source file and destination file are different format.', file=sys.stderr)
        color_normal()
        return

    # Current sampling rate
    sound = AudioSegment.from_file(source_file)
    current_samrate = sound.frame_rate

    if current_samrate == samrate:
        color_red()
        print('Error: Source file is already the same sampling rate.', file=sys.stderr)
        color_normal()
        return

    # Sampling rate change
    # sound = sound.set_frame_rate(samrate)
    # sound.export(destination_file, format=dst_ext[1:])
    if src_ext == '.mp3' and dst_ext == '.mp3':
        command = f'ffmpeg -vn -y -loglevel fatal -i {source_file} -ar {samrate} {destination_file}'
    elif src_ext == '.wav' and dst_ext == '.wav':
        command = f'ffmpeg -vn -y -loglevel fatal -i {source_file} -ar {samrate} {destination_file}'
    else:
        return
    subprocess.run(command, shell=True)


def graph_drawer(target_file):
    # File exists check
    if not os.path.exists(target_file):
        color_red()
        print('Error: Source file does not exist.', file=sys.stderr)
        color_normal()
        return

    # File format check
    _, ext = os.path.splitext(target_file)
    if not ext == '.wav':
        color_red()
        print('Error: Invalid source file format.', file=sys.stderr)
        color_normal()
        return

    # Open and load data
    wf = wave.open(target_file, 'rb')
    buf = wf.readframes(wf.getnframes())

    # Transfer from binary data to 16bit integer numpy array
    data = np.frombuffer(buf, dtype='int16')

    samplerate = wf.getframerate()

    if wf.getnchannels() == 2:
        left  = data[::2]  # Left channel
        right = data[1::2] # Right channel

        t = np.arange(0, len(left))/samplerate

        fig = plt.figure(f'Waveform : {target_file}')

        # Left channel
        axL = fig.add_subplot(2, 1, 1)
        axL.plot(t, left)
        axL.set_title('Left channel')
        axL.set_xlabel('Time(s)')
        axL.set_ylabel('Sound Amplitude')
        axL.grid()

        # Right channel
        axR = fig.add_subplot(2, 1, 2)
        axR.plot(t, right)
        axR.set_title('Right channel')
        axR.set_xlabel('Time(s)')
        axR.set_ylabel('Sound Amplitude')
        axR.grid()

        plt.tight_layout()
        plt.show()

    else:
        t = np.arange(0, len(data))/samplerate

        fig = plt.figure(f'Waveform : {target_file}')
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(t, data)
        ax.set_title('Waveform')
        ax.set_xlabel('Time(s)')
        ax.set_ylabel('Sound Amplitude')
        ax.grid()

        plt.tight_layout()
        plt.show()


def main():
    argv = ['-h']

    if len(sys.argv) > 1:
        argv = sys.argv[1:]
    args = arguments_parser(argv)
    pass

    if args.sub_command_name == 'conv':
        format_converter(args.source_file, args.destination_file, args.overwrite)
        pass
    elif args.sub_command_name == 'vol':
        volume_changer(args.source_file, args.destination_file, args.dB, args.overwrite)
        pass
    elif args.sub_command_name == 'channel':
        channel_changer(args.source_file, args.destination_file, args.ch, args.overwrite)
        pass
    elif args.sub_command_name == 'chunk':
        chunk_remover(args.source_file, args.destination_file, args.overwrite)
        pass
    elif args.sub_command_name == 'len':
        length_getter(args.target_file)
        pass
    elif args.sub_command_name == 'clip':
        clipper(args.source_file, args.destination_file, args.start, args.end, args.overwrite)
        pass
    elif args.sub_command_name == 'join':
        joiner(args.source_file_1, args.source_file_2, args.destination_file, args.overwrite)
        pass
    elif args.sub_command_name == 'samrate':
        samrate_changer(args.source_file, args.destination_file, args.samrate, args.overwrite)
        pass
    elif args.sub_command_name == 'graph':
        graph_drawer(args.target_file)
        pass
    pass


if __name__ == '__main__':
    main()


