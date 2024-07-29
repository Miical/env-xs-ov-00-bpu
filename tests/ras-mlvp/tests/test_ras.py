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

async def test_ras_spec_push_and_pop_with_overflow(ras_env: RASEnv):
    """
    测试 RAS Spec 栈在压入相同地址栈满的情况下是否可以正常出栈
    """

    await ras_env.reset()

    gen = FullPredGenerator()
    for _ in range(SPEC_MAX_SIZE):
        await ras_env.s2_s3_same(gen.random_call(specific_addr=0x12345))

    for _ in range(SPEC_MAX_SIZE):
        await ras_env.s2_s3_same(gen.random_ret())


async def test_ras_test_push_same_addr_with_stack_full(ras_env: RASEnv):
    """
    测试 RAS Spec 栈 Counter 在出入栈时是否正确

    Spec栈 Counter 有问题但未修复, RM 实现为不带 Counter 的版本, 因此出现栈溢出

    BUG 栈溢出时, POP 出的地址有异常
    """

    await ras_env.reset()

    gen = FullPredGenerator()
    for i in range(SPEC_MAX_SIZE):
        for _ in range(MAX_COUNTER):
            await ras_env.s2_s3_same(gen.random_call(specific_addr=i))

    for _ in range(MAX_COUNTER):
        await ras_env.s2_s3_same(gen.random_ret())

async def test_ras_spec_pop_with_one_element(ras_env: RASEnv):
    """
    测试 RAS Spec 栈只有一个元素时是否可以正常出栈
    """

    await ras_env.reset()

    gen = FullPredGenerator()
    for _ in range(100):
        await ras_env.s2_s3_same(gen.random_call())
        await ras_env.s2_s3_same(gen.random_ret())






async def top_test(ras):
    mlvp.create_task(mlvp.start_clock(ras))


    ras_bundle = RASBundle().set_name("ras").bind(ras)
    ras_bundle.set_all(0)

    env = RASEnv(ras_bundle)
    model = RASModel()
    env.attach(model)


    # await test_ras_spec_push_and_pop(env)
    # await test_ras_spec_push_and_pop_with_overflow(env)
    # await test_ras_spec_push_and_pop_with_overflow(env)
    # await test_ras_test_push_same_addr_with_stack_full(env)
    # await test_ras_spec_pop_with_one_element(env)



if __name__ == "__main__":
    ras = DUTRAS()
    ras.init_clock("clock")
    # mlvp.setup_logging(log_level=mlvp.logger.INFO)
    mlvp.setup_logging(log_level=mlvp.logger.ERROR)
    mlvp.run(top_test(ras), ras)
    ras.finalize()
