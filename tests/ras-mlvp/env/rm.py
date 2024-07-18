import mlvp
from mlvp import Port, Component
from .transaction import FullPredictItem

class RASModel(Component):
    def __init__(self):
        super().__init__()

        self.s2_port = Port(max_size=-1)
        self.s3_port = Port(max_size=-1)
        self.pipe_ctrl_port = Port()

        self.s2_out_port = Port()
        self.s3_out_port = Port()

    def process_s2(self, s2_full_pred: FullPredictItem):
        if s2_full_pred.second_slot.is_ret:
            s2_full_pred.second_slot.jalr_target = 0
        if s2_full_pred.second_slot.is_jalr:
            s2_full_pred.second_slot.target = s2_full_pred.second_slot.jalr_target
        return s2_full_pred

    async def main(self):
        while True:
            pipe_info = await self.pipe_ctrl_port.get()
            if pipe_info["reset"]:
                continue

            s2_full_pred = await self.s2_port.get()
            s2_out = self.process_s2(s2_full_pred)
            await self.s2_out_port.put(s2_out)



            # if not self.s3_port.empty():
            #     s3_info = await self.s3_port.get()
            #     print("get s3 info")
            #     await self.s3_out_port.put(s3_info)

