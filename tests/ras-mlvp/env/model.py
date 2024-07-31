import copy
from mlvp import Model, DriverMethod, MonitorMethod
from .config import *
from .transaction import *

class RASSpecStack:
    def __init__(self):
        self.stack = [0] * SPEC_MAX_SIZE
        self.nos = [0] * SPEC_MAX_SIZE    # index of the previous element

        self.ssp = RASPtr(max_size=COMMIT_MAX_SIZE) # commit stack pointer
        self.bos = RASPtr()                         # bottom of stack
        self.tosr = RASPtr()                        # top of stack
        self.tosw = RASPtr()                        # memory allocation

    def push(self, target):
        if self.stack[self.tosr.value] != target:
            self.ssp.inc()
        self.nos[self.tosw.value] = self.tosr.value
        self.tosr.value = self.tosw.value
        self.tosw.inc()
        self.stack[self.tosr.value] = target

    def pop(self):
        self.ssp.dec()
        value = self.stack[self.tosr.value]
        self.tosr.value = self.nos[self.tosr.value]
        return value

    def clear(self):
        self.ssp.value = 0
        self.tosr.value = 31
        self.tosr.flag = None
        self.tosw.value = 0
        self.tosw.flag = None
        self.bos.value = 0
        self.bos.flag = None
        for i in range(SPEC_MAX_SIZE):
            self.stack[i] = 0
            self.nos[i] = 0

class RASCommitStack:
    def __init__(self):
        self.stack = [{"addr": 0, "counter": 0}] * COMMIT_MAX_SIZE
        self.nsp = 0 # commit stack pointer

    def top(self):
        return self.stack[self.nsp]

    def push(self, target, meta_ssp):
        if self.top()["counter"] < MAX_COUNTER and self.top()["addr"] == target:
            self.top()["counter"] += 1
            self.nsp = meta_ssp
        else:
            self.nsp = meta_ssp + 1
            self.stack[self.nsp]["addr"] = target
            self.stack[self.nsp]["counter"] = 0

    def pop(self):
        ...

    def clear(self):
        self.nsp = 0
        for i in range(COMMIT_MAX_SIZE):
            self.stack[i] = {"addr": 0, "counter": 0}

class RASStack:
    def __init__(self):
        self.spec = RASSpecStack()
        self.commit = RASCommitStack()

    def push(self, target):
        self.spec.push(target)

    def pop(self):
        return self.spec.pop()

    def update(self, req: UpdateItem):
        if req.is_call_taken():
            push_addr = self.spec.stack[req.meta.tosw.value]
            self.spec.bos.value = req.meta.tosw.value
            self.commit.push(push_addr, req.meta.ssp)
        elif req.is_ret_taken():
            ...

    def clear(self):
        self.spec.clear()
        self.commit.clear()



class RASModel(Model):
    def __init__(self):
        super().__init__()

        self.put_s2 = DriverMethod()
        self.put_s3 = DriverMethod()
        self.pipeline_ctrl = DriverMethod()

        self.monitor_s2 = MonitorMethod()
        self.monitor_s3 = MonitorMethod()
        self.monitor_meta = MonitorMethod()

        self.stack = RASStack()

    def process_full_pred(self, s2_full_pred: FullPredictItem, stack_top):
        s2_full_pred = copy.deepcopy(s2_full_pred)
        if s2_full_pred.second_slot.is_ret:
            s2_full_pred.second_slot.jalr_target = stack_top
        if s2_full_pred.second_slot.is_jalr:
            s2_full_pred.second_slot.target = s2_full_pred.second_slot.jalr_target
        return s2_full_pred

    def update(self, req: UpdateItem):
        self.stack.update(req)

    def reset(self, step=None):
        self.stack.clear()

    async def main(self):
        s2_out_queue = []
        while True:
            pipe_info = await self.pipeline_ctrl()

            if pipe_info["s2_fire"]:
                s2_meta = RASMeta()
                s2_meta.tosw = copy.deepcopy(self.stack.spec.tosw)
                s2_meta.tosr = copy.deepcopy(self.stack.spec.tosr)
                s2_meta.ssp = self.stack.spec.ssp.value
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
