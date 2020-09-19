import random, timeit, numpy, scipy.optimize as op

def all_possible_combinations(suppliers, weights):
  # DEFINE THE SEARCH SPACE
  # Given the list of suppliers and the dictionary with their 
  # weights, the function generates all the possible sublists 
  # of suppliers associated to the sum of their weights in the
  # form of a list of tuples. In position 0 of the tuple, the
  # list of suppliers will be stored, while in position 1 will 
  # be stored a number corresponding to the sum of the 
  # respective weights 
	records = []
	for supplier in suppliers:
		n = len(records)
		for i in range(n):
			new_list = records[i][0][:]
			new_list.append(supplier)
			records.append((new_list, records[i][1] + weights[supplier]))
		records.append(([supplier], weights[supplier]))
	records.append(([],0))
	return records
def compatible(choices, L):
  # CHECK THE COMPATIBILITY
  # Given one list of suppliers and the dictionary with their
  # corresponding incompatibilities, the funcion convert the
  # list of suppliers in a set and with a hash lookup checks 
  # if there are any incompatibilities
	set_of_choices = set(choices)
	for supplier in choices:
		for incompatible in L[supplier]:
			if incompatible in set_of_choices:
				return False
	return True
def optimal_purchase_plan(suppliers, weights, incompatibilities):
  # Input:
  # - suppliers: a list containing hashable objects (e.g. strings 
  #            or integers) that represent the identifiers
  #            of the suppliers
  # - weights: a dictionary mapping each identifier to a
  #            floating point number that represents the
  #            weight offered by that supplier
  # - incompatibilities: a dictionary mapping each identifier
  #            to the set (or list) of the identifiers of the suppliers
  #            that are incompatible with it
  # Output:
  #            a list of identifiers of pairwise compatible
  #            suppliers that provide maximal total weight
	best_combination = []
	max_weight = 0.0
	for combination in all_possible_combinations(suppliers, weights):
		if combination[1] > max_weight:
			if compatible(combination[0], incompatibilities):
				best_combination = combination[0]
				max_weight = combination[1]
	return best_combination #to see also the corresponding purchased grams of substance use "return (best_combination, max_weight)"

lengths=[4,8,10,12,14,16,18,20,22,24]
def testing_routine(n):
  # Given the number of suppliers n, the function 
  # test optimal_purchase_plan() on randomly generated inputs
  # that consider all the constraints defined in the assignement
	suppliers=list(range(n))
	weights, incompatibilities = dict(), dict()
	for s_i in suppliers:
		weights[s_i] = random.uniform(0,1)
		tc_suppliers = set(suppliers) #temporary copy of suppliers in the form of a set
		tc_suppliers.discard(s_i)
		incompatibles_for_s_i = set(random.sample(tc_suppliers,n//2))
		incompatibilities[s_i] = incompatibles_for_s_i
	return optimal_purchase_plan(suppliers, weights, incompatibilities)

for n in lengths:
	print('Number of suppliers:',n)
	print('The optimal purchase plan to be selected is: ',end=' ')
	print(testing_routine(n))

def runtime(function, lengths):
  # RUNTIME TESTING
  # Given the function and the list with the input sizes we want
  # to the test the function for, "runtime" returns a list with
  # the average running time for a fixed number of repetitions
  # (in this case 10) for each value in length
	average=[]
	for i in lengths:
		average.append(timeit.timeit(function+"("+str(i)+')', 
			number=10, setup="from __main__ import "+function+",random")/10)
	return average

data=runtime("testing_routine",lengths)

print('Coordinates\n')
for (x,y) in zip(lengths,data):
	print((x,y),end=' ')

def complexity_equation(n,a,b):
  # Define the parametric relationship corresponding to the
  # time complexity of optimal_purchase_plan()
  # The complexity t is computed as a function of n and 
  # a and b are the parameters
	return a*((2**n)*(n**2))+b

variable=op.curve_fit(complexity_equation,lengths,data)
print('\nParameters\n')
print(variable)
