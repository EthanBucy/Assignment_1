# sorting_algorithms.py
from typing import List

def selection_sort(a: List[int]) -> List[int]:
    """Return a NEW sorted list using Selection Sort (O(n^2))."""
    arr = a.copy()
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def merge_sort(a: List[int]) -> List[int]:
    """Return a NEW sorted list using Merge Sort (O(n log n))."""
    arr = a.copy()
    return _merge_sort_inplace(arr, 0, len(arr))

def _merge_sort_inplace(arr: List[int], lo: int, hi: int) -> List[int]:
    if hi - lo <= 1:
        return arr[lo:hi]
    mid = (lo + hi) // 2
    left = _merge_sort_inplace(arr, lo, mid)
    right = _merge_sort_inplace(arr, mid, hi)
    return _merge(left, right)

def _merge(left: List[int], right: List[int]) -> List[int]:
    i = j = 0
    out: List[int] = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out

def insertion_sort(a: list[int]) -> list[int]:
    """Return a NEW sorted list using Insertion Sort (O(n^2))."""
    arr = a.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
