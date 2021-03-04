from os import rename
import pytube as pt
from re import compile

v_re = compile('(https:\/\/)?www\.youtube.com\/watch\?v=[a-zA-Z0-9-_]+')
p_re = compile(
    '(https:\/\/)?www\.youtube.com\/playlist\?list=[a-zA-Z0-9-_]+')
link = input('Please provide a link : ')

mode = input('Audio or Video? (a/v) : ')


def download_video(stream, audio):
    path = stream.download()
    if audio:
        new_path = path[:-4] + ".mp3"
        rename(path, new_path)
        return new_path

    return path


if v_re.match(link):
    yt = pt.YouTube(link)
    if mode == 'v':
        download_video(yt.streams.get_highest_resolution(), False)
    elif mode == 'a':
        download_video(yt.streams.get_audio_only(), True)
    else:
        print('Invalid stuff ngl')

elif p_re.match(link):
    pl = pt.Playlist(link)
    for vid in pl.video_urls:
        yt = pt.YouTube(vid)
        if mode == 'v':
            download_video(yt.streams.get_highest_resolution(), False)
        elif mode == 'a':
            download_video(yt.streams.get_audio_only(), True)
        else:
            print('Invalid stuff ngl')

else:
    print('Invalid stuff ngl')
