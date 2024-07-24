import mlvp
from mlvp import Component
from mlvp import Model, DriverMethod, MonitorMethod

class RASModel(Model):
    def __init__(self):
        super().__init__()

        self.put_s2 = DriverMethod()
        self.put_s3 = DriverMethod()
        self.monitor_s2 = MonitorMethod()

    async def main(self):
        while True:
            item = await self.put_s2()
            print("Model get s2 put", item)
            await self.monitor_s2(item)

