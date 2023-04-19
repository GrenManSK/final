from tkinter import filedialog
import glob
import re
import os
import mal
import anitopy



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
            anime_name = anitopy.parse(item.split('\\')[-1])['anime_title']
            output_folder.append(item)
            output_folder_names.append(os.path.split(item)[-1])
        print(output_folder)
        print(output_folder_names)
        folder_name = os.path.split(os.path.split(output_folder[0])[0])[-1]
        folder_name_parent = os.path.split(input_folder[0])[0]
        print(folder_name)
        print(folder_name_parent)
        print(anime_name)
        extensions = []
        for item in input_folder:
            extensions.append(anitopy.parse(item)['file_extension'])
        resolution = []
        for item in input_folder:
            try:
                resolution.append(anitopy.parse(item)['video_resolution'])
            except KeyError:
                resolution.append('')
        season = []
        for item in input_folder:
            try:
                season.append(anitopy.parse(item)['anime_season'])
            except KeyError:
                season.append('1')
        anime_title = []
        for item in input_folder:
            try:
                anime_title.append(' - ' + anitopy.parse(item)['episode_title'])
            except KeyError:
                anime_title.append('')
        for times, item in enumerate(output_folder_names):
            print(episode_name := anitopy.parse(item)['episode_number'])
            output_names.append([anime_name, episode_name, f" (Season {season[times]})"])
        output_final = []
        for times, item in enumerate(output_names):
            output_final.append(folder_name_parent + '/' + anime_name + str(item[2]) +
                                ' - ' + str(item[1]) + anime_title[times] +  '.' + extensions[times])
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
