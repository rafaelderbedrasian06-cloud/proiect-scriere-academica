import random


def generate_random(n):
    return [random.randint(0, n * 10) for _ in range(n)]


def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
