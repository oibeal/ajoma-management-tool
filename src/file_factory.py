from abstract_file import AbstractFile
import pandas as pd
from bill import Bill
from estimate import Estimate
import pathlib

class FileFactory:

    __TYPE_BILL = 0
    __TYPE_ESTIMATE = 1

    __FILE_TYPE_POS = (1, 0) # (col, row from file type in data frame)

    def create(self, path: str) -> AbstractFile:
        df = self.__read_excel(path)
        file_type = self.__get_file_type(df[self.__FILE_TYPE_POS[0]].iloc[self.__FILE_TYPE_POS[1]])

        if (file_type == self.__TYPE_BILL):
            return Bill(path, df)
        
        return Estimate(path, df)

    def __get_file_type(self, type: str) -> int:
        if (type == "FACTURA"):
            return self.__TYPE_BILL
        
        return self.__TYPE_ESTIMATE

    def __read_excel(self, path: str):
        file_extension = pathlib.Path(path).suffix

        if file_extension == '.xlsx':
            df = pd.read_excel(path, header=None, skiprows=21, usecols="A,B,F,G", engine='openpyxl')
        elif file_extension == '.xls':
            df = pd.read_excel(path, header=None, skiprows=21, usecols="A,B,F,G")
        else:
            raise Exception('Invalid file: %s', path)

        return df