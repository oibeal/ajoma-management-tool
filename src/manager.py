import sys
import os
from pathlib import Path
from file_factory import FileFactory
from bill import Bill
from estimate import Estimate
from tqdm import tqdm

class Manager:
    """
    Manager class
    """

    __SKIP_FILES = ('FACTURA.xlsx', 'PRESUPUESTO.xlsx')

    def __init__(self, source_path: str):
        self.__file_factory = FileFactory()
        self.__source_path = source_path
        self.__estimates = [] # presupuestos
        self.__bills = [] # facturas

        self.__load()

    def __load(self):
        file_list = Path(self.__source_path).rglob( '*.xls*' )
        num_files = len(list(file_list))

        for p in tqdm(Path(self.__source_path).rglob( '*.xls*' ), desc="Loading...", total=num_files):
            basename = os.path.basename(p)
            if (basename not in self.__SKIP_FILES):
                try:
                    file = self.__file_factory.create(p)
                except Exception as error:
                    # print('\n'+repr(error))
                    continue

                if isinstance(file, Bill):
                    self.add_bill(file)
                else:
                    self.add_estimate(file)

    
    def add_bill(self, bill: Bill):
        self.__bills.append(bill)

    def add_estimate(self, estimate: Estimate):
        self.__estimates.append(estimate)



# Main behaviour
if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) < 1:
        sys.exit('No path included')

    sp = args[0]
    manager = Manager(sp)