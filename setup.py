from setuptools import setup
from setuptools import find_packages

from pathlib import Path
from final import VERSION, AUTHOR

this_directory = Path(__file__).parent

long_description = (this_directory / "README.md").read_text()


setup(
    name='final',
    version=VERSION,
    description='final',
    long_description=long_description,

    long_description_content_type='text/markdown',
    author=AUTHOR,
    install_requires=['glob2', 'tk', 'mal-api', 'urllib3', 'Pillow', 'PyAutoGUI', 'show-in-file-manager', 'tqdm', 'python-vlc', 'pygame', 'bs4', 'snakeviz', 'windows-curses',
                      'pytube', 'moviepy', 'filesplit', 'CProfileV', 'PyGetWindow', 'mysql-connector-python', 'thread6', 'bing-image-urls', 'setuptools', 'anitopy', 'diff_match_patch'],
    packages=find_packages(exclude=('tests*', 'testing*')),
)
