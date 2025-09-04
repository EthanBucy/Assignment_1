import csv
import statistics
import random
import time
import argparse
from typing import Callable, List, Dict
from sorting_algorithms import selection_sort, merge_sort, insertion_sort

# ====== CONFIG ======
DEFAULT_SEED = 42
NS = [100, 500, 1000, 5000]   # you can append larger n if your machine can handle it
DEFAULT_TRIALS = 5
REPEAT_PER_TRIAL = 1  # increase automatically if times are too small
# ====================

parser = argparse.ArgumentParser(description="Run sorting experiments with fixed seed and trials.")
parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Random seed (default 42).")
parser.add_argument("--trials", type=int, default=DEFAULT_TRIALS, help="Number of trials per test.")
args = parser.parse_args()

Algo = Callable[[List[int]], List[int]]

def make_permutation(n: int, rng: random.Random) -> List[int]:
    arr = list(range(1, n + 1))
    rng.shuffle(arr)
    return arr

def time_once(algo: Algo, data: List[int]) -> float:
    start = time.perf_counter()
    _ = algo(data)  # returns new list; original 'data' unchanged
    end = time.perf_counter()
    return end - start

def time_trial(algo: Algo, data: List[int], repeat: int) -> float:
    # If time is tiny, repeat many times and divide to reduce clock noise
    if repeat <= 1:
        t = time_once(algo, data)
        if t < 1e-4:
            # auto-increase repeats for stability
            repeat = max(10, int(1e-3 / max(t, 1e-9)))
        else:
            return t
    total = 0.0
    for _ in range(repeat):
        total += time_once(algo, data)
    return total / repeat

def run():
    rng = random.Random(args.seed)
    results: List[Dict[str, str]] = []

    algos = {
        "SelectionSort": selection_sort,
        "MergeSort": merge_sort,
        "InsertionSort": insertion_sort,
    }

    for n in NS:
        for name, fn in algos.items():
            trial_times: List[float] = []
            for t in range(args.trials):
                # fresh permutation each trial; seed is fixed overall for reproducibility
                data = make_permutation(n, rng)
                tsec = time_trial(fn, data, REPEAT_PER_TRIAL)
                trial_times.append(tsec)

            median = statistics.median(trial_times)
            mean = statistics.fmean(trial_times)
            stdev = statistics.pstdev(trial_times) if len(trial_times) > 1 else 0.0

            results.append({
                "algorithm": name,
                "n": str(n),
                "median_s": f"{median:.8f}",
                "mean_s": f"{mean:.8f}",
                "stdev_s": f"{stdev:.8f}",
            })
            print(f"{name:14s} n={n:5d}  median={median:.6e}s  mean={mean:.6e}s  sd={stdev:.2e}")

    with open("results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["algorithm", "n", "median_s", "mean_s", "stdev_s"])
        writer.writeheader()
        writer.writerows(results)
    print("Wrote results.csv")

if __name__ == "__main__":
    run()
