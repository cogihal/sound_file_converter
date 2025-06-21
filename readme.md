# MP3 & Wave file converter sample scripts

This is a sample script that will convert MP3 files or Wav files with mainly ffmpeg.


## Usage

```
python sound_file_converter.py [-h] {conv,vol,channel,chunk,len,clip,join,samrate,graph} ...

positional arguments:
  {conv,vol,channel,chunk,len,clip,join,samrate,graph}
        There are available sub commands as follows :
    conv
        The 'conv' sub-command will convert file format, from mp3 to wav, or from wav to mp3.
        The source file and the destination file must be different format.
    vol
        The 'vol' sub-command will change volume level by dB.
        The source file and the destination file must be same format.
    channel
        The 'channel' sub-command will change channel, stereo to monaural or monaural to stereo.
        The source file and the destination file must be same format.
    chunk
        The 'chunk' sub-command will remove unnecessary chunk(s) from the wav file.
        The source file and the destination file must be wav format.
    len
        The 'len' sub-command will get time length of sound file.
    clip
        The 'clip' sub-command will clip a part of sound file and save to another.
        Need to specify the start time and the end time.
        The source file and the destination file must be same format.
    join
        The 'join' sub-command will join 2 files into 1 file.
        The 2nd file will be added to the end of the 1st file.
        The source file and the destination file must be wav format.
    samrate
        The 'samrate' sub-command will change sampling rate.
        The source file and the destination file must be same format.
    graph
        The 'graph' sub-command will show the waveform graph.
        The source file must be a wav format.

options:
  -h, --help
        Show this help message and exit.
```


### 'conv' sub-command

```
python sound_file_converter.py conv [-h] [--overwrite] source-file destination-file

File format conversion, mp3 to wav, or wav to mp3.
The source file and the destination file must be different format.

positional arguments:
  source-file
        Specify the source file name to process.
  destination-file
        Specify the destination file name to save.

options:
  -h, --help
        Show this help message and exit.
  --overwrite
        Overwrite destination file if the file exists.
```

### 'vol' sub-command

```
python sound_file_converter.py vol [-h] [--overwrite] --dB dB source-file destination-file

Volume level up / down by dB
The source file and the destination file must be same format.

positional arguments:
  source-file
        Specify the source file name to process.
  destination-file
        Specify the destination file name to save.

options:
  -h, --help
        Show this help message and exit.
  --overwrite
        Overwrite destination file if the file exists.
  --dB dB, --db dB
        Change volume level by dB.
        Positive value will increase volume level, and negative value will decrease volume level.
```

### 'channel' sub-command

```
python sound_file_converter.py channel [-h] [--overwrite] --ch channel source-file destination-file

Change channel, stereo to monaural or monaural to stereo.
The source file and the destination file must be same format.

positional arguments:
  source-file
        Specify the source file name to process.
  destination-file
        Specify the destination file name to save.

options:
  -h, --help
        Show this help message and exit.
  --overwrite
        Overwrite destination file if the file exists.
  --ch channel
        Change channel.
        The value 1 means monaural, and the value 2 means stereo.
```

### 'chunk' sub-command

```
python sound_file_converter.py chunk [-h] [--overwrite] source-file destination-file

Remove unnecessary chunk(s) from the wav file.
The source file and the destination file must be wav format.

positional arguments:
  source-file
        Specify the source file name to process.
  destination-file
        Specify the destination file name to save.

options:
  -h, --help
        Show this help message and exit.
  --overwrite
        Overwrite destination file if the file exists.
```

### 'len' sub-command

```
python sound_file_converter.py len [-h] target-file

Get time length of sound file.

positional arguments:
  target-file
        Specify the target file name to process.

options:
  -h, --help
        Show this help message and exit.
```

### 'clip' sub-command

```
python sound_file_converter.py clip [-h] [--overwrite] [--start start(msec)] [--end end(msec)] source-file destination-file

Clipping sound file.
Need to specify the start time and the end time.
The source file and the destination file must be same format.

positional arguments:
  source-file
        Specify the source file name to process.
  destination-file
        Specify the destination file name to save.

options:
  -h, --help
        Show this help message and exit.
  --overwrite
        Overwrite destination file if the file exists.
  --start start(msec), -s start(msec)
        Start time for clipping by milli-seconds.
        If not specified, it means clipping from the beginning.
        Negative value means to specify the time from the end.
  --end end(msec), -e end(msec)
        End time for clipping by milli-seconds.
        If not specified, it means clipping to the end.
        Negative value means to specify the time from the end.
```

### 'join' sub-command

```
python sound_file_converter.py join [-h] [--overwrite] source-file-1 source-file-2 destination-file

Join 2 files into 1 file.
The source file and the destination file must be wav format.

positional arguments:
  source-file-1
        Specify the source file name 1 to process.
  source-file-2
        Specify the source file name 2 to process.
  destination-file
        Specify the destination file name to save.

options:
  -h, --help
        Show this help message and exit.
  --overwrite
        Overwrite destination file if the file exists.
```

### 'samrate' sub-command

```
python sound_file_converter.py samrate [-h] [--overwrite] --samrate sampling rate source-file destination-file

Change sampling rate.
The source file and the destination file must be same format.

positional arguments:
  source-file
        Specify the source file name to process.
  destination-file
        Specify the destination file name to save.

options:
  -h, --help
        Show this help message and exit.
  --overwrite
        Overwrite destination file if the file exists.
  --samrate sampling rate, -sr sampling rate
        Change sampling rate by Hz.
        For example, 44100 means 44.1kHz, 48000 means 48kHz.
```

### 'graph' sub-command

```
python sound_file_converter.py graph [-h] target-file

Show waveform graph.
The source file must be a wav format.

positional arguments:
  target-file
        Specify the target file name to process.

options:
  -h, --help
        Show this help message and exit.
```


## Developing environments

- Windows 11 Pro
- Python 3.13.4
- pydub==0.25.1
- numpy==2.3.0
- matplotlib==3.10.3
- ffmpeg version 7.1-essentials_build-www.gyan.dev
