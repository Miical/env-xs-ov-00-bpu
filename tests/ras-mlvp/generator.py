from random import randint
from env import FullPredictItem, FirstSlot, SecondSlot


class FullPredGenerator():
    def random_firstslot(self, item: FullPredictItem, taken):
        """Randomly generate a first slot."""

        item.first_slot.valid = randint(0, 1) if not taken else 1
        item.first_slot.offset = randint(0, 2**4-1)
        item.first_slot.target = randint(0, 2**41-1)

        if taken:
            item.first_slot.taken = 1
        elif item.first_slot.valid:
            item.first_slot.taken = 0
        else:
            item.first_slot.taken = randint(0, 1)
        return item


    def random_secondslot(self, item: FullPredictItem, is_ret=False, is_call=False):
        """Randomly generate a second slot."""

        assert not (is_ret and is_call), "Cannot be both ret and call."

        item.second_slot.valid = 1 if is_ret or is_call else randint(0, 1)
        item.second_slot.offset = randint(0, 2**4-1)
        item.second_slot.target = randint(0, 2**41-1)
        item.second_slot.is_jalr = randint(0, 1) if not is_ret else 1
        item.second_slot.is_call = int(is_call)
        item.second_slot.is_ret = int(is_ret)
        item.second_slot.is_br_sharing = 0 if is_ret or is_call else randint(0, 1)
        item.second_slot.jalr_target = randint(0, 2**41-1)
        item.second_slot.rvi_call = randint(0, 1)
        return item

    def random_item(self):
        """Randomly generate a item."""
        item = FullPredictItem()

        item.hit = randint(0, 1)
        item.fall_through_addr = randint(0, 2**41-1)
        item.fall_through_err = randint(0, 1)
        self.random_firstslot(item, taken=randint(0, 1))
        random_args = randint(0, 2)
        self.random_secondslot(item, is_call=random_args&1, is_ret=random_args>>1&1)
        return item

    def random_call(self, specific_addr=None):
        """Randomly generate a call."""

        item = self.random_item()
        self.random_firstslot(item, taken=False)
        self.random_secondslot(item, is_call=True)
        item.hit = 1
        if specific_addr is not None:
            item.fall_through_addr = specific_addr
        return item

    def random_ret(self):
        """Randomly generate a ret."""

        item = self.random_item()
        self.random_firstslot(item, taken=False)
        self.random_secondslot(item, is_ret=True)
        item.hit = 1
        return item

    def random_keep(self):
        """Randomly generate a keep."""

        item = self.random_item()
        self.random_secondslot(item)
        item.hit = 1
        return item
