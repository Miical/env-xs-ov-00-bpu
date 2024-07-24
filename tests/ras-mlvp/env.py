import mlvp
import functools
from transaction import *
from ras_bundle import *
from mlvp import Env, driver_method, monitor_method




class DUTEnv(Env):
    def __init__(self, bundle: RASBundle):
        super().__init__(monitor_step=bundle.step)

        self.bundle = bundle
        self.in_s2 = bundle.resp_in.in_full_pred_s2_0
        self.out_s2 = bundle.out.full_pred_s2_3
        self.s2_fire = bundle.control.s2_fire

    @driver_method()
    async def put_s2(self, fullpred: FullPredictItem):
        self.in_s2.assign(fullpred)
        print("assign done")
        await self.bundle.step()
        return fullpred

    @monitor_method()
    async def monitor_s2(self):
        return FullPredictItem.from_bundle(self.out_s2)


