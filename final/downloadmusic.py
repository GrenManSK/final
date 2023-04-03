import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import re
import os
import requests
from pytube import YouTube
from moviepy.editor import *
import logging


def DownloadMusic(music_name, directory):
    """
    The DownloadMusic function takes in a string of the name of the song you want to download.
    It then searches for that song on YouTube and downloads it as an mp3 file into your assets folder.
    The function returns a string containing the name of the downloaded file.

    :param music_name: Search for the music in youtube
    :return: The name of the downloaded music
    """
    query_string = urllib.parse.urlencode({"search_query": music_name})
    formatUrl = urllib.request.urlopen(
        "https://www.youtube.com/results?" + query_string)
    logging.debug(
        "Searched in: https://www.youtube.com/results?" + query_string)
    search_results = re.findall(
        r"watch\?v=(\S{11})", formatUrl.read().decode())
    clip = requests.get("https://www.youtube.com/watch?v=" +
                        "{}".format(search_results[0]))
    clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
    logging.debug("Found: https://www.youtube.com/watch?v=" +
                  "{}".format(search_results[0]))
    inspect = BeautifulSoup(clip.content, "html.parser")
    yt_title = inspect.find_all("meta", property="og:title")
    for concatMusic1 in yt_title:
        pass
    print('\nStarting download')
    print(clip2)
    print(concatMusic1['content'])

    def run(clip2):
        """
        The run function takes a YouTube link as an argument and downloads the highest resolution video file.
        It then extracts the audio from that video file, saves it to a new mp3 file, and deletes the original video.
        The function returns the name of this new mp3 file.

        :param clip2: Pass the youtube link to the run function
        :return: The name of the song
        """
        out_file = YouTube(
            str(clip2)).streams.get_highest_resolution().download()
        base, ext = os.path.splitext(out_file)
        base = os.path.basename(base)
        base.replace("[", "(")
        base.replace("]", ")")
        base.replace("'", "")
        base.replace("\"", "")
        new_file = base + '.mp3'
        print(os.path.join(out_file))
        print(os.path.join(directory + '\\' + new_file))
        video = VideoFileClip(os.path.join(out_file))
        video.audio.write_audiofile(os.path.join(directory + '\\' + new_file))
        video.close()
        os.remove(out_file)
        print('Done\n')
        return base
    a = run(clip2)
    return a


if __name__ == '__main__':
    DownloadMusic(input())
