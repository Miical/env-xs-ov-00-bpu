from .transaction import *
from .ras_bundle import *
from mlvp import Env, driver_method, monitor_method

class RASEnv(Env):
    def __init__(self, bundle: RASBundle):
        super().__init__(monitor_step=bundle.step)

        self.bundle = bundle
        self.s2_fire = bundle.control.s2_fire

        bundle.control.io_ctrl_ras_enable.value = 1


    @driver_method(match_func=True, imme_ret=False)
    async def reset(self, step=1):
        self.bundle.set_all(0)
        self.bundle.control.reset.value = 1
        self.bundle.control.io_ctrl_ras_enable.value = 1
        await self.bundle.step(step)
        self.bundle.control.reset.value = 0

    @driver_method()
    async def pipeline_ctrl(self, s0_fire, s1_fire, s2_fire, s3_fire, s2_redirect, s3_redirect):
        self.bundle.control.s0_fire.set_all(s0_fire)
        self.bundle.control.s1_fire.set_all(s1_fire)
        self.bundle.control.s2_fire.set_all(s2_fire)
        self.bundle.control.s3_fire.set_all(s3_fire)
        self.bundle.control.s3_redirect.set_all(s3_redirect)
        await self.bundle.step()

    @driver_method()
    async def put_s2(self, fullpred: FullPredictItem):
        self.bundle.resp_in.full_pred_s2_0.assign(fullpred)
        self.bundle.resp_in.full_pred_s2_1.assign(fullpred)
        self.bundle.resp_in.full_pred_s2_2.assign(fullpred)
        self.bundle.resp_in.full_pred_s2_3.assign(fullpred)
        await self.bundle.step()

    @driver_method()
    async def put_s3(self, fullpred: FullPredictItem):
        self.bundle.resp_in.full_pred_s3_0.assign(fullpred)
        self.bundle.resp_in.full_pred_s3_1.assign(fullpred)
        self.bundle.resp_in.full_pred_s3_2.assign(fullpred)
        self.bundle.resp_in.full_pred_s3_3.assign(fullpred)
        await self.bundle.step()

    @driver_method(match_func=True)
    async def update(self, req: UpdateItem):
        self.bundle.update.valid.value = 1
        self.bundle.update.assign(req)
        await self.bundle.step()
        self.bundle.update.valid.value = 0

    @monitor_method()
    async def monitor_s2(self):
        if self.s2_fire._1.value:
            return FullPredictItem.from_bundle(self.bundle.out.full_pred_s2_3)

    @monitor_method()
    async def monitor_s3(self):
        if self.bundle.control.s3_fire._2.value:
            return FullPredictItem.from_bundle(self.bundle.out.full_pred_s3_3)

    @monitor_method()
    async def monitor_meta(self):
        if self.bundle.control.s3_fire._2.value:
            return RASMeta.from_int(self.bundle.out.last_stage_meta.value)

    async def single_update(self, req: UpdateItem):
        await self.update(req)
        await self.pipeline_ctrl(0, 0, 0, 0, 0, 0)
        await self.drive_completed()

    async def s2_s3_same(self, fullpred: FullPredictItem):
        await self.pipeline_ctrl(0, 0, 1, 0, 0, 0)
        await self.put_s2(fullpred)
        await self.drive_completed()

        await self.pipeline_ctrl(0, 0, 0, 1, 0, 0)
        await self.put_s3(fullpred)
        await self.drive_completed()

        return await self.monitor_meta()
