from typing import List
import pandas as pd
import xlsxwriter

class GenerateBomSheet(object):
    finished_goods = None
    raw_material_list = None
    workbook = None

    def open_workbook(self, filename):
        self.workbook = xlsxwriter.Workbook('%s.xlsx' % filename)

    def set_finished_goods(self, finished_goods):
        self.finished_goods = finished_goods

    def set_raw_material_list(self, raw_material_list):
        self.raw_material_list = raw_material_list

    def get_finished_goods_data(self):
        return [
            [
                1, self.finished_goods.item_name, 
                self.finished_goods.quantity, self.finished_goods.unit
            ]
        ]

    def get_raw_materials_list_data(self):
        return [
            [index+1, rw.item_name, rw.quantity, rw.unit]
            for index, rw in enumerate(self.raw_material_list)
        ]

    def generate_bom(self):
        worksheet = self.workbook.add_worksheet(self.finished_goods.item_name)
        caption = 'Finished Good List'
        worksheet.write('A1', caption)

        get_options = lambda data: {
            'data': data, 
            'columns': [
                {'header': '#'}, {'header': 'Item Description'}, 
                {'header': 'Quantity'}, {'header': 'Unit'}
            ]}

        data = self.get_finished_goods_data()
        worksheet.add_table('A2:D3', get_options(data))
        worksheet.write('A4', 'End of FG')


        data = self.get_raw_materials_list_data()
        worksheet.write('A5', 'Raw Material List')
        footer = len(data) + 6 # starting from next line from caption
        worksheet.add_table('A6:D%d' % footer, get_options(data))
        worksheet.write('A{}'.format(footer+1), 'End of Rw')
