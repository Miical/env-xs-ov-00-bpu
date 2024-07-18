from mlvp import Bundle

class DupBundle(Bundle):
    signals = ["_0", "_1", "_2", "_3"]

class PCBundle(Bundle):

    def __init__(self):
        super().__init__()
        self.in_s0_pc = DupBundle.from_prefix("io_in_bits_s0_pc")
        self.out_s2_pc = DupBundle.from_prefix("io_out_s2_pc")
        self.out_s3_pc = DupBundle.from_prefix("io_out_s3_pc")

class FullPredictBundle(Bundle):
    signals = [
        "br_taken_mask_0",
        "br_taken_mask_1",
        "slot_valids_0",
        "slot_valids_1",
        "targets_0",
        "targets_1",
        "jalr_target",
        "offsets_0",
        "offsets_1",
        "fallThroughAddr",
        "fallThroughErr",
        "last_may_be_rvi_call",
        "is_jalr",
        "is_call",
        "is_ret",
        "is_br_sharing",
        "hit",
    ]

class FTBBundle(Bundle):
    signals = [
        "valid",
        "brSlots_0_offset",
        "brSlots_0_lower",
        "brSlots_0_tarStat",
        "brSlots_0_sharing",
        "brSlots_0_valid",
        "tailSlot_offset",
        "tailSlot_lower",
        "tailSlot_tarStat",
        "tailSlot_sharing",
        "tailSlot_valid",
        "pftAddr",
        "carry",
        "isCall",
        "isRet",
        "isJalr",
        "last_may_be_rvi_call",
        "always_taken_0",
        "always_taken_1",
    ]

class SpecInfoBundle(Bundle):
    signals = [
        "ssp",
        "sctr",
        "TOSW_flag",
        "TOSW_value",
        "TOSR_flag",
        "TOSR_value",
        "NOS_flag",
        "NOS_value",
        "topAddr"
    ]

class UpdateBundle(Bundle):
    signals = [
        "valid",
        "ftb_entry_tailSlot_offset",
        "ftb_entry_tailSlot_valid",
        "ftb_entry_isCall",
        "ftb_entry_isRet",
        "cfi_idx_valid",
        "cfi_idx_bits",
        "jmp_taken",
        "meta",
    ]

class RedirectBundle(Bundle):
    signals = [
        "valid",
        "level",
        "pc",
        "pd_isRVC",
        "pd_isCall",
        "pd_isRet",
        "ssp",
        "sctr",
        "TOSW_flag",
        "TOSW_value",
        "TOSR_flag",
        "TOSR_value",
        "NOS_flag",
        "NOS_value",
    ]

class PipeCtrlBundle(Bundle):
    signals = ["reset", "io_reset_vector", "io_ctrl_ras_enable"]

    def __init__(self):
        super().__init__()

        self.s0_fire = DupBundle.from_prefix("io_s0_fire")
        self.s1_fire = DupBundle.from_prefix("io_s1_fire")
        self.s2_fire = DupBundle.from_prefix("io_s2_fire")
        self.s3_fire = DupBundle.from_prefix("io_s3_fire")
        self.s3_redirect = DupBundle.from_prefix("io_s3_redirect")




class RASInBundle(Bundle):
    def __init__(self):
        super().__init__()

        self.in_full_pred_s2_0 = FullPredictBundle.from_prefix("s2_full_pred_0_")
        self.in_full_pred_s2_1 = FullPredictBundle.from_prefix("s2_full_pred_1_")
        self.in_full_pred_s2_2 = FullPredictBundle.from_prefix("s2_full_pred_2_")
        self.in_full_pred_s2_3 = FullPredictBundle.from_prefix("s2_full_pred_3_")
        self.in_full_pred_s3_0 = FullPredictBundle.from_prefix("s3_full_pred_0_")
        self.in_full_pred_s3_1 = FullPredictBundle.from_prefix("s3_full_pred_1_")
        self.in_full_pred_s3_2 = FullPredictBundle.from_prefix("s3_full_pred_2_")
        self.in_full_pred_s3_3 = FullPredictBundle.from_prefix("s3_full_pred_3_")
        self.in_last_stage_ftb = FTBBundle.from_prefix("last_stage_ftb_entry_")

class RASOutBundle(Bundle):
    signals = ["last_stage_meta"]

    def __init__(self):
        super().__init__()

        self.full_pred_s2_0 = FullPredictBundle.from_prefix("s2_full_pred_0_")
        self.full_pred_s2_1 = FullPredictBundle.from_prefix("s2_full_pred_1_")
        self.full_pred_s2_2 = FullPredictBundle.from_prefix("s2_full_pred_2_")
        self.full_pred_s2_3 = FullPredictBundle.from_prefix("s2_full_pred_3_")
        self.full_pred_s3_0 = FullPredictBundle.from_prefix("s3_full_pred_0_")
        self.full_pred_s3_1 = FullPredictBundle.from_prefix("s3_full_pred_1_")
        self.full_pred_s3_2 = FullPredictBundle.from_prefix("s3_full_pred_2_")
        self.full_pred_s3_3 = FullPredictBundle.from_prefix("s3_full_pred_3_")
        self.last_stage_ftb = FTBBundle.from_prefix("last_stage_ftb_entry_")
        self.last_stage_spec = SpecInfoBundle.from_prefix("last_stage_spec_info_")

class RASBundle(Bundle):
    def __init__(self):
        super().__init__()

        self.pc = PCBundle()
        self.control = PipeCtrlBundle()

        self.resp_in = RASInBundle.from_prefix("io_in_bits_resp_in_0_")
        self.out = RASOutBundle.from_prefix("io_out_")

        self.update = UpdateBundle.from_regex(r"io_update_(?:(valid)|bits_(.*))")
        self.redirect = RedirectBundle.from_regex(r"io_redirect_(?:(valid)|bits_(level)|bits_cfiUpdate_(.*))")
