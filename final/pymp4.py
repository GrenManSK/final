"""
Video changes
"""

import moviepy.editor as mp


class video:
    def __init__(self, filename: str,):
        self.filename = filename

    def g2v(self):
        clip = mp.VideoFileClip(self.filename)
        clip.write_videofile(
            '.' + self.filename.split('.')[0:-1][1] + '.mp4')
        clip.reader.close()  # type: ignore
