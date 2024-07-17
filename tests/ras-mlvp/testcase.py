import sys
sys.path.append('../../out/picker_out_RAS')

from env import *
from UT_RAS import DUTRAS

async def test_case1(ras_master):
    for i in range(10):
        await ras_master.put_s2(FullPredictItem())
        await ras_master.put_s3(FullPredictItem())
        await ras_master.pipeline_ctrl(1, 1, 1, 1, 0, 0)


if __name__ == "__main__":
    ras = DUTRAS()
    ras.init_clock("clock")
    # mlvp.setup_logging(log_level=mlvp.logger.ERROR)
    mlvp.run(top_test(ras, [test_case1]))
    ras.finalize()
