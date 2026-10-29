"""Planning assumptions, not hardware measurements. Run offline."""
import json

def estimate():
    gpu = {
        'setup_smoke_resume_tests': [6, 10],
        'teacher_generation_qwen': [12, 24],
        'checker_judge_calibration': [4, 8],
        'shared_sft_3_seeds': [3 * 2, 3 * 4],
        'preference_and_continued_sft_3_arms_3_seeds': [3 * 3 * 2, 3 * 3 * 4],
        'graft_3_fits_3_seeds': [3 * 3 * 1, 3 * 3 * 2],
        'competing_finetune_survival': [6, 12],
        'behavior_activation_steering_evals': [10, 20],
        'conditional_8b_smoke': [8, 16],
    }
    totals = [sum(v[i] for v in gpu.values()) for i in (0, 1)]
    mac = []
    for pp, tg in ((30, 2.8), (13, 1.96)):
        h = (1000 * 2048 / pp + 1000 * 512 / tg) / 3600
        mac.append(round(h, 2))
    return {'gpu_hours_by_stage': gpu, 'gpu_hours_total': totals,
            'gpu_hours_with_25pct_contingency': [round(v * 1.25, 2) for v in totals],
            'mac_1000_candidates_hours_at_two_external_rate_pairs': mac,
            'mac_with_50pct_contingency': [round(v * 1.5, 2) for v in mac],
            '405b_4bit_raw_GB': 405e9 * 4 / 8 / 1e9,
            '405b_8bit_raw_GB': 405e9 * 8 / 8 / 1e9}

if __name__ == '__main__':
    print(json.dumps(estimate(), indent=2))
