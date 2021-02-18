from typing import List
from .output_sheet import GenerateBomSheet


class BomNode(object):

    def __init__(self, name:str, quantity:float = 1, unit:str = 'Pc', **kwargs) -> None:
        self.item_name = name
        self.unit = unit
        self.quantity = quantity
        self.childs : List[BomNode] = []

    def add(self, node) -> None:
        self.childs.append(node)

    @property
    def has_child(self) -> bool:
        return bool(self.childs)

    def __repr__(self) -> str:
        return self.item_name
    
    def __str__(self) -> str:
        return '{} => {}'.format(self.item_name, self.childs)


class BomTree(GenerateBomSheet):

    def __init__(self, root_item) -> None:
        self.root : BomNode = BomNode(name=root_item)

    def add_node(self, row_data : dict) -> None:
        level, iter_node = row_data.get('level') - 1, self.root
        node = BomNode(name=row_data.pop('raw_material'), **row_data)

        while level:
            if iter_node.has_child:
                iter_node = iter_node.childs[-1]
            level = level - 1

        iter_node.add(node)

    def get_childs(self, node: BomNode, bom_childs:list) -> List:
        if node.has_child:
            bom_childs.append([node, node.childs])
            for child in node.childs:
                self.get_childs(child, bom_childs)
        return bom_childs

    def generate_bom(self):
        # get all the nodes for which bom can be generated
        tree_mapping = self.get_childs(self.root, [])

        self.open_workbook(self.root.item_name)

        for finished_item, raw_material in tree_mapping:
            self.set_finished_goods(finished_item)
            self.set_raw_material_list(raw_material)
            super().generate_bom()

        self.workbook.close()

    def __repr__(self) -> str:
        return str(self.root)
