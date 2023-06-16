import sys
import os
import shutil
import glob


class download:
    def __init__(self, url: str):
        self.url = url
        self.caller = os.getcwd() + "/" + self.url.split("/")[-1].split(".")[0]

    def download(self, folder=""):
        """
        The download function downloads the zip file from the url, extracts it and returns a list of all files in the directory

        :param self: Access the class attributes and methods
        :return: The directory of the extracted files
        """
        if folder != "":
            self.caller = folder
        directory_before = os.listdir()
        os.system(f"git clone {self.url} {folder}")
        name = self.url.split("/")[-1].split(".")[0]
        os.system(f"cd {name}")
        directory_after = os.listdir()
        self.directory = []
        for i in directory_after:
            if i in directory_before:
                continue
            self.directory = i
        print(self.directory)
        return self

    def remove_info(self):
        """
        The remove_info function removes the README.md and requirements.txt files from the target directory.

        :param self: Represent the instance of the class
        :return: Nothing
        """
        file_names = os.listdir(self.caller + "\\")
        for file_name in file_names:
            if file_name in ["README.md", "requirements.txt", "LICENSE", ".gitignore"]:
                try:
                    os.remove(self.caller + "\\" + file_name)
                except FileNotFoundError:
                    pass
        return self

    def install(self):
        os.system(f"{sys.executable} -m pip install {self.caller}")
        return self

    def delete(self):
        for file in glob.glob(self.caller + "\\*", include_hidden=True):
            if file.split("\\")[-1] == ".git":
                continue
            if os.path.isdir(file):
                shutil.rmtree(file)
            else:
                os.remove(file)
