import pytube as pt
import moviepy.editor as mp
from os import remove
from re import compile

v_re = compile('www\\.youtube\\.com\\/watch\\?v=[_a-zA-Z0-9-]+')
p_re = compile('www\\.youtube\\.com\\/playlist\\?list=[_a-zA-Z0-9-]+')
link = input('Please provide a link : ')
method = input('Is the above link a single video or a playlist? (s/p) : ')
mode = input('Audio or Video? (a/v) : ')

if method == 's':
    yt = pt.YouTube(link)
    yr = yt.streams.get_highest_resolution()
    path = yr.download()
    if mode == 'v':
        pass
    elif mode == 'a':
        video_file_to_convert = mp.VideoFileClip(path)
        video_file_to_convert.audio.write_audiofile(path[:-4] + '.mp3')
        video_file_to_convert.close()
        remove(path)
    else:
        print('Invalid stuff ngl')

elif method == 'p':
    pl = pt.Playlist(link)
    for vid in pl.video_urls:
        yt = pt.YouTube(vid)
        yr = yt.streams.get_highest_resolution()
        path = yr.download()
        if mode == 'v':
            pass
        else:
            if mode == 'a':
                video_file_to_convert = mp.VideoFileClip(path)
                video_file_to_convert.audio.write_audiofile(path[:-4] + '.mp3')
                video_file_to_convert.close()
                remove(path)
            else:
                print('Invalid stuff ngl')

else:
    print('Invalid stuff ngl')
