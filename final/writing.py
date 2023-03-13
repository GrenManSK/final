"""Writing methods"""

from tqdm import tqdm
import os
from time import sleep
from datetime import datetime
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



def installing_carousel(package: str, comment: str = 'Installing', bar=False):
    """
    The installing_carousel function is a function that will print out the string 'Installing' and then
    the package name, in an animated fashion. It will do this until it reaches the INSTALL_DONE file, which
    is created by another function. This is to prevent multiple instances of installing_carousel from running at once.
    
    :param package: str: Specify the package that is being installed
    :param comment: str: Tell the user what is happening during the installation process
    :return: :
    """
    error = False
    alinst = False
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
            if not bar:
                print('                                            ', end='\r')
            if bar:
                tqdm.write('                                            ', end='\r')
            sleep(0.4)
            os.remove('INSTALL_PAUSE')
        if not bar:
            print(f'{comment} {package} /               ', end='\r')
        if bar:
            tqdm.write(f'{comment} {package} /               ', end='\r')
        sleep(0.1)
        if os.path.isfile('INSTALL_DONE'):
            break
        if os.path.isfile('INSTALL_ERROR'):
            error = True
            break
        if os.path.isfile('INSTALL_ALINST'):
            alinst = True
            break
        if os.path.isfile('INSTALL_PAUSE'):
            if not bar:
                print('                                            ', end='\r')
            if bar:
                tqdm.write('                                            ', end='\r')
            sleep(0.4)
            os.remove('INSTALL_PAUSE')
        if not bar:    
            print(f'{comment} {package} -               ', end='\r')
        if bar:
            tqdm.write(f'{comment} {package} -               ', end='\r')
        sleep(0.1)
        if os.path.isfile('INSTALL_DONE'):
            break
        if os.path.isfile('INSTALL_ERROR'):
            error = True
            break
        if os.path.isfile('INSTALL_ALINST'):
            alinst = True
            break
        if os.path.isfile('INSTALL_PAUSE'):
            if not bar:
                print('                                            ', end='\r')
            if bar:
                tqdm.write('                                            ', end='\r')
            sleep(0.4)
            os.remove('INSTALL_PAUSE')
        if not bar:
            print(f'{comment} {package} \\              ', end='\r')
        if bar:
            tqdm.write(f'{comment} {package} \\              ', end='\r')
        sleep(0.1)
        if os.path.isfile('INSTALL_DONE'):
            break
        if os.path.isfile('INSTALL_ERROR'):
            error = True
            break
        if os.path.isfile('INSTALL_ALINST'):
            alinst = True
            break
        if os.path.isfile('INSTALL_PAUSE'):
            if not bar:
                print('                                            ', end='\r')
            if bar:
                tqdm.write('                                            ', end='\r')
            sleep(0.4)
            os.remove('INSTALL_PAUSE')
        if not bar:
            print(f'{comment} {package} |               ', end='\r')
        if bar:
            tqdm.write(f'{comment} {package} |               ', end='\r')
        sleep(0.1)
    if error:
        if not bar:
            print(f'{comment} {package} ERROR             ')
        if bar:
            tqdm.write(f'{comment} {package} ERROR             ')
    elif alinst:
        if not bar:
            print(f'{comment} {package} ALREADY INSTALLED             ')
        if bar:
            tqdm.write(f'{comment} {package} ALREADY INSTALLED             ')
    else:
        if not bar:
            print(f'{comment} {package} DONE             ')
        if bar:
            tqdm.write(f'{comment} {package} DONE             ')
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