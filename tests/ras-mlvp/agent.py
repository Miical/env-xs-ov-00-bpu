import mlvp
from driver import *


class RASMasterAgent:
    def __init__(self, ras_bundle):
        self.bundle = ras_bundle

        self.s2_driver_port = Port()
        self.s2_driver = [
            FullPredictDriver(ras_bundle.resp_in.in_full_pred_s2_0),
            FullPredictDriver(ras_bundle.resp_in.in_full_pred_s2_1),
            FullPredictDriver(ras_bundle.resp_in.in_full_pred_s2_2),
            FullPredictDriver(ras_bundle.resp_in.in_full_pred_s2_3)
        ]
        for i in range(4):
            self.s2_driver_port.connect(self.s2_driver[i].port)


        self.s3_driver_port = Port()
        self.s3_driver = [
            FullPredictDriver(ras_bundle.resp_in.in_full_pred_s3_0),
            FullPredictDriver(ras_bundle.resp_in.in_full_pred_s3_1),
            FullPredictDriver(ras_bundle.resp_in.in_full_pred_s3_2),
            FullPredictDriver(ras_bundle.resp_in.in_full_pred_s3_3)
        ]
        for i in range(4):
            self.s3_driver_port.connect(self.s3_driver[i].port)

        self.last_stage_ftb_driver = None

        self.pc_driver = None
        self.pipectrl_driver = PipeCtrlDriver(ras_bundle.control)

        self.update_driver = None
        self.redirect_driver = None

    async def pipeline_ctrl(self, s0_fire, s1_fire, s2_fire, s3_fire,
                            s2_redirect, s3_redirect):
        await self.ctrl_driver.put({
            "fire": [s0_fire, s1_fire, s2_fire, s3_fire],
            "redirect": [s2_redirect, s3_redirect]
        })

    async def put_s2(self, fullpreditem: FullPredictItem):
        await self.s2_driver_port.put(fullpreditem)

    async def put_s3(self, fullpreditem: FullPredictItem):
        await self.s3_driver_port.put(fullpreditem)

    async def step(self):
        await self.bundle.step()

