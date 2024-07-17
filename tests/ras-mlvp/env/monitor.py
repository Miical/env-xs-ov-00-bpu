import mlvp
from mlvp import Component, Port, Value
from .transaction import *

class FullPredictMonitor(Component):
    def __init__(self, bundle, fire):
        super().__init__()

        self.port = Port()
        self.bundle = bundle
        self.fire_signal = fire

    async def main(self):
        while True:
            await Value(self.fire_signal, 1)

            item = FullPredictItem()
            item.first_slot.taken = self.bundle.br_taken_mask_0.value
            item.first_slot.valid = self.bundle.slot_valids_0.value
            item.first_slot.target = self.bundle.targets_0.value
            item.first_slot.offset = self.bundle.offsets_0.value
            item.second_slot.taken = self.bundle.br_taken_mask_1.value
            item.second_slot.valid = self.bundle.slot_valids_1.value
            item.second_slot.target = self.bundle.targets_1.value
            item.second_slot.offset = self.bundle.offsets_1.value
            item.second_slot.jalr_target = self.bundle.jalr_target.value
            item.second_slot.rvi_call = self.bundle.last_may_be_rvi_call.value
            item.second_slot.is_jalr = self.bundle.is_jalr.value
            item.second_slot.is_call = self.bundle.is_call.value
            item.second_slot.is_ret = self.bundle.is_ret.value
            item.second_slot.is_br_sharing = self.bundle.is_br_sharing.value
            item.fall_through_addr = self.bundle.fallThroughAddr.value
            item.fall_through_err = self.bundle.fallThroughErr.value
            item.hit = self.bundle.hit.value

            await self.port.put(item)
            await self.bundle.step()

