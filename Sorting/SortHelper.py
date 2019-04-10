import numpy as np
import random
import time
import matplotlib.pyplot as plt
import math

def CallOrder(arr):
	global count
	count = 1
	def mergeSort(arr):
		global count 
		print(str(count) + ": ", arr)
		count = count + 1
		if len(arr) >1: 
			mid = len(arr)//2 
			L = arr[:mid] # Dividing the array elements  
			R = arr[mid:] # into 2 halves 

			mergeSort(L) # Sorting the first half 
			mergeSort(R) # Sorting the second half 

			i = j = k = 0

			# Copy data to temp arrays L[] and R[]
			while i < len(L) and j < len(R):
				if L[i] < R[j]:
					arr[k] = L[i]
					i+=1
				else: 
					arr[k] = R[j] 
					j+=1
				k+=1
			# Checking if any element was left 
			while i < len(L):
				arr[k] = L[i]
				i+=1
				k+=1
			while j < len(R): 
				arr[k] = R[j] 
				j+=1
				k+=1

	mergeSort(arr)


def DisplayResults(method1, method2, inputType = "Random"):
	def partition(array , low , high):
		i = low - 1
		pivot = array[high]
		for j in range( low , high):
			if array[j] <= pivot:

				i += 1
				array[i],array[j] = array[j],array[i] # Swapping 
		array[i+1],array[high] = array[high],array[i+1] 
		return(i+1)

	def QuickSort(array,low,high, method):
		if low < high:

			if method == 'Last Element':
				random_value = high
			elif method == "Random":
				random_value = random.randint(low,high)
			elif method == "Median":
				random_value = math.floor(quickselect_median(array))
			elif method == "Median of Three":
				random_value = median_of_three(array, low, high)

			array[random_value] , array[high] = array[high], array[random_value] 

			mid = partition(array,low,high)
			QuickSort(array,low,mid-1, method)
			QuickSort(array,mid+1,high, method)

	def quickselect(l, k, pivot_fn):
		if len(l) == 1:
			assert k == 0
			return l[0]

		pivot = pivot_fn(l)

		lows = [el for el in l if el < pivot]
		highs = [el for el in l if el > pivot]
		pivots = [el for el in l if el == pivot]

		if k < len(lows):
			return quickselect(lows, k, pivot_fn)
		elif k < len(lows) + len(pivots):
			return pivots[0]
		else:
			return quickselect(highs, k - len(lows) - len(pivots), pivot_fn)

	def quickselect_median(l, pivot_fn=random.choice):
	    if len(l) % 2 == 1:
	        return quickselect(l, len(l) / 2, pivot_fn)
	    else:
	        return 0.5 * (quickselect(l, len(l) / 2 - 1, pivot_fn) +
	                      quickselect(l, len(l) / 2, pivot_fn))

	def median_of_three(L, low, high):
	    mid = (low+high-1)//2
	    a = L[low]
	    b = L[mid]
	    c = L[high-1]
	    if a <= b <= c:
	        return mid
	    if c <= b <= a:
	        return mid
	    if a <= c <= b:
	        return high-1
	    if b <= c <= a:
	        return high-1
	    return low
	

	results = []
	iteration = 1000
	n = 100
	for _ in range(iteration):
		if (inputType == "Random"):
			randomList = np.random.randint(n, size = n)
		if (inputType == "Sorted"):
			randomList = np.array(list(range(n)))
		if (inputType == "First Half Sorted"):
			half = int((n/2))
			randomList = np.array(list(list(range(half)) + np.random.randint(half, size = half)))
		if (inputType == "Partially Sorted"):
			randomList = np.array(list(np.random.randint(int(n/4), size = int(n/4))) + list(range(int(n/2))) + list(np.random.randint(int(n/4), size = int(n/4))))
		start = time.time()
		QuickSort(randomList, 0, len(randomList)-1, method1)
		end = time.time()
		results.append(end - start)

	results2 = []
	for _ in range(iteration):
		if (inputType == "Random"):
			randomList = np.random.randint(n, size = n)
		if (inputType == "Sorted"):
			randomList = np.array(list(range(n)))
		if (inputType == "Half Sorted"):
			half = int((n/2))
			randomList = np.array(list(list(range(half)) + np.random.randint(half, size = half)))
		if (inputType == "Partially Sorted"):
			randomList = np.array(list(np.random.randint(int(n/4), size = int(n/4))) + list(range(int(n/2))) + list(np.random.randint(int(n/4), size = int(n/4))))
		start = time.time()
		QuickSort(randomList, 0, len(randomList)-1, method2)
		end = time.time()
		results2.append(end - start)

	labels = [method1, method2]
	ax = plt.hist((results, results2), 
		bins = 100, 
		label = labels, 
		histtype = 'stepfilled',
		density = True,
		alpha = 0.7,
		color = ("red", "blue"))
	plt.legend()
	plt.title("Histogram of Runtimes")
	plt.xlabel('Runtime')
	plt.ylabel('Count')
	plt.figure(num=None, figsize=(8, 6), facecolor='w', edgecolor='k')

	return ax, np.mean(results), np.mean(results2)