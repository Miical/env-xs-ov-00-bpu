import mlvp
import copy
from mlvp import Port, Component
from .transaction import FullPredictItem

class RASStack:
    def __init__(self):
        super().__init__()

        self.stack = []

    def push(self, target):
        self.stack.append(target)

    def pop(self):
        return self.stack.pop()

class RASModel(Component):
    def __init__(self):
        super().__init__()

        self.s2_port = Port(max_size=-1)
        self.s3_port = Port(max_size=-1)
        self.pipe_ctrl_port = Port()

        self.s2_out_port = Port()
        self.s3_out_port = Port()

        self.stack = RASStack()

    def process_full_pred(self, s2_full_pred: FullPredictItem, stack_top):
        s2_full_pred = copy.deepcopy(s2_full_pred)
        if s2_full_pred.second_slot.is_ret:
            s2_full_pred.second_slot.jalr_target = stack_top
        if s2_full_pred.second_slot.is_jalr:
            s2_full_pred.second_slot.target = s2_full_pred.second_slot.jalr_target
        return s2_full_pred

    async def main(self):
        last_cycle_s2_out = None
        while True:
            pipe_info = await self.pipe_ctrl_port.get()
            if pipe_info["reset"]:
                continue

            if pipe_info["fire"][2]:
                s2_full_pred = await self.s2_port.get()
                if s2_full_pred.call_taken():
                    self.stack.push(s2_full_pred.fall_through_addr + 2 * s2_full_pred.second_slot.rvi_call)
                    s2_out = self.process_full_pred(s2_full_pred, 0)
                elif s2_full_pred.ret_taken():
                    s2_out = self.process_full_pred(s2_full_pred, self.stack.pop())
                else:
                    s2_out = self.process_full_pred(s2_full_pred, 0)

                last_cycle_s2_out = s2_out
                await self.s2_out_port.put(s2_out)

            if pipe_info["fire"][3]:
                s3_full_pred = await self.s3_port.get()
                await self.s3_out_port.put(last_cycle_s2_out)
