import mlvp

class FirstSlot:
    def __init__(self):
        self.valid = 1
        self.offset = 2
        self.target = 3
        self.taken = 1

class SecondSlot(FirstSlot):
    def __init__(self):
        super().__init__()

        self.is_jalr = 0
        self.is_call = 0
        self.is_ret = 0
        self.is_br_sharing = 0
        self.jalr_target = 0
        self.rvi_call = 0

class FullPredictItem:
    def __init__(self):
        self.hit = 0
        self.fall_through_addr = 0
        self.fall_through_err = 0
        self.first_slot = FirstSlot()
        self.second_slot = SecondSlot()
