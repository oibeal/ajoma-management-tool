from abc import ABC, abstractmethod
from datetime import datetime

class AbstractFile(ABC):

    __DATE_FORMAT = '%y-%m-%d %H:%M:%S'
    __DATE_POS = (1, 0) # (col, row from date in data frame)

    def __init__(self, path: str, df):
        self.__path = path
        date = df[self.__DATE_POS[0]].iloc[self.__DATE_POS[1]]
        if not isinstance(date, datetime):
            date = None

        self.__date = date


    def getYear(self) -> int:
        if (self.__date == None):
            return None

        return self.__date.year
