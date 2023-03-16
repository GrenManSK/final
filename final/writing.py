"""Writing methods"""

from tqdm import tqdm
import os
from time import sleep
from datetime import datetime
from threading import Thread
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
    def __init__(self, package: str, comment: str = 'Installing', bar: bool = False, move_by_command: bool = False):
        self.package = package
        self.comment = comment
        self.bar = bar
        self.move_by_command = move_by_command
        self._move = 0

    def start(self):
        """
        The start function is the main function of the class. It starts a thread that runs init()
        
        :param self: Represent the instance of the class
        :return: Nothing, so the return statement is never reached
        """
        
        Thread(target=self.init).start()

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
            if os.path.isfile('INSTALL_DONE'):
                break
            if os.path.isfile('INSTALL_ERROR'):
                error = True
                break
            if os.path.isfile('INSTALL_ALINST'):
                alinst = True
                break
            if os.path.isfile('INSTALL_PAUSE'):
                if not self.bar:
                    print('                                            ', end='\r')
                if self.bar:
                    tqdm.write(
                        '                                            ', end='\r')
                sleep(0.4)
                os.remove('INSTALL_PAUSE')
            if not self.bar:
                print(
                    f'{self.comment} {self.package} {char[number]}               ', end='\r')
            if self.bar:
                tqdm.write(
                    f'{self.comment} {self.package} {char[number]}               ', end='\r')
            if not self.move_by_command or self._move != 0 and self.move_by_command:
                number += 1
                if self.move_by_command:
                    self._move -= 1
            if number >= len(char):
                number = 0
            sleep(0.1)
        if error:
            if not self.bar:
                print(f'{self.comment} {self.package} ERROR             ')
            if self.bar:
                tqdm.write(f'{self.comment} {self.package} ERROR             ')
        elif alinst:
            if not self.bar:
                print(
                    f'{self.comment} {self.package} ALREADY INSTALLED             ')
            if self.bar:
                tqdm.write(
                    f'{self.comment} {self.package} ALREADY INSTALLED             ')
        else:
            if not self.bar:
                print(f'{self.comment} {self.package} DONE             ')
            if self.bar:
                tqdm.write(f'{self.comment} {self.package} DONE             ')
        try:
            os.remove('INSTALL_DONE')
        except Exception:
            pass
        try:
            os.remove('INSTALL_ERROR')
        except Exception:
            pass
        try:
            os.remove('INSTALL_ALINST')
        except Exception:
            pass
