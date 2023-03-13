from tkinter import filedialog
import glob
import re
import os
import mal


def getEpisode(filename):
    """
    The getEpisode function searches for a string that matches the regular expression r'\b(?:e(?:p(?:isode)?)?|0x|S\d\d?
        E)?\s*?(\d{2,3})\b'. If it finds a match, it returns the first group of digits as an integer. Otherwise, it returns None.
    :param filename: Find the episode number in the filename
    :return: The episode number of the file
    """
    match = re.search(
        r'''\b(?:e(?:p(?:isode)?)?|0x|S\d\dE)?\s*?(\d{2,3})\b''', filename)
    if match:
        return match.group(1)


class rename:
    def __init__(self, input):
        """
        The __init__ function is called when an instance of the class is created.
        It initializes the attributes of the class , and sets up any variables that are needed to be used by other functions in this class.
        : param self: Reference the object itself
        : param input: Pass the path to the folder containing files that need to be renamed
        : return: The input and output folders
        """
        self.input = input
        output_folder = []
        output_folder_names = []
        output_names = []
        for item in (input_folder := glob.glob(self.input + '/*.*')):
            item = re.sub("\(.*?\)", "", item)
            item = re.sub("\[.*?\]", "", item)
            item = re.sub("\{.*?\}", "", item)
            output_folder.append(item)
            output_folder_names.append(os.path.split(item)[-1])
        print(output_folder)
        print(output_folder_names)
        folder_name = os.path.split(os.path.split(output_folder[0])[0])[-1]
        folder_name_parent = os.path.split(input_folder[0])[0]
        print(folder_name)
        print(folder_name_parent)
        anime_name = mal.AnimeSearch(folder_name).results[0].title
        print(anime_name)
        extensions = []
        for item in input_folder:
            extensions.append(item.split('.')[-1])
        for item in output_folder_names:
            print(episode_name := getEpisode(item))
            output_names.append([anime_name, episode_name])
        output_final = []
        for times, item in enumerate(output_names):
            output_final.append(folder_name_parent + '/' + folder_name +
                                ' - ' + str(item[1]) + '.' + extensions[times])
        print(output_final)
        for number in range(0, len(output_final)):
            print(input_folder[number] + ' => ' + output_final[number])
        self.input = input_folder
        self.output = output_final

    def rename(self):
        """
        The rename function takes a list of files and renames them.
        The function accepts two lists as arguments: the input list and output list.
        The input file names are used to rename the output files.
        : param self: Access the attributes and methods of the class in python
        : return: None
        """
        for number in range(0, len(self.output)):
            os.rename(self.input[number], self.output[number])


def main():
    """
    The main function of the program.
    : return: The anime object
    """
    input_folder = filedialog.askdirectory()
    anime = rename(input_folder)
    while True:
        vstup = input('Rename (Y/n) > ')
        if vstup in ['', 'y', 'Y']:
            anime.rename()
            break
        if vstup in ['n', 'N']:
            break
        else:
            continue


if __name__ == '__main__':
    main()
