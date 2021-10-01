"""
MathWorld: "Hundred-Dollar, Hundred-Digit Challenge Problems", Challenge #3.
http://mathworld.wolfram.com/Hundred-DollarHundred-DigitChallengeProblems.html
The Computer Language Benchmarks Game
http://benchmarksgame.alioth.debian.org/u64q/spectralnorm-description.html#spectralnorm
Contributed by Sebastien Loisel
Fixed by Isaac Gouy
Sped up by Josh Goldfoot
Dirtily sped up by Simon Descarpentries
Concurrency by Jason Stitt
"""

import pyjion
import timeit
from statistics import fmean

DEFAULT_N = 130


def eval_A(i, j):
    return 1.0 / ((i + j) * (i + j + 1) // 2 + i + 1)


def eval_times_u(func, u):
    return [func((i, u)) for i in range(len(list(u)))]


def eval_AtA_times_u(u):
    return eval_times_u(part_At_times_u, eval_times_u(part_A_times_u, u))


def part_A_times_u(i_u):
    i, u = i_u
    partial_sum = 0
    for j, u_j in enumerate(u):
        partial_sum += eval_A(i, j) * u_j
    return partial_sum


def part_At_times_u(i_u):
    i, u = i_u
    partial_sum = 0
    for j, u_j in enumerate(u):
        partial_sum += eval_A(j, i) * u_j
    return partial_sum


def bench_spectral_norm():
    u = [1] * DEFAULT_N

    for dummy in range(10):
        v = eval_AtA_times_u(u)
        u = eval_AtA_times_u(v)

    vBv = vv = 0

    for ue, ve in zip(u, v):
        vBv += ue * ve
        vv += ve * ve


if __name__ == "__main__":
    without_result = timeit.repeat(bench_spectral_norm, repeat=5, number=10)
    print("{0} took {1} min, {2} max, {3} mean without Pyjion".format("spectralnorm", min(without_result), max(without_result), fmean(without_result)))
    pyjion.enable()
    pyjion.config(level=2, pgc=False)
    with_result = timeit.repeat(bench_spectral_norm, repeat=5, number=10)
    pyjion.disable()
    print("{0} took {1} min, {2} max, {3} mean with Pyjion".format("spectralnorm", min(with_result), max(with_result), fmean(with_result)))
    delta = (abs(fmean(with_result) - fmean(without_result)) / fmean(without_result)) * 100.0
    print(f"Pyjion is {delta:.2f}% faster")
