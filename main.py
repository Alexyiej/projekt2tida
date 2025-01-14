import time
import random
import pandas as pd
import heapq



def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def quick_sort(arr):
    if len(arr) <= 1: return arr
    pivot = arr[len(arr) // 2]

    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


def intro_sort(arr):
    if len(arr) <= 1: return arr


    def introsort_helper(start, end, depth_limit):
        if start > end: return
        
        if depth_limit == 0:
            heapq.heapify(arr[start:end + 1])
            arr[start:end + 1] = [heapq.heappop(arr[start:end + 1]) for _ in range(start, end + 1)]
        else:
            pivot = partition(start, end)
            introsort_helper(start, pivot - 1, depth_limit - 1)
            introsort_helper(pivot + 1, end, depth_limit - 1)


    def partition(low, high):
        pivot = arr[high]
        i = low - 1
    
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
    
        return i + 1


    depth_limit = (len(arr).bit_length() - 1) * 2
    introsort_helper(0, len(arr) - 1, depth_limit)


def measure_time(sort_function, data):
    start_time = time.time()
    
    if sort_function in [quick_sort, intro_sort]:
        sort_function(data.copy())  
    else:
        sort_function(data)

    end_time = time.time()
    return round(end_time - start_time, 3)


def generate_data(size): return [random.randint(0, 10000) for _ in range(size)]


data_sizes = [100, 1000, 10000]
results = []
algorithms = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Quick Sort": quick_sort,
    "Merge Sort": merge_sort,
    "TimSort": sorted,
    "IntroSort": intro_sort,
}


for size in data_sizes:
    data = generate_data(size)
    row = {"Rozmiar danych": size}

    for name, function in algorithms.items():
        time_taken = measure_time(function, data)
        row[name] = f"{time_taken} s"
    
    results.append(row)


df = pd.DataFrame(results)
print(df.to_string(index=False))