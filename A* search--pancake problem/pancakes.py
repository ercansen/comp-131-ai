# Artificial Intelligence: Homework 2 -- A* Search
# October 15, 2019
# Ercan Sen and Kerem San
# Filename: pancakes.py
# Purpose: Solves the 'Pancake Problem' using A* Search algorithm

from queue import PriorityQueue
import copy

# Calculates the "gap heuristic" as explained in the Landmark Heuristics article
def heuristic(inpList):
	h = 0
	for i in range(len(inpList) - 1):
		if abs(inpList[i] - inpList[i+1]) > 1:
			h += 1
	return h # forward cost

# Computes the "k-flip", for k = {2, ... , (# pancakes)}
# Returns the number of flipped pancakes, which is cumulatively added to the backward cost
def flip(inpList, k):
	i = 1
	cost = k
	while (k - i > 0):
		switch(inpList, (i-1), (k-1))
		i += 1
		k -= 1
	return cost # backward cost

# Helper for the function 'flip'; switches the list values for given indices
def switch(inpList, ind1, ind2):
	val1 = inpList[ind1]
	inpList[ind1] = inpList[ind2]
	inpList[ind2] = val1

# Used when the algorithm successfully finds a solution
def success(Dict):
		print('Success')
		print('Number of flips: ' + str(len(Dict['prev'])))
		for List in Dict['prev']:
			print('[', *List, '],', sep=' ')
		print('[', *Dict['self'], ']', sep=' ')

# Used when the algorithm fails to find a solution
def failure():
	print('Failed to reach a solution')

# Class that creates an instance of pancakes-list object and
## uses A* algorithm to find the best possible solution
class Pancakes:
	num_pancakes = 0
	plate = 0 # Not a part of the 'flip's; used by the heuristic calculation
	initial = []
	goal_state = []
	frontier = PriorityQueue()
	costs_dict = {} # Used to keep only the least costly one of the same sequences
	unique_id = 0 # Serves as a tie-breaker, when priorities in frontier are equal
	popped = {}

	# Constructor
	# Takes user input to determine # pancakes, initial order of pancakes
	# Sets the goal_state
	def __init__(self):
		self.num_pancakes = int(input('Enter number of pancakes: '))
		self.plate = self.num_pancakes + 1
		print('Top ' + ('__ ' * self.num_pancakes) + 'Plate')
		inputs = input('Enter the initial order of pancakes (sizes) as shown' +
			           ' above (just enter numbers with a space in between; ' +
			           '1: smallest, ' + str(self.num_pancakes) + 
			           ': largest) ').split()
		for inp in inputs:
			if int(inp) not in range(1, self.num_pancakes+1):
				raise Exception('The input should be num.s between 1 and ' + str(self.num_pancakes) +
					            ' each appearing once, in any order.')
			self.initial.append(int(inp))

		if sum(self.initial) != (self.num_pancakes * (self.num_pancakes + 1) * (1/2)):
			raise Exception('The input should be num.s between 1 and ' + str(self.num_pancakes) + 
				            ' each appearing once, in any order.')

		self.initial.append(self.plate)
		self.goal_state = list(range(1, self.num_pancakes+2))

	# Determines whether a sequence exists in the frontier at the moment
	def is_popped(self, key):
		if (key in self.popped.keys()) and (self.popped[key] == True):
			return True
		else:
			return False

	# Sets the 3-tuple to be added to frontier; assigns relevant val.s to helper dict.s
	def add_to_frontier(self, pri, Dict):
		self.frontier.put((pri, self.unique_id, Dict))
		self.unique_id += 1
		self.costs_dict[tuple(Dict['self'])] = pri
		self.popped[tuple(Dict['self'])] = False


	# Helper for the Pancakes class function 'astar'
	# For the given list (of pancakes), computes all possible k = {2,...,n} flips
	# Checks for repeated sequences of pancakes and only keeps those with min. total cost
	# Keeps track of previous sequences and cumulative (backward) cost
	def expand_flips(self, inpDict):
		for i in range(2, self.num_pancakes+1):
			newDict = copy.deepcopy(inpDict)
			newDict['prev'].append(inpDict['self'])
			backward = flip(newDict['self'], i)
			newDict['cumulCost'] += backward
			forward = heuristic(newDict['self'])
			priorityToAdd = newDict['cumulCost'] + forward
			
			if tuple(newDict['self']) in self.costs_dict.keys():
				if self.costs_dict[tuple(newDict['self'])] > priorityToAdd:
					if not self.is_popped(tuple(newDict['self'])):
					# no need to delete lower priority (higher #) element from frontier if already popped
						tempitem = self.frontier.get()
						templist = []
						while tempitem[2]['self'] != newDict['self']:
							templist.append(tempitem) # gets everything before elt to be removed
							tempitem = self.frontier.get()
						for it in templist:
							self.frontier.put(it) # adds them back to the frontier
					self.add_to_frontier(priorityToAdd, newDict)
			else:
				self.add_to_frontier(priorityToAdd, newDict)

	# Conducts the A* search algorithm
	# In a loop, gets the highest priority (lowest #) element from frontier
	# If highest priority element is the goal_state, returns success
	# Otherwise, keeps expanding the search by making the possible flips
	# Fails only when frontier gets empty (no possible solutions left)
	def astar(self):
		self.frontier.put((0, self.unique_id, {'self': self.initial, 'prev': [], 'cumulCost': 0}))
		self.costs_dict[tuple(self.initial)] = 0
		self.unique_id += 1

		while not self.frontier.empty():
			to_expand = self.frontier.get()
			self.popped[tuple(to_expand[2]['self'])] = True

			if to_expand[2]['self'] == self.goal_state:
				return success(to_expand[2])
			
			self.expand_flips(to_expand[2])

		return failure()

# Runs the program
def execute():
	PancakesObject = Pancakes()
	PancakesObject.astar()

execute()
