import mlvp

class FirstSlot:
    def __init__(self):
        self.valid = 1
        self.offset = 2
        self.target = 3
        self.taken = 1

    def is_taken(self):
        """If the instruction in the slot is taken."""

        return self.valid and self.taken

class SecondSlot(FirstSlot):
    def __init__(self):
        super().__init__()

        self.is_jalr = 0
        self.is_call = 0
        self.is_ret = 0
        self.is_br_sharing = 0
        self.jalr_target = 0
        self.rvi_call = 0

    def is_taken(self):
        """If the instruction in the slot is taken."""

        return self.valid and (
            (self.is_br_sharing and self.taken)
            or not self.is_br_sharing
        )

class FullPredictItem:
    def __init__(self):
        self.hit = 0
        self.fall_through_addr = 0
        self.fall_through_err = 0
        self.first_slot = FirstSlot()
        self.second_slot = SecondSlot()

    def will_jump(self):
        """This predict Item will trigger unconditional jump instructions in SecondSlot."""

        return not self.first_slot.is_taken and self.second_slot.is_taken() and not self.second_slot.is_br_sharing

    def call_taken(self):
        """This predict Item will trigger a call instruction."""

        return self.will_jump() and self.second_slot.is_call

    def ret_taken(self):
        """This predict Item will trigger a return instruction."""

        return self.will_jump() and self.second_slot.is_ret

    def jalr_taken(self):
        """This predict Item will trigger a jalr instruction."""

        return self.will_jump() and self.second_slot.is_jalr

