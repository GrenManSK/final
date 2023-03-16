"""
Video changes
"""

import moviepy.editor as mp


class video:
    def __init__(self, filename: str,):
        self.filename = filename

    def g2v(self):
        """
        The g2v function takes a .gif file and converts it to an mp4 video.
            The function uses the moviepy library, which is built on top of FFmpeg.
            It requires that you have FFmpeg installed on your computer.
        
        :param self: Represent the instance of the class
        :return: A video file
        :doc-author: Trelent
        """
        
        clip = mp.VideoFileClip(self.filename)
        clip.write_videofile(
            '.' + self.filename.split('.')[0:-1][1] + '.mp4')
        clip.reader.close()  # type: ignore
