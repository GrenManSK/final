import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import re
import os
import requests
from pytube import YouTube
from moviepy.editor import *
import logging


def DownloadMusic(music_name):
    query_string = urllib.parse.urlencode({"search_query": music_name})
    formatUrl = urllib.request.urlopen(
        "https://www.youtube.com/results?" + query_string)
    logging.debug("Searched in: https://www.youtube.com/results?" + query_string)
    search_results = re.findall(
        r"watch\?v=(\S{11})", formatUrl.read().decode())
    clip = requests.get("https://www.youtube.com/watch?v=" +
                        "{}".format(search_results[0]))
    clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
    logging.debug("Found: https://www.youtube.com/watch?v=" + "{}".format(search_results[0]))
    inspect = BeautifulSoup(clip.content, "html.parser")
    yt_title = inspect.find_all("meta", property="og:title")
    for concatMusic1 in yt_title:
        pass
    print('\nStarting download')
    print(clip2)
    print(concatMusic1['content'])

    def run(clip2):
        out_file = YouTube(
            str(clip2)).streams.get_highest_resolution().download()
        base, ext = os.path.splitext(out_file)
        base = os.path.basename(base)
        base.replace("[","(")
        base.replace("]",")")
        base.replace("'","")
        base.replace("\"","")
        new_file = base + '.mp3'
        print(os.path.join(out_file))
        print(os.path.join('assets\\' + new_file))
        video = VideoFileClip(os.path.join(out_file))
        video.audio.write_audiofile(os.path.join('assets\\' + new_file))
        video.close()
        os.remove(out_file)
        print('Done\n')
        return base
    a = run(clip2)
    return a


if __name__ == '__main__':
    DownloadMusic(input())
