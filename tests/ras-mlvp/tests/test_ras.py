import sys
sys.path.append('../../../out/picker_out_RAS')
sys.path.append('../')

import mlvp
from env import *
from generator import FullPredGenerator
from UT_RAS import DUTRAS



async def test_ras_spec_push_and_pop(ras_env: RASEnv):
    """
    测试 RAS spec 栈最基本的压栈和出栈功能（不考虑栈溢出）
    """

    await ras_env.reset()

    gen = FullPredGenerator()
    for _ in range(SPEC_MAX_SIZE):
        await ras_env.s2_s3_same(gen.random_call())
    for _ in range(SPEC_MAX_SIZE):
        await ras_env.s2_s3_same(gen.random_ret())

async def test_ras_spec_push_and_pop_with_overflow(ras_env: RASEnv):
    """
    测试 RAS Spec 栈在栈满的情况下是否可以正常出入栈

    BUG 该用例无法通过
    """
    await ras_env.reset()

    gen = FullPredGenerator()
    for _ in range(SPEC_MAX_SIZE):
        await ras_env.s2_s3_same(gen.random_call())

    for _ in range(2):
        await ras_env.s2_s3_same(gen.random_call())
    for _ in range(2):
        await ras_env.s2_s3_same(gen.random_ret())



async def top_test(ras):
    mlvp.create_task(mlvp.start_clock(ras))


    ras_bundle = RASBundle().set_name("ras").bind(ras)
    ras_bundle.set_all(0)

    env = RASEnv(ras_bundle)
    model = RASModel()
    env.attach(model)


    await test_ras_spec_push_and_pop_with_overflow(env)



if __name__ == "__main__":
    ras = DUTRAS()
    ras.init_clock("clock")
    # mlvp.setup_logging(log_level=mlvp.logger.INFO)
    mlvp.setup_logging(log_level=mlvp.logger.ERROR)
    mlvp.run(top_test(ras), ras)
    ras.finalize()
