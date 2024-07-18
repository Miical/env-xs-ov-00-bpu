import mlvp
from mlvp import Port, Component

class RASModel(Component):
    def __init__(self):
        super().__init__()

        self.s2_port = Port(max_size=-1)
        self.s3_port = Port(max_size=-1)
        self.pipe_ctrl_port = Port()

        self.s2_out_port = Port()
        self.s3_out_port = Port()

    async def main(self):
        while True:
            pipe_info = await self.pipe_ctrl_port.get()


            s2_info = await self.s2_port.get()
            print(f"RM: {hex(s2_info.fall_through_addr)}")
            await self.s2_out_port.put(s2_info)

            # if not self.s3_port.empty():
            #     s3_info = await self.s3_port.get()
            #     print("get s3 info")
            #     await self.s3_out_port.put(s3_info)

