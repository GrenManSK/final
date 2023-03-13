import zipfile
import os
from tqdm import tqdm
import shutil


def download_file(url: str, fname: str, chunk_size: int = 1024) -> bool:
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


class download:
    def __init__(self, url: str):
        self.url = url
        self.name = 'new.zip'

    def download(self):
        directory_before = os.listdir()
        download_file(self.url, self.name)
        with zipfile.ZipFile(self.name, mode='r') as zip:
            for member in tqdm(iterable=zip.namelist(), total=len(zip.namelist()), desc='Extracting '):
                try:
                    zip.extract(member)
                    tqdm.write(
                        f"{os.path.basename(member)}(" + str(os.path.getsize(member)) + "KB)")
                except zipfile.error as e:
                    pass
        os.remove(self.name)
        directory_after = os.listdir()
        self.directory = []
        for i in directory_after:
            if i in directory_before:
                continue
            self.directory = i
        print(self.directory)
        return self

    def extract(self, destionation = './'):

        source_dir = f'{self.directory}/'
        target_dir = destionation
        file_names = os.listdir(source_dir)
        for file_name in file_names:
            try:
                shutil.move(os.path.join(source_dir, file_name), target_dir)
            except shutil.Error:
                pass
        self.target_dir = target_dir
        shutil.rmtree(source_dir)
        return self

    def remove_info(self):
        file_names = os.listdir(self.target_dir)
        for file_name in file_names:
            if file_name in ["README.md", 'requirements.txt']:
                try:
                    os.remove(file_name)
                except FileNotFoundError:
                    pass
