from random import randint
from env import FullPredictItem, FirstSlot, SecondSlot


class FullPredGenerator(FullPredictItem):
    def random_firstslot(self, taken):
        """Randomly generate a first slot."""

        self.first_slot.valid = randint(0, 1) if not taken else 1
        self.first_slot.offset = randint(0, 2**4-1)
        self.first_slot.target = randint(0, 2**41-1)

        if taken:
            self.first_slot.taken = 1
        elif self.first_slot.valid:
            self.first_slot.taken = 0
        else:
            self.first_slot.taken = randint(0, 1)
        return self


    def random_secondslot(self, is_ret=False, is_call=False):
        """Randomly generate a second slot."""

        assert not (is_ret and is_call), "Cannot be both ret and call."

        self.second_slot.valid = randint(0, 1)
        self.second_slot.offset = randint(0, 2**4-1)
        self.second_slot.target = randint(0, 2**41-1)
        self.second_slot.is_jalr = randint(0, 1) if not is_ret else 1
        self.second_slot.is_call = int(is_call)
        self.second_slot.is_ret = int(is_ret)
        self.second_slot.is_br_sharing = 1 if is_ret or is_call else randint(0, 1)
        self.second_slot.jalr_target = randint(0, 2**41-1)
        self.second_slot.rvi_call = randint(0, 1)
        return self

    def random_item(self):
        """Randomly generate a item."""

        self.hit = randint(0, 1)
        self.fall_through_addr = randint(0, 2**41-1)
        self.fall_through_err = randint(0, 1)
        self.random_firstslot(taken=randint(0, 1))
        random_args = randint(0, 2)
        self.random_secondslot(is_call=random_args&1, is_ret=random_args>>1&1)
        return self

    def random_call(self):
        """Randomly generate a call."""

        self.random_item()
        self.random_firstslot(taken=False)
        self.random_secondslot(is_call=True)
        return self

    def random_ret(self):
        """Randomly generate a ret."""

        self.random_item()
        self.random_firstslot(taken=False)
        self.random_secondslot(is_ret=True)
        return self

    def random_keep(self):
        """Randomly generate a keep."""

        self.random_item()
        self.random_secondslot()
        return self
