from abstract_file import AbstractFile

class Bill(AbstractFile):

    __BILL_ID_POS = (1, 1) # (col, row from bill id in data frame)

    def __init__(self, path: str, df) -> AbstractFile:
        super().__init__(path, df)
        self.__id = df[self.__BILL_ID_POS[0]].iloc[self.__BILL_ID_POS[1]]
