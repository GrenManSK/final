"""Code to string"""

from tqdm import tqdm


class c2s:
    def __init__(self, code_file: str, string_file: str):
        self.string_file = string_file
        self.code_file = code_file

    @staticmethod
    def to_str(thing) -> str:
        """
        The to_str function takes a list of lists and converts it into a string.
        The function is used to convert the data from the csv file into something that
        can be written to an SQL database. The function also removes any apostrophes or 
        quotation marks in order to prevent SQL injection attacks.

        :param thing: Pass in a list of lists
        :return: A string that is formatted for the insert statement
        """
        name: str = ''
        if thing is None:
            return 'NULL'
        if len(thing) == 0:
            name: str = 'None'
            return name
        temp: str = ''
        for i in tqdm(range(len(thing)), leave=False):
            if thing[i] == "'":
                temp += "\\'"
            elif thing[i] == '\"':
                temp += '\\"'
            elif thing[i] == '\n':
                temp += '\\n'
            else:
                temp += str(thing[i])
        name += str(temp)
        return name

    def start(self) -> str:
        full = ""
        with open(self.code_file, 'r') as code:
            if self.string_file is not None or not self.string_file in ['']:
                with open(self.string_file, 'w') as file:
                    for i in tqdm(fr := code.readlines()):
                        oneline = c2s.to_str(i)
                        file.write(oneline)
                        full += oneline
            else:
                for i in tqdm(fr := code.readlines()):
                    oneline = c2s.to_str(i)
                    full += oneline
        return full
