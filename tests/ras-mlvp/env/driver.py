from mlvp import Driver
from .transaction import *
from .ras_bundle import *

class FullPredictDriver(Driver):
    async def driver_method(self, req: FullPredictItem):
        self.bundle.br_taken_mask_0.value = req.first_slot.taken
        self.bundle.slot_valids_0.value = req.first_slot.valid
        self.bundle.targets_0.value = req.first_slot.target
        self.bundle.offsets_0.value = req.first_slot.offset
        self.bundle.br_taken_mask_1.value = req.second_slot.taken
        self.bundle.slot_valids_1.value = req.second_slot.valid
        self.bundle.targets_1.value = req.second_slot.target
        self.bundle.offsets_1.value = req.second_slot.offset
        self.bundle.jalr_target.value = req.second_slot.jalr_target
        self.bundle.fallThroughAddr.value = req.fall_through_addr
        self.bundle.fallThroughErr.value = req.fall_through_err
        self.bundle.last_may_be_rvi_call.value = req.second_slot.rvi_call
        self.bundle.is_jalr.value = req.second_slot.is_jalr
        self.bundle.is_call.value = req.second_slot.is_call
        self.bundle.is_ret.value = req.second_slot.is_ret
        self.bundle.is_br_sharing.value = req.second_slot.is_br_sharing
        self.bundle.hit.value = req.hit

        await self.bundle.step()

class PipeCtrlDriver(Driver):
    async def driver_method(self, req: FullPredictItem):
        if req is not None:
            fire = req["fire"]
            redirect = req["redirect"]
            reset = req["reset"]

            if reset:
                self.bundle.set_all(0)
                self.bundle.reset.value = 1
                await self.bundle.step()
                self.bundle.reset.value = 0
            else:
                self.bundle.s0_fire.set_all(fire[0])
                self.bundle.s1_fire.set_all(fire[1])
                self.bundle.s2_fire.set_all(fire[2])
                self.bundle.s3_fire.set_all(fire[3])
                self.bundle.s3_redirect.set_all(redirect[1])
            self.bundle.io_ctrl_ras_enable.value = 1

        await self.bundle.step()
