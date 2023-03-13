"""
API method

Raises:
    ConnectionError: No connection
    ValueError: No data available from server
    ValueError: Type mismatch
    ValueError: Category mismatch
    ValueError: Category mismatch
    ConnectionError: No connection
    ConnectionError: No connection
    ValueError: Server not found
    ValueError: Server not found

Returns:
    _type_: self
"""

import requests
from tqdm import tqdm
import logging
import os
import moviepy.editor as mp
import vlc
from time import sleep
from PIL import Image
import pyautogui as pg
import pygetwindow
import final.pymp4


logging.basicConfig(level=logging.WARNING,
                    format="%(asctime)s - %(levelname)s - %(message)s")


def download(url: str, fname: str, chunk_size: int = 1024) -> bool:
    """
    Download a file from a URL to a local file.

    The first line is the function's signature. It's a single line of code that tells you everything
    you need to know about the function

    :param url: The URL of the file to download
    :type url: str
    :param fname: The name of the file to be downloaded
    :type fname: str
    :param chunk_size: The size of the chunks to download, defaults to 1024 (optional)
    """
    if os.path.exists(fname):
        logging.warning(
            'file %s already exists, still downloading and replacing', fname)
    try:
        resp = requests.get(url, stream=True)
        total: int = int(resp.headers.get('content-length', 0))
        with open(fname, 'wb') as file, tqdm(
            desc=fname,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in resp.iter_content(chunk_size=chunk_size):
                size = file.write(data)
                bar.update(size)
    except ConnectionError:
        logging.error("Failed to download file: %s", fname)
        return False
    return True


class animq:
    """
    Quotes from anime
    """

    def __init__(self):
        try:
            self.data: dict[str, str] = requests.get(
                "https://animechan.vercel.app/api/random").json()
        except requests.exceptions.ConnectionError:
            logging.error("Connection error")
            raise ConnectionError(
                'Make sure you have a connection established')
        try:
            self.anime: str = self.data["anime"]
            self.character: str = self.data["character"]
            self.quote: str = self.data["quote"]
        except TypeError:
            logging.error("No data available")
            raise ValueError('Server returned no data')

    def getq(self):
        """
        The get_anime function returns a string containing the anime, character, and quote of the given character.

        :param self: Access variables that belongs to the class
        :return: A string containing the anime, character and quote
        """

        return "Anime: " + self.anime + '\nCharacter: ' + self.character + "\nQuote: " + self.quote


class fanart:
    def __init__(self, server: int = 0, type: str = 'sfw', category: str = 'waifu'):
        self.error: list[str] = []
        servers = [0, 1]
        types = ['sfw', 'nsfw']
        category_sfw: list[str] = ["waifu", "neko", "shinobu", "megumin", "bully", "cuddle", "cry", "hug", "awoo", "kiss", "lick", "pat", "smug", "bonk", "yeet", "blush",
                                   "smile", "wave", "highfive", "handhold", "nom", "bite", "glomp", "slap", "kill", "kick", "happy", "wink", "poke", "dance", "cringe", "back"]
        category_nsfw: list[str] = ['waifu', 'neko', 'trap', 'blowjob', 'back']
        if not type in types:
            logging.error("Unknown type")
            raise ValueError(f'Type not found {types}, given {type}')
        if type == 'sfw' and category not in category_sfw and server == 0:
            logging.error("Unknown category")
            if category in category_nsfw:
                raise ValueError(f'Category not found, but found in type nsfw')
            raise ValueError(
                f'Category not found {category_sfw}, given {category}')
        if type == 'nsfw' and category not in category_nsfw and server == 0:
            logging.error('Unknown category')
            if category in category_sfw:
                raise ValueError(f'Category not found, but found in type sfw')
            raise ValueError(
                f'Category not found {category_nsfw}, given {category}')
        if server == 0:
            try:
                resp = requests.get(
                    "https://api.waifu.pics/" + type + "/" + category)
            except requests.exceptions.ConnectionError:
                logging.error("Connection error")
                raise ConnectionError(
                    'Make sure you have a connection established')
            self.data: dict[str, str] = resp.json()
            self.res = requests.get(self.data["url"], stream=True)
        elif server == 1:
            try:
                resp = requests.get("https://nekos.best/api/v2/neko")
            except requests.exceptions.ConnectionError:
                logging.error("Connection error")
                raise ConnectionError(
                    'Make sure you have a connection established')
            self.data: dict[str, str] = resp.json()
            self.res = requests.get(
                self.data["results"][0]["url"], stream=True)  # type: ignore
            if type != 'sfw' or category != 'waifu':
                logging.warning("Type and category not supported on server 1")
                self.error.append(
                    f'type or category not supported on this server, given {server}')
        else:
            raise ValueError(f"Server not found: {servers}, given {server}")
        if self.res.status_code == 200:
            self.server = server

    def get_new(self, server: int = 0, type: str = 'sfw', category: str = 'waifu'):
        servers = [0, 1]
        types = ['sfw', 'nsfw']
        category_sfw: list[str] = ["waifu", "neko", "shinobu", "megumin", "bully", "cuddle", "cry", "hug", "awoo", "kiss", "lick", "pat", "smug", "bonk", "yeet", "blush",
                                   "smile", "wave", "highfive", "handhold", "nom", "bite", "glomp", "slap", "kill", "kick", "happy", "wink", "poke", "dance", "cringe", "back"]
        category_nsfw: list[str] = ['waifu', 'neko', 'trap', 'blowjob', 'back']
        if not type in types:
            logging.error("Unknown type")
            raise ValueError(f'Type not found {types}, given {type}')
        if type == 'sfw' and category not in category_sfw and server == 0:
            logging.error("Unknown category")
            if category in category_nsfw:
                raise ValueError(f'Category not found, but found in type nsfw')
            raise ValueError(
                f'Category not found {category_sfw}, given {category}')
        if type == 'nsfw' and category not in category_nsfw and server == 0:
            logging.error('Unknown category')
            if category in category_sfw:
                raise ValueError(f'Category not found, but found in type sfw')
            raise ValueError(
                f'Category not found {category_nsfw}, given {category}')
        if server == 0:
            try:
                resp = requests.get(
                    "https://api.waifu.pics/" + type + "/" + category)
            except requests.exceptions.ConnectionError:
                logging.error("Connection error")
                raise ConnectionError(
                    'Make sure you have a connection established')
            self.data: dict[str, str] = resp.json()
            self.res = requests.get(self.data["url"], stream=True)
        elif server == 1:
            try:
                resp = requests.get("https://nekos.best/api/v2/neko")
            except requests.exceptions.ConnectionError:
                logging.error("Connection error")
                raise ConnectionError(
                    'Make sure you have a connection established')
            self.data: dict[str, str] = resp.json()
            self.res = requests.get(
                self.data["results"][0]["url"], stream=True)  # type: ignore
            if type != 'sfw' or category != 'waifu':
                logging.warning("Type and category not supported on server 1")
                self.error.append(
                    f'type or category not supported on this server, given {server}')
        else:
            raise ValueError(f"Server not found: {servers}, given {server}")
        if self.res.status_code == 200:
            self.server = server
        return self

    def get_error(self):
        """
        The get_error function returns the error of the current state.

        :param self: Refer to the object itself
        :return: The error of the neuron
        """
        return self.error

    def get_url(self):
        """
        The get_url function returns the URL of a given search result.
        If there is no server specified, it will return the URL from the 
        first search result in self.data[&quot;results&quot;]. If there is a server 
        specified, it will return the URL from that specific search result.

        :param self: Reference the object itself
        :return: The url of the first search result
        """
        if self.server == 0:
            return self.data["url"]
        elif self.server == 1:
            return self.data["results"][0]["url"]  # type: ignore

    def get_data(self):
        """
        The get_data function returns the data stored in the object. If no data is present, it will return None.

        :param self: Access variables that belongs to the class
        :return: The data attribute of the object
        """
        if self.server == 0:
            return self.data
        elif self.server == 1:
            return self.data

    def download(self, filename: str = 'image.png', destination: str = '.\\'):
        """
        The download function downloads the image from the url and saves it to a specified location.
        The function takes two arguments, filename and destination. 
        If no filename is given, then 'image.png' will be used as default value for the file name argument. 
        If no destination is given, then current working directory will be used as default value for the destination argument.

        :param self: Access variables that belongs to the class
        :param filename: str: Specify the name of the file that will be downloaded
        :param destination: str: Specify the directory where the image is to be saved
        :return: The filename of the image
        """
        if self.res.status_code == 200:
            if self.server == 0:
                if self.data["url"].split('.')[-1] == 'gif':
                    logging.info("Downloading image as gif")
                    filename = destination + \
                        str(filename.split('.')[0:-1][0]) + '.gif'
                    download(self.data['url'], filename)
                else:
                    filename = destination + filename
                    download(self.data['url'], filename)
            elif self.server == 1:
                download(self.data["results"][0]["url"],  # type: ignore
                         destination + filename)
            else:
                logging.error('Server not found')
                raise ValueError('Server not found')
            self.filename = filename
            return self
        return self

    def show(self, side: str = 'right'):
        """
        The show function is used to display the image. It takes a single argument, side, which defaults to right.
        The show function will open the image in Windows Photo Viewer and then play it in VLC media player.

        :param self: Access variables that belongs to the class
        :param side: str: Specify which side of the screen to show the image on
        :return: The object itself
        """
        if self.filename.split('.')[-1] == 'gif':
            if os.path.exists(self.filename):
                final.pymp4.video(self.filename).g2v()
                os.remove(self.filename)
            if os.path.exists('.' + self.filename.split('.')[0:-1][1] + '.mp4'):
                player = vlc.Instance('--input-repeat=999999')
                media_list = player.media_list_new()  # type: ignore
                self.media_player = player.media_list_player_new()  # type: ignore
                media = player.media_new(  # type: ignore
                    '.' + self.filename.split('.')[0:-1][1] + '.mp4')
                media_list.add_media(media)
                self.media_player.set_media_list(media_list)
                player.vlm_set_loop("video", True)  # type: ignore
                self.media_player.play()
                sleep(0.4)
                window = pygetwindow.getWindowsWithTitle(
                    'VLC (Direct3D11 Output)')[0]
                window.activate()
                pg.keyDown('win')
                pg.press(side)
                pg.keyUp('win')
                pg.press('esc')
                sleep(0.25)
                pg.keyDown('alt')
                pg.press('tab')
                pg.keyUp('alt')
                sleep(1)
            else:
                logging.error('File not found')
        else:
            img = Image.open(self.filename)
            img.show()
            pg.keyDown('win')
            pg.press('right')
            pg.keyUp('win')
            pg.press('esc')
            sleep(0.25)
            pg.keyDown('alt')
            pg.press('tab')
            pg.keyUp('alt')
        return self

    def hide(self, delete: bool = True):
        """
        The hide function hides the image or video.

        :param self: Access the class attributes
        :return: None
        """
        if self.filename.split('.')[-1] == 'gif':
            self.media_player.stop()  # type: ignore
            sleep(0.1)
            if delete:
                os.remove('.' + self.filename.split('.')[0:-1][1] + '.mp4')
        else:
            pg.keyDown('alt')
            pg.press('tab')
            pg.keyUp('alt')
            pg.keyDown('alt')
            pg.press('f4')
            pg.keyUp('alt')
            if delete:
                os.remove(self.filename)
        return self

    def sleep(self, seconds: float):
        from time import sleep
        sleep(seconds)
        return self
