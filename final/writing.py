"""Writing methods"""

from tqdm import tqdm
import os
from time import sleep
from datetime import datetime
from threading import Thread
import curses
from final.mathematical import get_id
import sys
datelog: str = datetime.now().strftime("%y-%m-%d-%H-%M-%S")


def log(msg: str, end: str = '\n') -> str:
    """
    It opens a file, writes a message to it, and closes the file

    :param msg: The message to be logged
    :param end: The character that will be used to end the line, defaults to \n (optional)
    """
    crashfile = open('crash_dump-' + datelog + ".txt", 'a', encoding='utf-8')
    crashfile.write(str(msg) + str(end))
    crashfile.close()
    return msg


def get_time() -> str:
    """
    The get_time function returns the current time in HH-MM-SS format.
       This is a useful function for generating timestamps.
    :return: The current time in the format of &quot;hour-minute-second&quot;
    """
    return datetime.now().strftime("%H-%M-%S")


class installing_carousel:
    def __init__(self, package: str, comment: str = 'Installing', bar: bool = False, move_by_command: bool = False, use_curses: bool = False, curses_y: int = 0, curses_x: int = 0, curses_obj = None):
        self.package = package
        self.comment = comment
        self.bar = bar
        self.move_by_command = move_by_command
        self._move = 0
        self.id = get_id()
        self.use_curses = use_curses
        self.curses_y = curses_y
        self.curses_x = curses_x
        self.curses_obj = curses_obj
        if self.use_curses and self.curses_obj is None:
            raise curses.error('curses object is not specified; curses_obj')

    def start(self):
        """
        The start function is the main function of the class. It starts a thread that runs init()

        :param self: Represent the instance of the class
        :return: Nothing, so the return statement is never reached
        """

        Thread(target=self.init).start()

    def pause(self):
        """
        The pause function is used to pause the installation of a package.

        :param self: Represent the instance of the class
        :return: Nothing, it just creates a file
        """
        open(f"INSTALL_PAUSE{self.id}", 'x')

    def unpause(self):
        open(f"INSTALL_UNPAUSE{self.id}", 'x')

    def stop(self, mode='s'):
        """
        The stop function is called when the user wants to stop the installation.

        :param self: Represent the instance of the class
        :param mode: Determine what file is created
        :return: The name of the file that is created
        """
        if mode == 's':
            open(f"INSTALL_DONE{self.id}", 'x')
        if mode == 'e':
            open(f"INSTALL_ERROR{self.id}", 'x')
        if mode == 'ali':
            open(f"INSTALL_ALINST{self.id}", 'x')

    def move(self):
        self._move += 1

    def init(self):
        """
        The init function is used to initialize the package installation.
        It will print a loading bar until it finds an INSTALL_DONE, INSTALL_ERROR or 
        INSTALL_ALINST file in the current directory. If it finds an INSTALL_DONE file, 
        it will print DONE after the package name and if it finds an INSTALL_ERROR file, 
        it will print ERROR after the package name. If it finds an INSTALL_ALINST file, 
        it will print ALREADY INSTALLED after the package name.

        :param self: Represent the instance of the class
        :return: Nothing, so the return statement is not needed
        """
        error = False
        alinst = False
        number = 0
        char = ['|', '/', '-', '\\']
        while True:
            if os.path.isfile(f'INSTALL_DONE{self.id}'):
                break
            if os.path.isfile(f'INSTALL_ERROR{self.id}'):
                error = True
                break
            if os.path.isfile(f'INSTALL_ALINST{self.id}'):
                alinst = True
                break
            if os.path.isfile(f'INSTALL_PAUSE{self.id}'):
                if not self.bar:
                    if not self.use_curses:
                        print(
                            '                                            ', end='\r')
                    else:
                        self.curses_obj.addstr(
                            self.curses_y, self.curses_x, '                                            ')
                        self.curses_obj.refresh()
                if self.bar:
                    tqdm.write(
                        '                                            ')
                os.remove(f'INSTALL_PAUSE{self.id}')
                while not os.path.isfile(f'INSTALL_UNPAUSE{self.id}'):
                    sleep(0.1)
                os.remove(f'INSTALL_UNPAUSE{self.id}')
            if not self.bar:
                if not self.use_curses:
                    print(
                        f'{self.comment} {self.package} {char[number]}               ', end='\r')
                else:
                    self.curses_obj.addstr(
                        self.curses_y, self.curses_x, f'{self.comment} {self.package} {char[number]}               ')
                    self.curses_obj.refresh()
            if self.bar:
                tqdm.write(
                    f'{self.comment} {self.package} {char[number]}               ')
            if not self.move_by_command or self._move != 0 and self.move_by_command:
                number += 1
                if self.move_by_command:
                    self._move -= 1
            if number >= len(char):
                number = 0
            sleep(0.1)
        if error:
            if not self.bar:
                if not self.use_curses:
                    print(f'{self.comment} {self.package} ERROR             ')
                else:
                    self.curses_obj.addstr(
                        self.curses_y, self.curses_x, f'{self.comment} {self.package} ERROR             ')
                    self.curses_obj.refresh()
            if self.bar:
                tqdm.write(f'{self.comment} {self.package} ERROR             ')
        elif alinst:
            if not self.bar:
                if not self.use_curses:
                    print(
                        f'{self.comment} {self.package} ALREADY INSTALLED             ')
                else:
                    self.curses_obj.addstr(
                        self.curses_y, self.curses_x, f'{self.comment} {self.package} ALREADY INSTALLED             ')
                    self.curses_obj.refresh()
            if self.bar:
                tqdm.write(
                    f'{self.comment} {self.package} ALREADY INSTALLED             ')
        else:
            if not self.bar:
                if not self.use_curses:
                    print(f'{self.comment} {self.package} DONE             ')
                else:
                    self.curses_obj.addstr(
                        self.curses_y, self.curses_x, f'{self.comment} {self.package} DONE             ')
                    self.curses_obj.refresh()
            if self.bar:
                tqdm.write(f'{self.comment} {self.package} DONE             ')
        try:
            os.remove(f'INSTALL_DONE{self.id}')
        except Exception:
            pass
        try:
            os.remove(f'INSTALL_ERROR{self.id}')
        except Exception:
            pass
        try:
            os.remove(f'INSTALL_ALINST{self.id}')
        except Exception:
            pass
