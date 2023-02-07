import sys
import os
from pathlib import Path
from file_factory import FileFactory
from bill import Bill
from estimate import Estimate
from tqdm import tqdm
import constants as const

class Manager:
    """
    Manager class
    """

    __SKIP_FILES = ('FACTURA.xlsx', 'PRESUPUESTO.xlsx')

    __BILL_FOLDER_NAME = 'Facturas'
    __ESTIMATE_FOLDER_NAME = 'Presupuestos'

    def __init__(self, source_path: str):
        self.__file_factory = FileFactory()
        self.__source_path = source_path
        self.__estimates = [] # presupuestos
        self.__bills = [] # facturas

        self.__load()

    def __load(self):
        file_list = list(Path(self.__source_path).rglob( '*.xls*' ))
        num_files = len(file_list)

        for p in tqdm(Path(self.__source_path).rglob( '*.xls*' ), desc="Loading...", total=num_files):
            basename = os.path.basename(p)
            if (basename not in self.__SKIP_FILES):
                try:
                    file = self.__file_factory.create(p)
                except Exception as error:
                    # print('\n'+repr(error))
                    continue

                if isinstance(file, Bill):
                    self.__add_bill(file)
                else:
                    self.__add_estimate(file)

    
    def __add_bill(self, bill: Bill):
        self.__bills.append(bill)

    def __add_estimate(self, estimate: Estimate):
        self.__estimates.append(estimate)

    def organize_files(self):
        self.__organize_by_type(const.TYPE_BILL)
        self.__organize_by_type(const.TYPE_ESTIMATE)

    def __organize_by_type(self, f_type: int):
        """
        Organizes the files inside the source path
        Path
        |_Bills or Estimates
            |_2020
                |_file1.xlsx\n
                |_file2.xlsx\n
                ...
            |_2021
            ...

        @var int type type of file that will be organized. 
        - 0 => bills
        - 1 => estimates
        """

        root_path = self.__source_path
        file_folder = self.__BILL_FOLDER_NAME if f_type == const.TYPE_BILL else self.__ESTIMATE_FOLDER_NAME
        file_folder_path = root_path + "/" + file_folder

        file_list = self.__bills if f_type == const.TYPE_BILL else self.__estimates

        for f in file_list:
            file_path = f.getPath()
            file_basename = os.path.basename(file_path)
            file_date = f.getDate()

            year_folder = file_folder_path + "/" + str(file_date.year)
            self.__generate_folder(year_folder)

            destination = year_folder + "/" + file_basename

            if not os.path.samefile(file_path, destination):
                
                if os.path.exists(destination):
                    destination = year_folder + "/" + file_date.strftime('%Y%m%d') + "_" + file_basename

                os.rename(file_path, destination)
                f.setPath(destination)


    def __generate_folder(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)



# Main behaviour
if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) < 1:
        sys.exit('No path included')

    sp = args[0]
    manager = Manager(sp)
    manager.organize_files()