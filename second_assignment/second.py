import random, timeit, numpy, scipy.optimize as optimization

#------------------- BRUTE BIN PACKING --------------------

def check_validity(box, weights, capacity):
  # CHECK THE VALIDITY
  # Given a bin (box), the weights list and a value for the 
  # capacity, the function returns True if the selected bin
  # is valid, i.e. the sum of the weights contained in it
  # does not exceed the capacity, otherwise it returns False
	weight_sum = 0.
	for item in box: weight_sum += weights[item]
	if weight_sum <= capacity:
		return True
	return False

def generate_all_valid_choices(weights, capacity):
  # DEFINE THE SEARCH SPACE
  # Given the list of weights and the capacity, the function 
  # generates all the valid choices, since before yielding 
  # each partition the "check_validity" function is called.
	items = list(range(len(weights)))
	number_of_items = len(weights)

	def sub_generator():
		nonlocal items, number_of_items
		if len(items) == 1:
			yield [items]
		else:
			first = items[0]
			items = items[1:]

			for partition in sub_generator():
				for i, subset in enumerate(partition):
					if check_validity([first]+subset,weights,capacity):
						yield partition[:i]+[[first]+subset]+partition[i+1:]

				if len([[first]] + partition) < number_of_items:
					yield [[first]] + partition
			items = items[:]

	yield from sub_generator()

def brute_force_packing(number_of_items, weights, capacity):
  # SELECT THE OPTIMAL SOLUTION
  # Given the number of items (an integer), the list containing
  # the weight of each item and the value of the capacity, the 
  # the function iterates over all the valid partiotions of the
  # items and select the one with the least length.
  # The minimum number of partiotions in which items can be 
  # divided is stored in the optimal_number_of_bins variable.
  # The function returns the optimal packing, i.e. how to share
  # the items between the bins, and the optimal number of bins
  # needed to realized the beforementioned packaging.
	optimal_number_of_bins = number_of_items
	optimal_packing = [[item] for item in range(number_of_items)]
	for choice in generate_all_valid_choices(weights, capacity):
		length_of_current_packing = len(choice)
		if length_of_current_packing < optimal_number_of_bins:
			optimal_packing = choice
			optimal_number_of_bins = length_of_current_packing
	return optimal_packing, optimal_number_of_bins

#------------------- FIRST FIT BIN PACKING --------------------

def first_fit(number_of_items, weights, capacity):
  # GREEDY IMPLEMENTATION OF THE BIN PACKING PROBLEM
  # Given the number of items (an integer), the list containing
  # the weight of each item and the value of the capacity, the 
  # the function returns packaging and the corrisponding
  # number of bins obtained applying the First Fit algorithm.
  # This algorithm, basically, tries to insert the current
  # item in the first bin that has enough room for it and if 
  # there is no bin able to contain it the function creates
  # a new bin.
  # INITIALIZATION
	box_packing = [set() for i in range(number_of_items)]
	boxes = 0
	box_remaining_space = [capacity] * number_of_items
	# there can be at most "number_of_items" bins
	already_used_items = set()  # initialized to an empty set to perform an HASH LOOKUP later on
  # PACKING (placing the items one by one in the order they are provided)
	for item in range(number_of_items):
		for box in range(boxes):
			if box_remaining_space[box] >= weights[item]:
				box_packing[box].add(item)
				already_used_items.add(item)
				box_remaining_space[box] -= weights[item] # update the remaining space in the current space removing the weight of the used item
				break
		if item not in already_used_items:
			box_remaining_space[boxes] = capacity - weights[item]  # assign the item to a new bin
			already_used_items.add(item)
			box_packing[boxes].add(item)
			boxes += 1
	while set() in box_packing: box_packing.remove(set())
	return box_packing, boxes

#------------------- AUTOMATED TESTING ROUTINE AND CHECK --------------------

def automated_testing_routine(bpp_function):
	n1, C1, weights1 = 4, 2, [1.0, 1.4, 0.6, 1.0]
	first_instace_result = bpp_function(n1, weights1, C1)
	n2, C2, weights2 = 6, 2.5, [0.50, 1.25, 1.00, 1.75, 0.75, 1.50]
	second_instace_result = bpp_function(n2, weights2, C2)
	return first_instace_result, second_instace_result
# print(automated_testing_routine(brute_force_packing))
# print(automated_testing_routine(first_fit))
def check_automated_testing_routine(bpp_function):
	if bpp_function == brute_force_packing:
		test = ''
		if automated_testing_routine(bpp_function)[0] == ([[1, 2], [0, 3]], 2): test += '1'
		if automated_testing_routine(bpp_function)[1] == ([[1, 2], [0, 3], [4, 5]], 3): test += '2'
		if test == '12': return 'The brute force function has passed all tests'
		elif test == '1': return 'The brute force function has passed only the first test\nThe right solution for the second one was ([[1, 2], [0, 3], [4, 5]], 3)'
		elif test == '2': return 'The brute force function has passed only the second test\nThe right solution for the first one was ([[1, 2], [0, 3]], 2)'
		else: return 'The brute force function has failed all tests\nThe right solution for the first one was ([[1, 2], [0, 3], [4, 5]], 3)\nThe right solution for the second one was ([[1, 2], [3, 4], [0, 5]], 3)'
	if bpp_function == first_fit:
		test = ''
		if automated_testing_routine(bpp_function)[0] == ([{0, 2}, {1}, {3}], 3): test += '1'
		if automated_testing_routine(bpp_function)[1] == ([{0, 1, 4}, {2, 5}, {3}], 3): test += '2'
		if test == '12': return 'The first fit function has passed all tests'
		elif test == '1': return 'The first fit function has passed only the first test\nThe right solution for the second one was ([{0, 1, 4}, {2, 5}, {3}], 3)'
		elif test == '2': return 'The first fit function has passed only the second test\nThe right solution for the first one was ([{0, 2}, {1}, {3}], 3)'
		else: return 'The first fit function has failed all tests\nThe right solution for the first one was ([{0, 2}, {1}, {3}], 3)\nThe right solution for the second one was ([{0, 1, 4}, {2, 5}, {3}], 3)'
