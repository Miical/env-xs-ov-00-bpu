import mlvp
import sys
from ras_bundle import *
from generator import FullPredGenerator
from model import *
from env import *

sys.path.append('../../out/picker_out_RAS')
from UT_RAS import DUTRAS

async def top_test(ras):
    mlvp.create_task(mlvp.start_clock(ras))


    ras_bundle = RASBundle().set_name("ras").bind(ras)
    ras_bundle.set_all(0)
    # print(Bundle.detect_unconnected_signals(ras))

    env = DUTEnv(ras_bundle)
    model = RASModel()
    env.attach(model)

    gen = FullPredGenerator()

    await env.put_s2(gen.random_item())
    print(await env.drive_completed())
    await env.put_s2(gen.random_item())
    print(await env.drive_completed())

    await ras_bundle.step(2)






if __name__ == "__main__":
    ras = DUTRAS()
    ras.init_clock("clock")
    mlvp.setup_logging(log_level=mlvp.logger.INFO)
    mlvp.run(top_test(ras))
    ras.finalize()


