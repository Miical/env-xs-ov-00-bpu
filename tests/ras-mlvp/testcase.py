import sys
sys.path.append('../../out/picker_out_RAS')

from env import *
from generator import FullPredGenerator
from UT_RAS import DUTRAS

async def test_case1(ras_master):
    fullpred = FullPredGenerator()
    await ras_master.reset()

    for i in range(100):
        await ras_master.nochange_exec(fullpred.random_call(specific_addr=0x12345))
        await ras_master.nochange_exec(fullpred.random_ret())

    await ras_master.reset()


if __name__ == "__main__":
    ras = DUTRAS()
    ras.init_clock("clock")
    mlvp.setup_logging(log_level=mlvp.logger.INFO)
    mlvp.run(top_test(ras, [test_case1]))
    ras.finalize()
