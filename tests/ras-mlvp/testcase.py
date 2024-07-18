import sys
sys.path.append('../../out/picker_out_RAS')

from env import *
from generator import FullPredGenerator
from UT_RAS import DUTRAS

async def test_case1(ras_master):
    fullpred = FullPredGenerator()
    await ras_master.reset()

    await ras_master.pipeline_ctrl(1, 1, 1, 1, 0, 0)
    await ras_master.put_s2(fullpred.random_call())
    await ras_master.pipeline_ctrl(1, 1, 1, 1, 0, 0)
    await ras_master.put_s2(fullpred.random_call())
    await ras_master.pipeline_ctrl(1, 1, 1, 1, 0, 0)
    await ras_master.put_s2(fullpred.random_ret())
    await ras_master.pipeline_ctrl(1, 1, 1, 1, 0, 0)
    await ras_master.put_s2(fullpred.random_ret())
    await ras_master.pipeline_ctrl(1, 1, 1, 1, 0, 0)
    await ras_master.put_s2(fullpred.random_call())


async def test_case2(ras_master):
    fullpred = FullPredGenerator()
    await ras_master.reset()

    await ras_master.pipeline_ctrl(1, 1, 1, 1, 0, 0)
    await ras_master.put_s2(fullpred.random_call())


if __name__ == "__main__":
    ras = DUTRAS()
    ras.init_clock("clock")
    mlvp.setup_logging(log_level=mlvp.logger.INFO)
    mlvp.run(top_test(ras, [test_case1, test_case2]))
    ras.finalize()
