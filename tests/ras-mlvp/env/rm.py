import mlvp
from mlvp import Port, Component

class RASModel(Component):
    def __init__(self):
        super().__init__()

        self.s2_port = Port()
        self.s3_port = Port()
        self.pipe_ctrl_port = Port()

        self.s2_out_port = Port()
        self.s3_out_port = Port()

    async def main(self):
        while True:
            pipe_info = await self.pipe_ctrl_port.get()

            if not self.s2_port.empty():
                s2_info = await self.s2_port.get()
                print("get s2 info: ", s2_info)
                await self.s2_out_port.put(s2_info)

            if not self.s3_port.empty():
                s3_info = await self.s3_port.get()
                print("get s3 info: ", s3_info)
                await self.s3_out_port.put(s3_info)



