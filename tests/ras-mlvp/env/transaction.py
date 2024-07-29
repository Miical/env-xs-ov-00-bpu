import mlvp
from .ras_bundle import FullPredictBundle

def comp_with_none(a, b):
    if a is None or b is None:
        return True
    return a == b

def hex_with_none(num):
    if num is None:
        return None
    return hex(num)

class FirstSlot:
    def __init__(self):
        self.valid = 1
        self.offset = 2
        self.target = 3
        self.taken = 1

    def is_taken(self):
        """If the instruction in the slot is taken."""

        return self.valid and self.taken

    def __str__(self):
        return f"FirstSlot(valid={self.valid}, offset={self.offset}, target={hex_with_none(self.target)}, taken={self.taken})"

    def __eq__(self, other):
        return comp_with_none(self.valid, other.valid) and \
               comp_with_none(self.offset, other.offset) and \
               comp_with_none(self.target, other.target) and \
               comp_with_none(self.taken, other.taken)

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

    def __str__(self):
        return f"SecondSlot(valid={self.valid}, offset={self.offset}, target={hex_with_none(self.target)}, taken={self.taken}, is_jalr={self.is_jalr}, is_call={self.is_call}, is_ret={self.is_ret}, is_br_sharing={self.is_br_sharing}, jalr_target={hex_with_none(self.jalr_target)}, rvi_call={self.rvi_call})"

    def __eq__(self, other):
        return super().__eq__(other) and \
               comp_with_none(self.is_jalr, other.is_jalr) and \
               comp_with_none(self.is_call, other.is_call) and \
               comp_with_none(self.is_ret, other.is_ret) and \
               comp_with_none(self.is_br_sharing, other.is_br_sharing) and \
               comp_with_none(self.jalr_target, other.jalr_target) and \
               comp_with_none(self.rvi_call, other.rvi_call)

class FullPredictItem:
    def __init__(self):
        self.hit = 0
        self.fall_through_addr = 0
        self.fall_through_err = 0
        self.first_slot = FirstSlot()
        self.second_slot = SecondSlot()

    def will_jump(self):
        """This predict Item will trigger unconditional jump instructions in SecondSlot."""

        return not self.first_slot.is_taken() and self.second_slot.is_taken() and not self.second_slot.is_br_sharing and self.hit

    def call_taken(self):
        """This predict Item will trigger a call instruction."""

        return self.will_jump() and self.second_slot.is_call

    def ret_taken(self):
        """This predict Item will trigger a return instruction."""

        return self.will_jump() and self.second_slot.is_ret

    def jalr_taken(self):
        """This predict Item will trigger a jalr instruction."""

        return self.will_jump() and self.second_slot.is_jalr

    def __str__(self):
        return f"FullPredictItem(hit={self.hit}, fall_through_addr={hex_with_none(self.fall_through_addr)}, fall_through_err={self.fall_through_err}, first_slot={self.first_slot}, second_slot={self.second_slot})"

    def __eq__(self, other):
        return comp_with_none(self.hit, other.hit) and \
               comp_with_none(self.fall_through_addr, other.fall_through_addr) and \
               comp_with_none(self.fall_through_err, other.fall_through_err) and \
               self.first_slot == other.first_slot and \
               self.second_slot == other.second_slot

    def __bundle_assign__(self, bundle: FullPredictBundle):
        bundle.br_taken_mask_0.value = self.first_slot.taken
        bundle.slot_valids_0.value = self.first_slot.valid
        bundle.targets_0.value = self.first_slot.target
        bundle.offsets_0.value = self.first_slot.offset
        bundle.br_taken_mask_1.value = self.second_slot.taken
        bundle.slot_valids_1.value = self.second_slot.valid
        bundle.targets_1.value = self.second_slot.target
        bundle.offsets_1.value = self.second_slot.offset
        bundle.jalr_target.value = self.second_slot.jalr_target
        bundle.fallThroughAddr.value = self.fall_through_addr
        bundle.fallThroughErr.value = self.fall_through_err
        bundle.last_may_be_rvi_call.value = self.second_slot.rvi_call
        bundle.is_jalr.value = self.second_slot.is_jalr
        bundle.is_call.value = self.second_slot.is_call
        bundle.is_ret.value = self.second_slot.is_ret
        bundle.is_br_sharing.value = self.second_slot.is_br_sharing
        bundle.hit.value = self.hit

    @classmethod
    def from_bundle(cls, bundle: FullPredictBundle):
        item = cls()
        item.first_slot.valid = bundle.slot_valids_0.value
        item.first_slot.offset = bundle.offsets_0.value
        item.first_slot.target = bundle.targets_0.value
        item.first_slot.taken = bundle.br_taken_mask_0.value
        item.second_slot.valid = bundle.slot_valids_1.value
        item.second_slot.offset = bundle.offsets_1.value
        item.second_slot.target = bundle.targets_1.value
        item.second_slot.taken = bundle.br_taken_mask_1.value
        item.second_slot.jalr_target = bundle.jalr_target.value
        item.fall_through_addr = bundle.fallThroughAddr.value
        item.fall_through_err = bundle.fallThroughErr.value
        item.second_slot.rvi_call = bundle.last_may_be_rvi_call.value
        item.second_slot.is_jalr = bundle.is_jalr.value
        item.second_slot.is_call = bundle.is_call.value
        item.second_slot.is_ret = bundle.is_ret.value
        item.second_slot.is_br_sharing = bundle.is_br_sharing.value
        item.hit = bundle.hit.value
        return item
