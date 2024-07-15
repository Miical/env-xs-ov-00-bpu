import sys
import mlvp
sys.path.append('../../out/picker_out_RAS')

from UT_RAS import DUTRAS
from ras_bundle import *



def test_res():
    ras = DUTRAS()
    ras.init_clock("clock")
    #--------

    ras_bundle = RASBundle().set_name("ras").bind(ras)

    print("".join([f"{s}\n" for s in mlvp.Bundle.detect_unconnected_signals(ras)]))








    #----------
    ras.finalize()


if __name__ == "__main__":
    # mlvp.setup_logging(log_level=mlvp.logger.INFO)
    test_res()

