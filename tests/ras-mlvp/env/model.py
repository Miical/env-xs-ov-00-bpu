import copy
from mlvp import Model, DriverMethod, MonitorMethod, Component
from .transaction import FullPredictItem

class RASStack:
    def __init__(self):
        super().__init__()

        self.stack = []

    def push(self, target):
        self.stack.append(target)

    def pop(self):
        return self.stack.pop()

    def clear(self):
        self.stack.clear()

class RASModel(Model):
    def __init__(self):
        super().__init__()

        self.put_s2 = DriverMethod()
        self.put_s3 = DriverMethod()
        self.pipeline_ctrl = DriverMethod()
        self.monitor_s2 = MonitorMethod()
        self.monitor_s3 = MonitorMethod()

        self.stack = RASStack()

    def process_full_pred(self, s2_full_pred: FullPredictItem, stack_top):
        s2_full_pred = copy.deepcopy(s2_full_pred)
        if s2_full_pred.second_slot.is_ret:
            s2_full_pred.second_slot.jalr_target = stack_top
        if s2_full_pred.second_slot.is_jalr:
            s2_full_pred.second_slot.target = s2_full_pred.second_slot.jalr_target
        return s2_full_pred

    def reset(self, step=None):
        self.stack.clear()

    async def main(self):
        last_cycle_s2_out = None
        while True:
            pipe_info = await self.pipeline_ctrl()

            if pipe_info["s2_fire"]:
                s2_full_pred = await self.put_s2()
                if s2_full_pred.call_taken():
                    self.stack.push(s2_full_pred.fall_through_addr + 2 * s2_full_pred.second_slot.rvi_call)
                    s2_out = self.process_full_pred(s2_full_pred, 0)
                elif s2_full_pred.ret_taken():
                    s2_out = self.process_full_pred(s2_full_pred, self.stack.pop())
                else:
                    s2_out = self.process_full_pred(s2_full_pred, 0)
                last_cycle_s2_out = s2_out
                await self.monitor_s2(s2_out)

            if pipe_info["s3_fire"]:
                s3_full_pred = await self.put_s3()
                await self.monitor_s3.put(last_cycle_s2_out)
