import csv
import math
from collections import defaultdict
import matplotlib.pyplot as plt

def load_results(path="results.csv"):
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            r["n"] = int(r["n"])
            r["median_s"] = float(r["median_s"])
            rows.append(r)
    return rows

def plot_linear(rows):
    by_algo = defaultdict(list)
    for r in rows:
        by_algo[r["algorithm"]].append((r["n"], r["median_s"]))
    for algo in by_algo:
        by_algo[algo].sort()

    plt.figure()
    for algo, pts in by_algo.items():
        xs = [n for (n, _) in pts]
        ys = [t for (_, t) in pts]
        plt.plot(xs, ys, marker="o", label=algo)
    plt.xlabel("Input size n")
    plt.ylabel("Median time (seconds)")
    plt.title("Sorting Runtimes (Linear Scale)")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig("plot_linear.png", dpi=200)

def plot_log(rows, loglog=False):
    by_algo = defaultdict(list)
    for r in rows:
        by_algo[r["algorithm"]].append((r["n"], r["median_s"]))
    for algo in by_algo:
        by_algo[algo].sort()

    plt.figure()
    for algo, pts in by_algo.items():
        xs = [n for (n, _) in pts]
        ys = [t for (_, t) in pts]
        if loglog:
            plt.xscale("log"); plt.yscale("log")
            title = "Sorting Runtimes (Log–Log)"
            fname = "plot_loglog.png"
        else:
            plt.yscale("log")
            title = "Sorting Runtimes (Semi-Log: y)"
            fname = "plot_semilog.png"
        plt.plot(xs, ys, marker="o", label=algo)
    plt.xlabel("Input size n")
    plt.ylabel("Median time (seconds)")
    plt.title(title)
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(fname, dpi=200)

if __name__ == "__main__":
    rows = load_results()
    plot_linear(rows)
    plot_log(rows, loglog=False)  # semi-log
    plot_log(rows, loglog=True)   # log-log
    print("Saved plot_linear.png, plot_semilog.png, plot_loglog.png")
