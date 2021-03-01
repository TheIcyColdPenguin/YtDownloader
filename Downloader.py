from os import rename
import pytube as pt
from re import compile

v_re = compile('(https:\/\/)?www\.youtube.com\/watch\?v=[a-zA-Z0-9-_]+')
p_re = compile(
    '(https:\/\/)?www\.youtube.com\/playlist\?list=[a-zA-Z0-9-_]+')
link = input('Please provide a link : ')

mode = input('Audio or Video? (a/v) : ')

if v_re.match(link):
    yt = pt.YouTube(link)
    if mode == 'v':
        yr = yt.streams.get_highest_resolution()
        path = yr.download()
    elif mode == 'a':
        yr = yt.streams.get_audio_only()
        path = yr.download()
        rename(path, path[:-4] + ".mp3")
    else:
        print('Invalid stuff ngl')

elif p_re.match(link):
    pl = pt.Playlist(link)
    for vid in pl.video_urls:
        yt = pt.YouTube(vid)
        if mode == 'v':
            yr = yt.streams.get_highest_resolution()
            path = yr.download()
        elif mode == 'a':
            yr = yt.streams.get_audio_only()
            path = yr.download()
            rename(path, path[:-4] + ".mp3")
        else:
            print('Invalid stuff ngl')

else:
    print('Invalid stuff ngl')
