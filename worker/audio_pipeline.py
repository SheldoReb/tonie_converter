import ffmpeg
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK, COMM

def process_track(input_pcm, output_mp3, tags, preset='speech', target_lufs=-18, true_peak=-1.0, bitrate_k=96, mono=True):
    # ffmpeg filter chain
    filters = []
    if preset == 'speech':
        filters.append('highpass=f=90')
        filters.append('equalizer=f=3000:t=q:w=2:g=2')
        filters.append('deesser')
        filters.append('acompressor=ratio=2:threshold=-20dB')
    filters.append(f'loudnorm=I={target_lufs}:TP={true_peak}:dual_mono=true')
    if mono:
        filters.append('pan=mono|c0=.5*c0+.5*c1')
    filter_str = ','.join(filters)
    ffmpeg.input(input_pcm, format='s16le', ac=2, ar=44100)
        .output(output_mp3, acodec='mp3', audio_bitrate=f'{bitrate_k}k', ar=44100, ac=1 if mono else 2, af=filter_str)
        .run(overwrite_output=True)
    # Tagging
    audio = MP3(output_mp3, ID3=ID3)
    audio.tags.add(TIT2(encoding=3, text=tags.get('title', '')))
    audio.tags.add(TPE1(encoding=3, text=tags.get('artist', '')))
    audio.tags.add(TALB(encoding=3, text=tags.get('album', '')))
    audio.tags.add(TRCK(encoding=3, text=str(tags.get('tracknumber', ''))))
    if 'comment' in tags:
        audio.tags.add(COMM(encoding=3, lang='deu', desc='desc', text=tags['comment']))
    audio.save()
