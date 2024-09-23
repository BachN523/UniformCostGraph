import time

# Class VacuumWorld represents the Problem Space
# Problem Space: a 4x5 Grid for a Vacuum Cleaner
class VacuumWorld:
    ROWS = 4  
    COLUMNS = 5  
    ACTION_COSTS = {
        'Left': 1.0,
        'Right': 0.9,
        'Up': 0.8,
        'Down': 0.7,
        'Suck': 0.6
    }
    ACTIONS = ['Left', 'Right', 'Up', 'Down', 'Suck']

    def __init__(self, initial_position, dirty_squares):
        self.grid = [[' ' for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
        self.agent_position = initial_position
        self.dirty_squares = set(dirty_squares)
        self.total_cost = 0.0
        self.place_agent(initial_position)
        self.place_dirt()
        self.expanded_nodes = []  # To store first 5 expanded nodes
        self.nodes_expanded_count = 0  # Count total number of nodes expanded
        self.nodes_generated_count = 0  # Count total number of nodes generated
        self.execution_time = 0.0  # To store CPU execution time

    def place_agent(self, position):
        row, col = position
        self.grid[row-1][col-1] = 'A'  # Place the agent in the grid
    
    def place_dirt(self):
        for row, col in self.dirty_squares:
            self.grid[row-1][col-1] = 'D'  # Mark the grid as dirty (D)

    def move_agent(self, direction, agent_position, dirty_squares):
        row, col = agent_position

        # Suck' action with action cost 
        if direction == 'Suck':
            if (row, col) in dirty_squares:
                dirty_squares.remove((row, col)) 
            return (row, col), dirty_squares, self.ACTION_COSTS[direction]

        # Movement with action cost
        if direction == 'Left' and col > 1:
            col -= 1
        elif direction == 'Right' and col < self.COLUMNS:
            col += 1
        elif direction == 'Up' and row > 1:
            row -= 1
        elif direction == 'Down' and row < self.ROWS:
            row += 1

        # Return new agent position, dirty squares, and the cost of the action
        return (row, col), dirty_squares, self.ACTION_COSTS[direction] # State / Node

    def is_goal(self, dirty_squares):
        return len(dirty_squares) == 0

def expand(node, problem):
    agent_position, dirty_squares, cost, path = node # state[node]
    
    successors = []

    for action in problem.ACTIONS:
        # Perform Action
        next_position, next_dirty_squares, next_cost = problem.move_agent(action, agent_position, dirty_squares.copy())

        # Get next_node's Path
        next_path = path + [action]

        next_node = (next_position, next_dirty_squares, cost + next_cost, next_path)
        successors.append(next_node)
    
    problem.nodes_generated_count += len(successors) # Record total nodes generated
    
    return successors

# Uniform Cost Graph Searching Algorithm for VacuumWorld
def uniform_cost_graph_search(problem):
    fringe = [(problem.agent_position, problem.dirty_squares, 0, [])] # Initial State
    closed = set() # Today I learned sets are not hashable but frozensets are 

    path = [] # To be returned as the Solution

    # While fringe is not Empty
    while fringe: 
        # Pop out the node with the lowest cost (node[2])
        node = min(fringe, key=lambda x: x[2]) 
        fringe.remove(node)
        agent_position, dirty_squares, total_cost, path = node # state[node] 

        # Record the first 5 expanded nodes, the number of total nodes expanded
        if (len(problem.expanded_nodes) < 5): problem.expanded_nodes.append((agent_position, path))
        
        # Count total nodes expanded
        problem.nodes_expanded_count += 1
        
        if problem.is_goal(dirty_squares): return path # Solution Found
        
        # if state[node] not in closed 
        if (agent_position, frozenset(dirty_squares)) not in closed:
            closed.add((agent_position, frozenset(dirty_squares)))
            fringe.extend(expand(node, problem))

    return None # Solution not Found

"""     Helper Functions #1: Displays Information on Solution        """
# For Output 
# 1) First 5 search nodes 
def print_summary(self, solution):
        print("First 5 expanded search nodes:")
        for idx, (position, path) in enumerate(self.expanded_nodes):
            print(f"Node {idx + 1}:")
            print(f"  Agent Position: {position}")
            print(f"  Path: {path}")
            print()

# 2) total node expanded 
        print(f"Total number of nodes expanded: {self.nodes_expanded_count}")
    
# 3) total node generated 
        print(f"Total number of nodes generated: {self.nodes_generated_count}")
    
# 4) execution time 
        print(f"CPU execution time: {self.execution_time:.6f} seconds")

# 5) Solution Output
        if solution:
    
            # Run the solution path to calculate total cost
            agent_position = self.agent_position
            dirty_squares = self.dirty_squares.copy()
            total_cost = 0.0

            for action in solution:
                agent_position, dirty_squares, action_cost = self.move_agent(action, agent_position, dirty_squares)
                total_cost += action_cost

            # Print Sequence of Moves, Total Number of Moves, Total Cost of Solution 
            print("Sequence of moves:", " -> ".join(solution))

            print(f"Total number of moves: {len(solution)}")
            print(f"Total cost of solution: {total_cost:.2f}")
        else:
            print("Solution wasn't found.")

""" Helper Functions #2: Function to run UCGS on seperate Vacuum World Instances"""
def run_vacuum_world(initial_position, dirty_squares):
    
    # Initialize the vacuum world
    vacuum_world = VacuumWorld(initial_position, dirty_squares)

    # Measure the CPU execution time
    start_time = time.time()

    # Perform iterative deepening search
    solution = uniform_cost_graph_search(vacuum_world)

    # Record the end time and calculate the CPU execution time
    end_time = time.time()
    vacuum_world.execution_time = end_time - start_time

    # Print the summary for the instance
    print_summary(vacuum_world, solution)

"""     Test     """
# Instance #1 
initial_position_1 = (2, 2)
dirty_squares_1 = [(1, 2), (2, 4), (3, 5)]

# Instance #2
initial_position_2 = (3, 2)
dirty_squares_2 = [(1,2), (2,1), (2,4), (3,3)]

# Found solution

print("Instance 1")
run_vacuum_world(initial_position_1, dirty_squares_1)

print("\n\n\n")

print("Instance 2")
run_vacuum_world(initial_position_2, dirty_squares_2)