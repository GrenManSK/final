import zipfile
import os
import subprocess
import sys
import shutil
from pathlib import Path
import glob
from time import sleep
from tqdm import tqdm
from filesplit.merge import Merge


class FindError(Exception):
    pass


class unpack:
    def __init__(self, default_name: str = 'data.xp2', folder: str = './', files: list = []):
        self.default_name = default_name
        self.folder = folder
        self.files = files

    @staticmethod
    def download(url: str, fname: str, chunk_size: int = 1024) -> bool:
        """
        "Download a file from a URL to a local file."

        The first line is the function's signature. It's a single line of code that tells you everything
        you need to know about the function

        :param url: The URL of the file to download
        :type url: str
        :param fname: The name of the file to be downloaded
        :type fname: str
        :param chunk_size: The size of the chunks to download, defaults to 1024 (optional)
        """
        import requests
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
            return False
        return True

    def unpack(self):
        print('Downloading krkr-xp3 ...', end='\r')
        unpack.download(
            'https://github.com/awaken1ng/krkr-xp3/zipball/master', name := 'xp3.zip')
        print('Downloading krkr-xp3 DONE\n')
        print('Exporting krkr-xp3\n')
        with zipfile.ZipFile(name, mode='r') as zip:
            for member in tqdm(iterable=zip.namelist(), total=len(zip.namelist()), desc='Extracting '):
                try:
                    zip.extract(member)
                    tqdm.write(
                        f"{os.path.basename(member)}(" + str(os.path.getsize(member)) + "KB)")
                except zipfile.error as e:
                    pass
        print('\nExporting krkr-xp3 DONE\n')
        directory = None
        for path, currentDirectory, file in os.walk(Path.cwd()):
            for directory1 in currentDirectory:
                if directory1.startswith("awaken1ng-krkr-xp3-"):
                    print(directory1)
                    directory = directory1
        os.remove('xp3.zip')
        if directory is None:
            raise FindError
        sleep(0.5)
        shutil.move(directory + "/xp3.py", 'xp3.py')
        shutil.move(directory + "/xp3reader.py", 'xp3reader.py')
        shutil.move(directory + "/xp3writer.py", 'xp3writer.py')
        os.mkdir('structs')
        for i in glob.iglob(directory + '/*'):
            try:
                shutil.copy2(i, './')
            except PermissionError:
                continue
        for i in glob.iglob(directory + '/structs/*'):
            try:
                shutil.copy2(i, 'structs/')
            except PermissionError:
                continue
        for i in ['requirements.txt', 'README.md', 'tests.py']:
            os.remove(i)
        shutil.rmtree(directory)
        datafiles = self.files
        if len(datafiles) == 0:
            for file in os.listdir(self.folder):
                if file.startswith(self.default_name.split('.')[0]):
                    if file.endswith('.' + self.default_name.split('.')[-1]):
                        datafiles.append(file)
        for i in range(1, len(datafiles)+1):
            print('\nUnpacking data\n')
            unpack.unpack_one(self, datafiles[-i])
        sleep(1)
        os.remove('xp3.py')
        os.remove('xp3reader.py')
        os.remove('xp3writer.py')
        shutil.rmtree('structs')

    def unpack_one(self, filename):
        with zipfile.ZipFile(filename, mode='r') as zip:
            for member in tqdm(iterable=zip.namelist(), total=len(zip.namelist()), desc='Rozbaľujem '):
                try:
                    zip.extract(member)
                    tqdm.write(
                        f"{os.path.basename(member)}(" + str(os.path.getsize(member)) + "B)")
                    print(f"{os.path.basename(member)}(" +
                          str(os.path.getsize(member)) + "B)")
                    sleep(0.01)
                except zipfile.error as e:
                    pass
            zip.close()
        subprocess.call([sys.executable, 'xp3.py', 'data.xp3',
                        'data1', '-e', 'neko_vol0_steam'])
        if filename == self.default_name:
            directories = [x[0] for x in os.walk('data1/')]
            directories.pop(0)
            for i in range(0, len(directories)):
                directories[i] = directories[i][6:]
            source_dir = 'data1/'
            target_dir = './'
            file_names = os.listdir(source_dir)
            for file_name in file_names:
                shutil.move(os.path.join(source_dir, file_name), target_dir)
            for i in directories:
                source_dir = i
                print(i)
                file_names = os.listdir(source_dir)
                for file_name in file_names:
                    if file_name == 'manifest':
                        continue
                    break
                if i.endswith('_cut'):
                    Merge(i, directories[0], os.path.basename(
                        i[0:-4] + '.' + file_name.split('.')[-1])).merge(cleanup=True)  # type: ignore
                    shutil.rmtree(i)
            shutil.rmtree('data1')
            sleep(1)
        os.remove('data.xp3')
        os.remove(filename)
