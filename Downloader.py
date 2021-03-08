from os import remove
import pytube as pt
from re import compile
from moviepy.editor import VideoFileClip
import music_tag
import requests


def download_video(link, audio):
    yt = pt.YouTube(link)
    stream = yt.streams.get_highest_resolution()
    path = stream.download()

    if audio:
        # Convert to audio
        new_path = path[:-4] + ".mp3"
        file = VideoFileClip(path)
        file.audio.write_audiofile(new_path, bitrate="320k")
        remove(path)

        # Read lyrics
        try:
            subtitle_path = yt.caption_tracks[0].download()
            subtitle = open(subtitle_path)
            lyrics = subtitle.read()
            subtitle.close()
            remove(subtitle_path)
        except:
            lyrics = ""

        # Get thumbnail
        thumbnail_data = requests.get(yt.thumbnail_url)

        # Get metadata
        metadata = yt.metadata.metadata

        f = music_tag.load_file(new_path)
        f['artist'] = metadata[0]['Artist'] if len(metadata) > 0 else yt.author
        f['artwork'] = thumbnail_data.content
        f['comment'] = yt.description
        f['compilation'] = False
        f['composer'] = metadata[0]['Artist'] if len(
            metadata) > 0 else yt.author
        f['lyrics'] = lyrics
        f['tracktitle'] = metadata[0]['Song'] if len(
            metadata) > 0 else yt.title
        f['year'] = yt.publish_date.year

        f.save()


def main(link, mode):
    v_re = compile('(https:\/\/)?(www\.)?youtube.com\/watch\?v=[a-zA-Z0-9-_]+')
    p_re = compile(
        '(https:\/\/)?(www\.)?youtube.com\/playlist\?list=[a-zA-Z0-9_-]+')

    if v_re.match(link):
        try:
            download_video(link, mode == 'a')
        except:
            None

    elif p_re.match(link):
        pl = pt.Playlist(link)
        for vid in pl.video_urls:
            try:
                download_video(vid, mode == 'a')
            except:
                None


if __name__ == '__main__':
    link = input('Please provide a link : ')
    mode = input('Audio or Video? (a/v) : ')

    main(link, mode)
