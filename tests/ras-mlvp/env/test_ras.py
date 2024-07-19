import mlvp
from mlvp import ClockCycles

from .ras_bundle import *
from .driver import *
from .agent import *
from .transaction import *
from .rm import *


async def top_test(ras, tests):
    mlvp.create_task(mlvp.start_clock(ras))

    ras_bundle = RASBundle().set_name("ras").bind(ras)
    ras_bundle.set_all(0)
    # print(Bundle.detect_unconnected_signals(ras))

    ras_master = RASMasterAgent(ras_bundle)
    ras_slave  = RASSlaveAgent(ras_bundle)
    ras_rm = RASModel()

    ras_rm.s2_port.connect(ras_master.s2_driver_port)
    ras_rm.s3_port.connect(ras_master.s3_driver_port)
    ras_rm.pipe_ctrl_port.connect(ras_master.pipectrl_port)

    mlvp.add_comparison(ras_slave.s2_full_pred_monitor.port, ras_rm.s2_out_port, match_detail=True)
    mlvp.add_comparison(ras_slave.s3_full_pred_monitor.port, ras_rm.s3_out_port, match_detail=True)


    for test in tests:
        await test(ras_master)



