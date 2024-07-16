import mlvp
from mlvp import ClockCycles

import sys
sys.path.append('../../out/picker_out_RAS')
from UT_RAS import DUTRAS

from ras_bundle import *
from driver import *
from agent import *
from transaction import *



async def test_res(ras):
    mlvp.create_task(mlvp.start_clock(ras))
    #--------

    ras_bundle = RASBundle().set_name("ras").bind(ras)
    ras_bundle.set_write_mode_as_imme().set_all(0)

    print(Bundle.detect_unconnected_signals(ras))


    ras_master = RASMasterAgent(ras_bundle)
    await ras_master.put_s2(FullPredictItem())
    await ClockCycles(ras, 1)

    await ClockCycles(ras, 10)


if __name__ == "__main__":
    ras = DUTRAS()
    ras.init_clock("clock")
    # mlvp.setup_logging(log_level=mlvp.logger.ERROR)
    mlvp.run(test_res(ras))
    ras.finalize()

