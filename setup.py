from setuptools import setup
from setuptools import find_packages

setup(
    name ='final' ,
    version='1.0.0',
    description='final',
    author='GrenManSK',
    install_requires=['glob2', 'tk', 'mal-api', 'urllib3', 'Pillow', 'PyAutoGUI', 'show-in-file-manager', 'tqdm', 'python-vlc', 'pygame','bs4', 'pytube', 'moviepy', 'filesplit', 'CProfileV', 'PyGetWindow', 'mysql-connector-python', 'thread6', 'bing-image-urls', 'setuptools'],
    packages=find_packages(exclude=('tests*', 'testing*')),
)
