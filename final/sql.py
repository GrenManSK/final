"""SQL Server Commands"""


import mysql.connector
import time
from tqdm import tqdm
import os
from random import uniform


class SQLServer:
    def __init__(self, host: str, port: int, user=None, passwd=None, database=None, log: bool = False):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.log = log

    def connect(self):
        """
        The connect function connects to the database and returns a connection object.

        :param self: Reference the class object
        :return: The connection object
        """

        if self.log:
            print('CONNECTING ...', end='\r')
        if self.user != None:
            if not isinstance(self.user, str):
                raise ValueError("user must be a string")
        if self.passwd is not None:
            if not isinstance(self.passwd, str):
                raise ValueError("passwd must be a string")
        if self.database is not None:
            if not isinstance(self.database, str):
                raise ValueError("database must be a string")

        self.db = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )

        if self.log:
            print('Connecting DONE')
            print('APPOINTING CURSOR ...', end='\r')
        self.mycursor = self.db.cursor()
        if self.log:
            print('APPOINTING CURSOR DONE')
        return self.db

    def execute(self, command: str, log=None, info=True):
        """
        The execute function executes a command and prints out the result.
        It also returns the result as a pandas dataframe.

        :param self: Refer to the object instance
        :param command: str: Pass the sql command to be executed
        :param log: Enable logging
        :param info: Print out the time it took to execute the command
        :return: A pandas dataframe
        """
        while os.path.exists('RUNNING'):
            time.sleep(uniform(0.5, 1.5))
        try:
            # deepcode ignore MissingClose: <create file>
            open('RUNNING', 'x')
        except FileExistsError:
            SQLServer.execute(self, command=command, log=log, info=info)
            return None
        if log != None:
            if isinstance(log, bool):
                self.log = log
        if self.log or info:
            print(f'Executing command {command}')
        start = time.time()
        try:
            self.mycursor.execute(command)
        except mysql.connector.errors.ProgrammingError:
            os.remove('RUNNING')
            return None
        end = time.time()
        commandtime = end - start
        start = time.time()
        data = self.mycursor.fetchall()
        if self.log:
            if data is not None:
                for row in tqdm(iterable=data, total=len(data)):
                    tqdm.write(str(row))
        end = time.time()
        endtime = end-start
        if self.log or info:
            print(f'DONE in {commandtime} seconds')
            print(f'Printing DONE in {endtime} seconds')

        self.db.commit()
        os.remove('RUNNING')
        return data

    @staticmethod
    def to_str(thing, mode: int = 0) -> str:
        """
        The to_str function takes a list of lists and converts it into a string.
        The function is used to convert the data from the csv file into something that
        can be written to an SQL database. The function also removes any apostrophes or 
        quotation marks in order to prevent SQL injection attacks.

        :param thing: Pass in a list of lists
        :return: A string that is formatted for the insert statement
        """
        name: str = ''
        if thing == None:
            return 'NULL'
        if len(thing) == 0:
            name: str = 'None'
            return name
        if mode == 0:
            for i in tqdm(range(len(thing)), leave=False):
                temp: str = ''
                was_edited: bool = False
                for j in tqdm(range(len(thing[i])), leave=False):
                    was_edited: bool = False
                    if thing[i][j] == "'":
                        temp += "\\'"
                        was_edited: bool = True
                    elif thing[i][j] == '\"':
                        temp += '\\"'
                        was_edited: bool = True
                    else:
                        was_edited: bool = False
                        temp += str(thing[i][j])
                if not was_edited:
                    name += str(thing[i]+', ')
                elif was_edited:
                    name += str(temp+', ')
            name: str = name[0:-2]
        if mode == 1:
            temp: str = ''
            was_edited: bool = False
            for i in tqdm(range(len(thing)), leave=False):
                if thing[i] == "'":
                    temp += "\\'"
                    was_edited: bool = True
                elif thing[i] == '\"':
                    temp += '\\"'
                    was_edited: bool = True
                else:
                    was_edited: bool = False
                    temp += str(thing[i])
                if not was_edited:
                    name += str(thing[i])
                elif was_edited:
                    name += str(temp)
        return name
