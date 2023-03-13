import os
from tqdm import tqdm


class nhentai:
    def __init__(self, id: int, start: int = 0, end: int = -1) -> None:
        self.id = str(id)
        self.start = start
        self.end = end

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
            if total == 0:
                return False
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

    def get_imgs(self, name: str):
        os.mkdir(name)
        if self.end == -1:
            counter: int = 0
            while True:
                counter += 1
                if not nhentai.download('https://cdn.nhentai.xxx/g/' + str(self.id) + '/' + str(counter) + '.jpg', name + '/' + str(counter) + '.jpg'):
                    break
        else:
            counter: int = 0
            while counter != self.end:
                counter += 1
                if not nhentai.download('https://cdn.nhentai.xxx/g/' + str(self.id) + '/' + str(counter) + '.jpg', name + '/' + str(counter) + '.jpg'):
                    break
