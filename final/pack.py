import os
import shutil
import subprocess
import sys
import zipfile
import glob
from tqdm import tqdm
from pathlib import Path
from subprocess import check_output
from time import sleep
from filesplit.split import Split
datapart = 0
breaked = True


class FindError(Exception):
    pass


class pack:
    def __init__(self, filename, default_name: str = 'data.xp2', uncoded=[], uncoded_folders=[], max_mbs: int = 0):  # type: ignore
        self.filename = filename
        self.default_name = default_name
        self.uncoded = uncoded
        self.uncoded_folders = uncoded_folders
        if max_mbs == 0:
            self.max_mbs = 32768
        else:
            self.max_mbs = max_mbs
        for file_name in os.listdir(filename + '/'):
            pass

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

    def pack(self, download = True):
        if download:
            pack.download(
                'https://github.com/awaken1ng/krkr-xp3/zipball/master', name := 'xp3.zip')
            with zipfile.ZipFile(name, mode='r') as zip:
                for member in tqdm(iterable=zip.namelist(), total=len(zip.namelist()), desc='Extracting '):
                    try:
                        zip.extract(member)
                        tqdm.write(
                            f"{os.path.basename(member)}(" + str(os.path.getsize(member)) + "KB)")
                    except zipfile.error as e:
                        pass
            directory = None
            for path, currentDirectory, files in os.walk(Path.cwd()):
                for directory1 in currentDirectory:
                    if directory1.startswith("awaken1ng-krkr-xp3-"):
                        print(directory1)
                        directory = directory1
            os.remove('xp3.zip')
            if directory == None:
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
        cut = False
        if self.max_mbs == 0:
            pack.pack_one(self)
        else:
            while True:
                breaked = pack.pack_one(self)
                if not breaked:
                    break
        sleep(1)
        os.remove('xp3.py')
        os.remove('xp3reader.py')
        os.remove('xp3writer.py')
        shutil.rmtree('structs')
        if isinstance(self.filename, str):
            shutil.rmtree(self.filename)
        elif isinstance(self.filename, list):
            for i in range(len(self.filename)):
                shutil.rmtree(self.filename[i])

    def pack_one(self):
        global datapart
        global breaked
        datapart += 1
        try:
            os.mkdir('datafolder')
        except FileExistsError:
            pass
        if datapart == 1:
            cachename = self.default_name
        else:
            cachename = self.default_name.split(
                '.')[0] + '_part' + str(datapart) + '.' + self.default_name.split('.')[-1]
        sleep(0.2)
        total_size = 0
        total_size1 = 0
        breaked = False
        if isinstance(self.filename, str):
            times = 0
            source_dir = self.filename + '/'
            os.mkdir('datafolder/' + source_dir)
            for file_name in os.scandir(source_dir):
                if file_name.is_dir():
                    if file_name.path.endswith('_cut'):
                        dir_name = file_name.path.split('.')[0]
                        dirs = glob.glob(dir_name + '/*')
                        for i in dirs:
                            if i.split('\\')[-1] != 'manifest' and breaked:
                                break
                            print(i)
                            try:
                                os.mkdir('datafolder/' + dir_name)
                            except FileExistsError:
                                pass
                            shutil.move(i, 'datafolder/' + i)
                            if breaked:
                                shutil.rmtree(file_name.path)
                            breaked = True
                            continue
                        if len(dirs) == 0:
                            shutil.rmtree(dir_name + '/')
                        break
                    break
                times += 1
                file_stats = os.stat(file_name)
                filesize = file_stats.st_size / (1024 * 1024)
                total_size += filesize
                if total_size > self.max_mbs:
                    if times == 1:
                        dir_name = file_name.path.split('.')[0] + '_cut'
                        os.mkdir('datafolder/' + dir_name)
                        os.mkdir(dir_name + '/')
                        mb = 1000000*self.max_mbs
                        Split(file_name.path,
                              dir_name + '/',).bysize(mb)
                        os.remove(file_name.path)
                        for i in glob.glob(dir_name + '/*' + '.' + file_name.path.split('.')[-1]):
                            print(i)
                            shutil.move(i, 'datafolder/' + i)
                            break
                    breaked = True
                    break
                print(f'File Size in MegaBytes is {filesize}')
                shutil.move(file_name.path, 'datafolder/' + file_name.path)
        elif isinstance(self.filename, str):
            source_dir = self.filename + '/'
            os.mkdir('datafolder/' + source_dir)
            times = 0
            for file_name in os.listdir(source_dir):
                times += 1
                file_stats = os.stat(source_dir + file_name)
                filesize = file_stats.st_size / (1024 * 1024)
                total_size += filesize
                total_size1 += filesize
                if total_size > self.max_mbs:
                    if times == 1:
                        dir_name = file_name.split('.')[0] + '_cut'
                        os.mkdir('datafolder/' +
                                 self.filename + '/' + dir_name)
                        os.mkdir(self.filename + '/' + dir_name + '/')
                        mb = 1000000*self.max_mbs
                        Split(self.filename + '/' + file_name,
                              self.filename + '/' + dir_name + '/',).bysize(mb)
                        os.remove(self.filename + '/' + file_name)
                        for i in glob.glob(self.filename + '/' + dir_name + '/*' + '.' + file_name.split('.')[-1]):
                            print(i)
                            shutil.move(i, 'datafolder/' + i)
                            break
                    breaked = True
                    break
                print(f'File Size in MegaBytes is {filesize}')
                shutil.move(os.path.join(source_dir, file_name),
                            'datafolder/' + source_dir)
        elif isinstance(self.filename, list):
            for i in range(0, len(self.filename)):
                source_dir = self.filename[i] + '/'
                os.mkdir('datafolder/' + source_dir)
                for file_name in os.listdir(source_dir):
                    file_stats = os.stat(source_dir + file_name)
                    filesize = file_stats.st_size / (1024 * 1024)
                    total_size += filesize
                    print(f'File Size in MegaBytes is {filesize}')
                    if total_size > self.max_mbs:
                        breaked = True
                        break
                    shutil.move(os.path.join(source_dir, file_name),
                                'datafolder/' + source_dir)
        if len(os.listdir('datafolder')) == 0:
            shutil.rmtree('datafolder')
            return False
        sleep(0.2)
        print("PACKING DATA\n")
        sleep(0.2)
        subprocess.call([sys.executable, 'xp3.py', 'datafolder', 'data.xp3',
                        '-mode', 'repack', '-e', 'neko_vol0_steam'])
        shutil.rmtree('datafolder')
        if total_size > self.max_mbs:
            zipfiles = ['data.xp3']
            zipfileswopath = ['data.xp3']
            if isinstance(self.uncoded, str):
                zipfiles.append(self.uncoded)
                zipfileswopath.append(os.path.basename(self.uncoded))
            if isinstance(self.uncoded, list):
                zipfiles.extend(self.uncoded)
                zipfileswopath.extend([os.path.basename(i)
                                      for i in self.uncoded])
        else:
            zipfiles = ['data.xp3']
            zipfileswopath = ['data.xp3']
            folders = []
            for i in range(0, len(folders)):
                for path, directories, files in os.walk(folders[i]):
                    for file in files:
                        file_name = os.path.join(path, file)
                        zipfiles.append(file_name)
                        zipfileswopath.append(file)
        with zipfile.ZipFile(cachename, mode='w', compresslevel=5) as zip:
            zip_kb_old = 0
            zipfilesnumber = len(zipfiles)
            bar = tqdm(range(0, len(zipfiles)),
                       desc="Packing ")
            for i in bar:
                zip.write(zipfiles[i])
                filesize = sum(
                    [zinfo.file_size for zinfo in zip.filelist])
                sleep(0.02)
                tqdm.write(zipfileswopath[i] + "(" + str(os.path.getsize(
                    zipfiles[i])) + " KB) -> " + str(round(filesize - zip_kb_old, 2)) + " KB")
                zip_kb_old = filesize
                os.remove(zipfiles[i])
                if i == len(zipfiles)-1:
                    tqdm.write("\n")
            filesize = sum(
                [zinfo.file_size for zinfo in zip.filelist])
            print("\nPacked data have > " +
                  str(filesize) + " KB")
            zip.close()
        return breaked
