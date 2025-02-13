import os
import wave
from dataclasses import dataclass


class WavError(Exception):
    pass


@dataclass
class RIFFHeader:           # 12 bytes
    FourCC: str             # 4 bytes strings
    data_size: int          # 4 byte integer
    data_type: str          # 4 bytes strings

@dataclass
class ChunkHeader:          # 8 bytes
    chunk_id: str           # 4 bytes strings
    chunk_size: int         # 4 byte integer

@dataclass
class FmtChunk:             # 16 bytes
    audio_fmt_type: int     # 2 byte integer
    channels: int           # 2 byte integer
    sampling_rate: int      # 4 byte integer
    ave_bytes_per_sec: int  # 4 byte integer
    block_align: int        # 2 byte integer
    bits_per_sample: int    # 2 byte integer

@dataclass
class InfoTag:              # 4 bytes
    info_tag: str           # 4 bytes strings

@dataclass
class SubChunk:
    sub_chunk_data: str     # variable length


def read_data(f, size):
    databuf = f.read(size)
    datalen = len(databuf)
    if datalen != size:
        return None
    return databuf


def analize_riff_header(databuf):
    header = RIFFHeader(*wave.struct.unpack('<4sI4s', databuf))

    if header.FourCC != b'RIFF':
        raise WavError('FourCC error')

    if header.data_type != b'WAVE':
        raise WavError('WAVE error')

    return header

def analize_fmt_chunk(databuf):
    fmt = FmtChunk(*wave.struct.unpack('<HHIIHH', databuf))

    if fmt.audio_fmt_type != 1:
        raise WavError('LPCM error')
    
    return fmt


def remove_chunk(src_file, dst_file):
    riff_header = None
    fmt_header = None
    fmt_chunk = None
    data_chunk = None
    datalen = 0

    with open(src_file, 'rb') as src:

        if (databuf := read_data(src, 12)) is None:
            raise WavError('read error')

        riff_header = analize_riff_header(databuf)

        while databuf := src.read(8):
            if len(databuf) != 8:
                raise WavError('read error')

            chunk = ChunkHeader(*wave.struct.unpack('<4sI', databuf))

            if chunk.chunk_id == b'fmt ':
                if chunk.chunk_size > 16:
                    raise WavError('read error')

                fmt_header = chunk
                if (databuf := read_data(src, 16)) is None:
                    raise WavError('read error')

                fmt_chunk = analize_fmt_chunk(databuf)

            elif chunk.chunk_id == b'data':
                data_chunk = chunk
                databuf = src.read(chunk.chunk_size)
                datalen = len(databuf)
                break

            elif chunk.chunk_id == b'LIST':
                if (databuf := read_data(src, 4)) is None:
                    raise WavError('read error')
                info_tag = InfoTag(*wave.struct.unpack('<4s', databuf))

            else:
                unpack_format = f'<{chunk.chunk_size}s'

                if chunk.chunk_id == b'fact':
                    raise WavError('fact chunk error')

                # skip unknown chunk
                src.seek(chunk.chunk_size, os.SEEK_CUR)

                # skip padding byte
                if chunk.chunk_size % 2 == 1:
                    src.seek(1, os.SEEK_CUR)

    with open(dst_file, 'wb') as dst:
        riff_header.data_size = 12 + 8 + 16 + 8 + datalen - 8
        dst.write(wave.struct.pack(
            '<4sI4s',
            riff_header.FourCC,
            riff_header.data_size,
            riff_header.data_type
        ))
        dst.write(wave.struct.pack(
            '<4sI',
            fmt_header.chunk_id,
            fmt_header.chunk_size
        ))
        dst.write(wave.struct.pack(
            '<HHIIHH',
            fmt_chunk.audio_fmt_type,
            fmt_chunk.channels,
            fmt_chunk.sampling_rate,
            fmt_chunk.ave_bytes_per_sec,
            fmt_chunk.block_align,
            fmt_chunk.bits_per_sample
        ))
        dst.write(wave.struct.pack(
            '<4sI',
            data_chunk.chunk_id,
            data_chunk.chunk_size
        ))
        dst.write(databuf)

    pass


