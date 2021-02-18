import os
import pandas as pd
from typing import Generator, List

class SourceParser(object):
    columns = ['Item Name', 'Level', 'Raw material', 'Quantity', 'Unit ']

    def validated_source_file(self) -> None:
        # file must exist & should have a .xlsx extension
        is_valid = os.path.isfile(self.file_path) and \
            self.file_path.split('.')[-1] == 'xlsx'
        
        if not is_valid:
            raise Exception('Provided path is not of a excel file')

    def __init__(self, source_file : str) -> None:
        self.file_path : str = source_file
        self.validated_source_file()
        self.df : pd.DataFrame = pd.read_excel(
            self.file_path, engine='openpyxl', 
            usecols=self.columns
        ).dropna()

    def get_finished_goods_generator(self) -> List[tuple]:
        """
            Returns a tuple containing the item name and generater
            to get all the rows belonging to that item
        """
        return [(item, self.filter_rows(item)) for item in self.df['Item Name'].unique()]

    def filter_rows(self, item_name : str) -> Generator:
        # filter out the rows based on item name
        filtered_rows = self.df.where(self.df['Item Name'] == item_name).dropna()
        for _, row in filtered_rows.iterrows():
            yield {
                'item_name': row['Item Name'],
                'level' : int(row['Level'].strip('.')),
                'raw_material': row['Raw material'],
                'quantity': float(row['Quantity']),
                'unit': row['Unit ']
            }
