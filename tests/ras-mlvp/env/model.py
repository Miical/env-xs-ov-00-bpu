import copy
from mlvp import Model, DriverMethod, MonitorMethod
from .config import *
from .transaction import *


class RASSpecStack:
    def __init__(self):
        self.stack = [0] * SPEC_MAX_SIZE
        self.nos = [0] * SPEC_MAX_SIZE    # index of the previous element

        self.bos = RASPtr()  # bottom of stack
        self.tosr = RASPtr() # top of stack
        self.tosw = RASPtr() # memory allocation

    def push(self, target):
        self.nos[self.tosw.value] = self.tosr.value
        self.tosr.value = self.tosw.value
        self.tosw.inc()
        self.stack[self.tosr.value] = target

    def pop(self):
        value = self.stack[self.tosr.value]
        self.tosr.value = self.nos[self.tosr.value]
        return value

    def clear(self):
        self.tosr.value = 31
        self.tosr.flag = None
        self.tosw.value = 0
        self.tosw.flag = None
        self.bos.value = 0
        self.bos.flag = None
        for i in range(SPEC_MAX_SIZE):
            self.stack[i] = 0
            self.nos[i] = 0


class RASModel(Model):
    def __init__(self):
        super().__init__()

        self.put_s2 = DriverMethod()
        self.put_s3 = DriverMethod()
        self.pipeline_ctrl = DriverMethod()

        self.monitor_s2 = MonitorMethod()
        self.monitor_s3 = MonitorMethod()
        self.monitor_meta = MonitorMethod()

        self.stack = RASSpecStack()

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
        s2_out_queue = []
        while True:
            pipe_info = await self.pipeline_ctrl()

            if pipe_info["s2_fire"]:
                s2_meta = RASMeta()
                s2_meta.tosw = copy.deepcopy(self.stack.tosw)
                s2_meta.tosr = copy.deepcopy(self.stack.tosr)
                s2_meta.nos = RASPtr(None)

                s2_full_pred = await self.put_s2()
                if s2_full_pred.call_taken():
                    self.stack.push(s2_full_pred.fall_through_addr + 2 * s2_full_pred.second_slot.rvi_call)
                    s2_out = self.process_full_pred(s2_full_pred, 0)
                elif s2_full_pred.ret_taken():
                    s2_out = self.process_full_pred(s2_full_pred, self.stack.pop())
                else:
                    s2_out = self.process_full_pred(s2_full_pred, 0)

                s2_out_queue.append([s2_out, s2_meta])
                await self.monitor_s2(s2_out)

            if pipe_info["s3_fire"]:
                s2_out, s2_meta = s2_out_queue.pop(0)

                s3_full_pred = await self.put_s3()
                await self.monitor_s3.put(s2_out)
                await self.monitor_meta.put(s2_meta)
