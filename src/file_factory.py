from abstract_file import AbstractFile
import pandas as pd
from bill import Bill
from estimate import Estimate
import pathlib
import constants as const

class FileFactory:

    __FILE_TYPE_POS = (0, 1) # (col, row from file type in data frame)

    def create(self, path: str) -> AbstractFile:
        df = self.__read_excel(path)
        file_type = self.__get_file_type(df[self.__FILE_TYPE_POS[0]].iloc[self.__FILE_TYPE_POS[1]])

        if (file_type == const.TYPE_BILL):
            return Bill(path, df)
        
        return Estimate(path, df)

    def __get_file_type(self, type: str) -> int:
        if (type == "FAC Nº"):
            return const.TYPE_BILL
        
        return const.TYPE_ESTIMATE

    def __read_excel(self, path: str):
        file_extension = pathlib.Path(path).suffix

        if file_extension == '.xlsx':
            df = pd.read_excel(path, header=None, skiprows=21, usecols="A,B,F,G", engine='openpyxl')
        elif file_extension == '.xls':
            df = pd.read_excel(path, header=None, skiprows=21, usecols="A,B,F,G")
        else:
            raise Exception('Invalid file: %s', path)

        return df