"""Music player using mixer from pygame"""

import os
from pygame import mixer

os.system("cls")


class music:
    def __init__(self) -> None:
        """
        The __init__ function is called when an instance of the class is created.
        The __init__ function receives a reference to the instance as its first argument,
        which we call self. The other arguments are provided by the caller.
        :param self: Refer to the object itself
        :param path: str: Specify the path of the music file
        :param fade: int: Set the fade time in milliseconds
        :return: The object of the class
        """
        mixer.init()

    @staticmethod
    def load(path: str) -> None:
        """
        The load function loads a song into the mixer.
        :param path: str: Specify the path to the music file
        :return: None
        """
        return mixer.music.load(path)

    def play(self, loops: int = -1, fade: int = 0, start: float = 0.0) -> None:
        """
        The play function plays the sound.

        :param self: Access the attributes of the class
        :param loops: int: Specify how many times the sound should be played
        :return: None
        """
        return mixer.music.play(loops=loops, fade_ms=fade, start=start)

    def lplay(
        self, path: str, loops: int = -1, fade: int = 0, start: float = 0.0
    ) -> None:
        """
        The lplay function plays a song from the given path.
        The lplay function has three parameters:
            path - The string containing the filepath of the song to be played.
            loops - An integer indicating how many times you would like to hear the song,
            default is infinite (- 1).
                If set to 0, then it will play once and stop.
                If set to 1 or more, then it will loop that many times so that you can keep playing
                songs in succession without having
        to call this function again.
                Note: if loops is greater than one and fade is non
        :param self: Reference the object itself
        :param path: str: Specify the path of the file to be played
        :param loops: int: Set the number of times the song is repeated
        :param fade: int: Fade in and out the music
        :param start: float: Start the music at a certain time
        :return: None
        """
        mixer.music.load(path)
        return mixer.music.play(loops=loops, fade_ms=fade, start=start)

    @staticmethod
    def pause() -> None:
        """
        The pause function is used to pause the music.

        :return: None
        """
        return mixer.music.pause()

    @staticmethod
    def unpause() -> None:
        """
        The pause function is used to unpause the music.

        :return: None
        """
        return mixer.music.unpause()

    @staticmethod
    def stop() -> None:
        """
        The stop function stops the music from playing.

        :return: None
        """
        return mixer.music.stop()


class Channel:
    def __init__(self, channel: int, loops: int = -1, fade: int = 0) -> None:
        self.channel = channel
        self.loops = loops
        self.fade = fade
        mixer.init()

    def play(self, path) -> None:
        """
        The play function plays a sound file.
        :param self: Access the attributes and methods of the class
        :param path: Specify the path of the sound file
        :return: None
        """
        return mixer.Channel(self.channel).play(
            mixer.Sound(path), loops=self.loops, fade_ms=self.fade
        )

    def pause(self) -> None:
        """
        The pause function pauses the music playback.
        :param self: Access the attributes and methods of the class in python
        :return: None
        """
        return mixer.Channel(self.channel).pause()

    def unpause(self) -> None:
        """
        The unpause function will unpause the music.
        :param self: Access the variables and methods of the class
        :return: None
        """
        return mixer.Channel(self.channel).unpause()

    def stop(self) -> None:
        """
        The stop function stops the music from playing.
        :param self: Refer to the object itself
        :return: None
        """
        return mixer.Channel(self.channel).stop()
