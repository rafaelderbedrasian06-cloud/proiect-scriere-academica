import time
import sys
import threading
from sorting import bubble_sort, selection_sort, insertion_sort, merge_sort, shell_sort
from utils import generate_random

sys.setrecursionlimit(200000)

SIZES = [10, 20, 50, 100, 1000, 10000, 100000, 1000000, 10000000]

ALGORITHMS = [
    ("Bubble Sort",    bubble_sort),
    ("Selection Sort", selection_sort),
    ("Insertion Sort", insertion_sort),
    ("Merge Sort",     merge_sort),
    ("Shell Sort",     shell_sort),
]

MERGE_LIMIT = 1000000
TIMEOUT = 90  

def run_with_timeout(func, arr, timeout):
    result = {"elapsed": None, "done": False}

    def target():
        start = time.perf_counter()
        func(arr)
        result["elapsed"] = time.perf_counter() - start
        result["done"] = True

    t = threading.Thread(target=target, daemon=True)
    t.start()
    t.join(timeout)
    return result["elapsed"] if result["done"] else None


def main():
    results = {}

    for name, func in ALGORITHMS:
        timed_out = False
        results[name] = []
        print(f"[{name}]")
        print(f"  {'N (elemente)':<20}{'Timp (secunde)':<20}")
        print("  " + "-" * 42)

        for n in SIZES:
            if n > MERGE_LIMIT and name == "Merge Sort":
                print(f"  {n:<20}{'LIMITA RECURSIVITATE (skip)':<20}")
                results[name].append(None)
                continue

            if timed_out:
                print(f"  {n:<20}{'PREA LENT (skip)':<20}")
                results[name].append(None)
                continue

            arr = generate_random(n)
            elapsed = run_with_timeout(func, arr, TIMEOUT)

            if elapsed is None:
                print(f"  {n:<20}{'PREA LENT (>90s, skip)':<20}")
                timed_out = True
                results[name].append(None)
            else:
                print(f"  {n:<20}{elapsed:.6f} s")
                results[name].append(elapsed)

        print()

    print("=" * 62)
    print("Experiment finalizat.")

   
    print("\n" + "=" * 62)
    print("REZUMAT FINAL (toti algoritmii)")
    print("=" * 62)

    
    print(f"{'Algoritm':<20}", end="")
    for n in SIZES:
        print(f"{str(n):<12}", end="")
    print()
    print("-" * (20 + 12 * len(SIZES)))

    
    for name in results:
        print(f"{name:<20}", end="")
        for t in results[name]:
            if t is None:
                print(f"{'X':<12}", end="")
            else:
                print(f"{t:.4f}".ljust(12), end="")
        print()


if __name__ == "__main__":
    main()