# print(check_automated_testing_routine(brute_force_packing))
# print(check_automated_testing_routine(first_fit))

#------------------- BENCHMARKING TESTING ROUTINE --------------------

def benchmarking_routine(bpp_function, n):
  # Given the Bin packing problem solving function and
  # the number of items n, the function test the selected
  # bpp_function on randomly generated inputs that consider 
  # all the constraints defined in the assignment.
	C = n**(1/2)
	weights = [random.uniform(0,1) for i in range(n)]
	while sum(weights) <= C:
		weights = [random.uniform(0,1) for i in range(n)]
	return bpp_function(n, weights, C)

def print_benchmarking_routine(items):
  # Given the list of the n instances for the number
  # of items, the function prints the solutions 
  # produced by both the brute_force_packing and 
  # the first_fit functions.
	for n in items:
		print('Number of items:',n)
		if n <= 13: print('The BRUTE packing and the optimal number of bins are: ',benchmarking_routine(brute_force_packing, n))
		else: print('The selected number of items is too high for the brute force solution')
		print('The GREEDY packing and the greedy number of bins are: ',end=' ')
		print(benchmarking_routine(first_fit, n))

items = [4, 6, 8, 10, 12, 14, 16, 18, 20]
#print_benchmarking_routine(items)

def approximation_ratio_routine(n):
  # Given the number of items n, the function computes
  # the ratio between between the number of bins used 
  # by the greedy solution and the number of bins used 
  # by the brute force solution, whenever the first_fit
  # function returns a sub-optimal solution.
	C = 1
	weights = [random.uniform(0,1) for i in range(n)]
	while sum(weights) <= C:
		weights = [random.uniform(0,1) for i in range(n)]
	print('Number of items:',n)
	if n <= 17:
		brute_bins = brute_force_packing(n, weights, C)
		greedy_bins = first_fit(n, weights, C)

		if brute_bins[1] < greedy_bins[1]:
			print('B', brute_bins[1])
			print('G', greedy_bins[1],'SUB-OPTIMAL')
			print('Approximation ratio: ', greedy_bins[1]/brute_bins[1])
			'''print(weights)
			print('B', brute_bins)
			print('G', greedy_bins) ACTIVATE ONLY TO CHECK'''
		else:
			print('B', brute_bins[1])
			print('G', greedy_bins[1])

	else: print('G', first_fit(n, weights, C)[1])

# for n in items:
# 	approximation_ratio_routine(n)

# HIGHEST APPROXIMATION RATIO
# Number of items: 4
# B 2
# G 3 SUB-OPTIMAL
# Approximation ratio:  1.5

#------------------- TIMEIT ANALYSIS AND COORDINATES --------------------

def runtime(bpp_function, n):
  # RUNTIME TESTING
  # Given the Bin packing problem solving function and the list 
  # with the input sizes we want to observe the runtime 
  # performance of, the function returns the average running 
  # time for a fixed number of repetitions
  # (in this case 2 for brute_force_packing and 100 for first_fit).
	runs = 100
	if bpp_function == "brute_force_packing": runs = 2
	average = timeit.timeit("benchmarking_routine("+bpp_function+','+str(n)+")", 
		number=runs, setup="from __main__ import "+bpp_function+", benchmarking_routine")/runs
	return average

# print('BRUTE timeit output: ')
# items = [4, 6, 8, 10, 12, 13]
# brute_data = [runtime("brute_force_packing", i) for i in items]
# print(brute_data)
# print('BRUTE coordinates\n')
# for (x,y) in zip(items,brute_data):
#   	print((x,y),end=' ')

# print('GREEDY timeit output: ')
# items = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
# greedy_data = [runtime("first_fit", i) for i in items]
# print(greedy_data)
# print('GREEDY coordinates\n')
# for (x,y) in zip(items,greedy_data):
#  	print((x,y),end=' ')

#------------------- SCIPY.OPTIMIZE APPLICATION --------------------

def exponentiation(n, a, b, c):  
  # Define the parametric relationship corresponding to the
  # Brute force time complexity. The complexity t is computed 
  # as a function of n and a, b and care the parameters	
	return a*(n**(b*(n+2)))+c

# brute_parameters = optimization.curve_fit(exponentiation, items, brute_data)
# print('\nBRUTE parameters:\n',brute_parameters)

def quadratic(n,a,b,c):
  # Define the parametric relationship corresponding to the
  # Greedy time complexity. The complexity t is computed 
  # as a function of n and a, b and care the parameters
	return a*(n**2)+b*n+c

# greedy_parameters = optimization.curve_fit(quadratic,items,greedy_data)
# print('\nGREEDY parameters:\n',greedy_parameters)
