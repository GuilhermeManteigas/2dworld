from block import Block


class Inventory:

    def __init__(self):
        self.inventory = []
        self.inventory_size = 5
        self.stack_size_limit = 100

    def add_block_to_inventory(self, block_id):
        if len(self.inventory) <= self.inventory_size:
            self.inventory.append([0, 0])
        for i in self.inventory:
            if i[0] == block_id or i[0] == 0:
                if i[1] < self.stack_size_limit:
                    i[1] += 1

