from mlvp import Bundle, Signals, Signal

class DupBundle(Bundle):
    _0, _1, _2, _3 = Signals(4)

class PCBundle(Bundle):
    in_s0_pc = DupBundle.from_prefix("io_in_bits_s0_pc")
    out_s2_pc = DupBundle.from_prefix("io_out_s2_pc")
    out_s3_pc = DupBundle.from_prefix("io_out_s3_pc")

class FullPredictBundle(Bundle):
    br_taken_mask_0, br_taken_mask_1, \
    slot_valids_0, slot_valids_1, \
    targets_0, targets_1, \
    jalr_target, \
    offsets_0, offsets_1, \
    fallThroughAddr, fallThroughErr, \
    last_may_be_rvi_call, \
    is_jalr, is_call, is_ret, is_br_sharing, hit = Signals(17)

class FTBBundle(Bundle):
    valid, \
    brSlots_0_offset, brSlots_0_lower, brSlots_0_tarStat, brSlots_0_sharing, brSlots_0_valid, \
    tailSlot_offset, tailSlot_lower, tailSlot_tarStat, tailSlot_sharing, tailSlot_valid, \
    pftAddr, carry, isCall, isRet, isJalr, last_may_be_rvi_call, always_taken_0, always_taken_1 = Signals(19)

class SpecInfoBundle(Bundle):
    ssp, sctr, \
    TOSW_flag, TOSW_value, \
    TOSR_flag, TOSR_value, \
    NOS_flag, NOS_value, \
    topAddr = Signals(9)

class UpdateBundle(Bundle):
    valid, \
    ftb_entry_tailSlot_offset, ftb_entry_tailSlot_valid, \
    ftb_entry_isCall, ftb_entry_isRet, \
    cfi_idx_valid, cfi_idx_bits, \
    jmp_taken, \
    meta = Signals(9)

class RedirectBundle(Bundle):
    valid, level, \
    pc, \
    pd_isRVC, pd_isCall, pd_isRet, \
    ssp, sctr, \
    TOSW_flag, TOSW_value, \
    TOSR_flag, TOSR_value, \
    NOS_flag, NOS_value = Signals(14)

class PipeCtrlBundle(Bundle):
    reset, io_reset_vector, io_ctrl_ras_enable = Signals(3)

    s0_fire = DupBundle.from_prefix("io_s0_fire")
    s1_fire = DupBundle.from_prefix("io_s1_fire")
    s2_fire = DupBundle.from_prefix("io_s2_fire")
    s3_fire = DupBundle.from_prefix("io_s3_fire")
    s3_redirect = DupBundle.from_prefix("io_s3_redirect")

class RASInBundle(Bundle):
    full_pred_s2_0 = FullPredictBundle.from_prefix("s2_full_pred_0_")
    full_pred_s2_1 = FullPredictBundle.from_prefix("s2_full_pred_1_")
    full_pred_s2_2 = FullPredictBundle.from_prefix("s2_full_pred_2_")
    full_pred_s2_3 = FullPredictBundle.from_prefix("s2_full_pred_3_")
    full_pred_s3_0 = FullPredictBundle.from_prefix("s3_full_pred_0_")
    full_pred_s3_1 = FullPredictBundle.from_prefix("s3_full_pred_1_")
    full_pred_s3_2 = FullPredictBundle.from_prefix("s3_full_pred_2_")
    full_pred_s3_3 = FullPredictBundle.from_prefix("s3_full_pred_3_")
    last_stage_ftb = FTBBundle.from_prefix("last_stage_ftb_entry_")

class RASOutBundle(Bundle):
    last_stage_meta = Signal()

    full_pred_s2_0 = FullPredictBundle.from_prefix("s2_full_pred_0_")
    full_pred_s2_1 = FullPredictBundle.from_prefix("s2_full_pred_1_")
    full_pred_s2_2 = FullPredictBundle.from_prefix("s2_full_pred_2_")
    full_pred_s2_3 = FullPredictBundle.from_prefix("s2_full_pred_3_")
    full_pred_s3_0 = FullPredictBundle.from_prefix("s3_full_pred_0_")
    full_pred_s3_1 = FullPredictBundle.from_prefix("s3_full_pred_1_")
    full_pred_s3_2 = FullPredictBundle.from_prefix("s3_full_pred_2_")
    full_pred_s3_3 = FullPredictBundle.from_prefix("s3_full_pred_3_")
    last_stage_ftb = FTBBundle.from_prefix("last_stage_ftb_entry_")
    last_stage_spec = SpecInfoBundle.from_prefix("last_stage_spec_info_")

class RASBundle(Bundle):
    pc = PCBundle()
    control = PipeCtrlBundle()

    resp_in = RASInBundle.from_prefix("io_in_bits_resp_in_0_")
    out = RASOutBundle.from_prefix("io_out_")

    update = UpdateBundle.from_regex(r"io_update_(?:(valid)|bits_(.*))")
    redirect = RedirectBundle.from_regex(r"io_redirect_(?:(valid)|bits_(level)|bits_cfiUpdate_(.*))")
