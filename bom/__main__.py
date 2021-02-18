from src import SourceParser, BomTree
import sys

if __name__ == '__main__':
    sheet_file_path : str = sys.argv[-1]

    source_parser = SourceParser(source_file=sheet_file_path)

    for pack in source_parser.get_finished_goods_generator():
        item_name, item_gen = pack
        tree = BomTree(item_name)

        for row in item_gen:
            tree.add_node(row)

        tree.generate_bom()
