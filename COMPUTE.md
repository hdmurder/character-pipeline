# Compute request

Request: Berlin node/workspace access and scheduled use of one RTX 6000-class GPU plus a 512GB Mac Studio. No monetary grant requested. Propose an initial 4–6 week work period **after access is approved**, not a promise that approval takes that long.

Alexandre Montserrat is based about ten minutes from the node and can attend 2–3 times a week. Attendance is not a request for exclusive hardware ownership. Overnight jobs require the node's permission and scheduling.

## Confirm hardware before allocating jobs

“RTX 6000” is ambiguous. NVIDIA lists [RTX PRO 6000 Blackwell Workstation Edition](https://www.nvidia.com/en-us/products/workstations/professional-desktop-gpus/rtx-pro-6000) with **96GB** GDDR7, but [RTX 6000 Ada](https://www.nvidia.com/en-us/products/workstations/rtx-6000) with **48GB** GDDR6. The node's exact card has not been verified. Plan below assumes the 96GB card; if it is Ada, remeasure 4B memory first, shorten sequences, use quantized LoRA as needed and defer larger runs. No full-model 405B training is proposed.

A 512GB Mac Studio can plausibly host a quantized 405B teacher. Raw parameter storage alone is 202.5 decimal GB at four bits or 405GB at eight bits; quantization metadata, runtime allocations, KV cache and OS memory are additional. Four-bit is the starting point. This is inference, not training, and not a guarantee of a particular context length.

External measurements establish plausibility, not node performance. An [oMLX submission](https://omlx.ai/benchmarks/performance/epj3uc8c) reports Meta-Llama-3.1-405B four-bit on an M3 Ultra 512GB at 2.8 generation tokens/s, 29.8 prompt tokens/s and 220.8GB peak memory at 4K context. A [community llama.cpp benchmark](https://github.com/geerlingguy/ai-benchmarks/issues/42) reports Hermes-3 405B Q4_K_M at 1.96 generation tokens/s and 12.92 prompt tokens/s at 4K. Hermes is a post-trained variant, **not the proposed Base teacher**; it is a throughput comparison only. Hardware, runtime and checkpoints differ. Confirm chip, model identity, quantization, context, memory limits and sustained performance on the actual node.

## Initial GPU budget

All hours below are planning allowances, not measured RTX throughput. Assume a small reviewed pilot of roughly 0.25–0.5M training tokens, context 1–2K, LoRA and short development evaluations. Do not interpret them as a guaranteed fit for any dataset. Three seeds are budgeted for main comparisons; reduce scope rather than quietly oversubscribe.

| Stage | Runs / scope | GPU hours |
| --- | --- | --- |
| Environment, fit and exact-resume tests | Small smoke runs | 6–10 |
| Qwen3-30B-A3B teacher generation | Initial candidates; checker acceptance unknown | 12–24 |
| Checker and d1 calibration | Real-transcript human labels; judge shadow-only | 4–8 |
| Shared 4B SFT | Three seeds, 2–4h each | 6–12 |
| DPO / KTO / continued SFT | Three arms × three seeds, 2–4h each | 18–36 |
| Document grafting | Three fits × three seeds, 1–2h each | 9–18 |
| Competing-finetune survival | Small controlled follow-up | 6–12 |
| Behavioral / activation / steering evals | Fixed initial screen, then conditional confirmation | 10–20 |
| Conditional 8B-class smoke | Only after a useful 4B result | 8–16 |
| Total | Before contingency | **79–156** |
| Total plus 25% contingency | Rounded booking request | **100–195** |

This is one-GPU wall time, not multiplied by virtual GPU partitions. The 27B extension is outside this initial budget. If throughput or fit is worse than assumed, prioritize the shared 4B baseline and three follow-up arms; defer seeds, 8B and survival tests with explicit reporting.

## Separate Mac teacher budget

An optional 405B Base batch targets **1,000 candidate responses**, averaging 2,048 input and 512 generated tokens each. Candidates are not accepted conversations. Using external rate pairs of 30/2.8 and 13/1.96 prompt/generation tokens per second gives **69.76–116.32 Mac-hours** before overhead. Formula: candidates × (input tokens / prompt rate + output tokens / generation rate) / 3,600.

Add 50% for loading, retries and scheduling: **about 105–175 Mac-hours**. Multi-turn history growth, long outputs and poor acceptance could exceed this. Stop and re-estimate after 20 candidates. The Mac batch is optional and separate from the GPU Qwen teacher budget; it does not assume equivalent teacher quality or a measured batching speedup.

## What node access produces

Weeks 1–2 focus on hardware measurements, checker repair, calibration and reviewed data. Weeks 3–4 target controlled 4B fits and a small graft comparison. Weeks 5–6, if access and results permit, add survival tests, steering baselines and an 8B smoke run. Human source review and labeling are separate work, not hidden GPU hours.

Outputs should include rights-cleared character folders, reproducible run manifests, small-model adapters where licenses permit, held-out behavioral results, failure cases and measured compute cost. No stable Golem character, 405B teacher quality or multi-agent simulator is promised in advance.

Reproduce arithmetic with `python3 scripts/estimate_compute.py`. Hardware sources checked 29 October 2026; node inventory remains unverified.
