from abstract_file import AbstractFile

class Bill(AbstractFile):

    def __init__(self, path: str) -> AbstractFile:
        super().__init__(path)
        self.__id = 0
