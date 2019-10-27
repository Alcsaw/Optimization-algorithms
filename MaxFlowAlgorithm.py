"""
 Data Structure: list of lists, in which the order of the objects in the external list doesn't matter and
 each internal list is composed by: origin_node;destiny_node;potential_flow
 Input is a CSV file separated by semicolons.
"""
            
            
def get_graph(input_file):
    # gets the graph from an input_file and determine the first and last nodes
    import csv
    graph = []
    FIRST_NODE = 10
    LAST_NODE = 0
    
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for line in csv_reader:
            line = list(map(int, line))
            graph.append(line)
            if line[0] < FIRST_NODE:
                FIRST_NODE = line[0]
            if line[1] > LAST_NODE:
                LAST_NODE = line[1]
        return graph, FIRST_NODE, LAST_NODE


# Identify potential flow remaining
def check_residual_network():
    residual = False
    flag_residual_from_first = False
    flag_residual_to_last = False

    print("\n\nchecking residual network:")
    for path in graph:
        if path[0] == FIRST_NODE and path[2] > 0:
            flag_residual_from_first = True
            print("flow remaining from: ", path)
        if path[1] == LAST_NODE and path[2] > 0:
            flag_residual_to_last = True
            print("flow remaining to: ", path)
        if flag_residual_from_first and flag_residual_to_last:
            break
    
    return flag_residual_from_first and flag_residual_to_last


def get_one_path():
    """
    returns entire_path_flow which is a List with an entire path on the graph, from FIRST_NODE to LAST_NODE
            the list is composed by [[next_node, flow_amount], [..., ...]] until next_node is the same as the LAST_NODE
    """
    entire_path_flow = []
    pointer = 0     # controls the position on the entire_path_flow (sequence on the path)
    current_node = FIRST_NODE
    blocked_paths = [FIRST_NODE]
    print("getting an entire path")

    while current_node < LAST_NODE:
        # entire_path_flow[pointer] = 0
        entire_path_flow.append([0, 0])
        
        chosen_path = None
        
        print("current_node: ", current_node)
        for path in graph:
            print("path: ", path)

            # If there is potential flow starting from the current node, gets the higher or, if there is an equally potential flow but that goes farther, gets it
            if ((path[0] == current_node and path[2] > entire_path_flow[pointer][1]) or (path[0] == current_node and path[2] == entire_path_flow[pointer][1] and path[1] > entire_path_flow[pointer][0] and path[2] > 0)) and path[1] not in blocked_paths:
                # Also, only chooses paths that are not already known
                
                # to where ([1] and how much flow [2]
                chosen_path = [path[1], path[2]]
                print("chosen_path: ", chosen_path)
                
                entire_path_flow[pointer] = chosen_path
        
        if chosen_path is None:
            print("chosen_path is still NONE!")
            entire_path_flow.pop()  # removes the [0, 0] added
            pointer -= 1            # and rewind the pointer
            if len(entire_path_flow) == 0:
                # This will occur when every possible intermediate node (after the first) has exhausted and,
                # although the first node is still capable of sending more flow, we cannot go any further
                return False
            blocked_node = entire_path_flow.pop()
            pointer -= 1            # again we removed one element of the list, so we need to adjust the pointer
            blocked_paths.append(blocked_node[0])
            if len(entire_path_flow) == 0:  # In some cases, we may need to go back to the first node
                current_node = FIRST_NODE
            else:
                current_node = entire_path_flow[pointer][0]
            pointer += 1
            continue
        else:
            blocked_paths.append(chosen_path[0])
            print("blocked_paths: ", blocked_paths)
        
            # Got the best path from the current node, so the next "current_node" is the destiny (the node inserted on the entire_path_flow)
            print("entire_path_flow: ", entire_path_flow)
            current_node = entire_path_flow[pointer][0]
        
            pointer += 1    # updates the pointer
        
    # checks the minimum supported flow
    supported_flow = entire_path_flow[0][1]

    for node in entire_path_flow:
        # updates the supported_flow to the least potential on the path
        if node[1] < supported_flow:
            supported_flow = node[1]
    print("supported_flow: ", supported_flow)

    # updates the entire_path_flow, setting all paths with the correct flow amount
    for node in entire_path_flow:
        node[1] = supported_flow
        
    return entire_path_flow


def update_graph(entire_path_flow):
    # Updates the graph - discounts the flow throughout the entire_path_flow on the graph
    current_node = FIRST_NODE
    print("Updating the graph")

    for next_node in entire_path_flow:
        print("current_node: ", current_node)
        print("next_node: ", next_node)

        for path in graph:
            # if the path is the one selected - i.e. if the origin is the current_node and the destiny is the next_node
            if path[0] == current_node and path[1] == next_node[0]:
                # updates the remaining potential flow (discounts the flow on the selected path)
                path[2] = path[2] - next_node[1]
        current_node = next_node[0]


# graph = [[]]
#graph, FIRST_NODE, LAST_NODE = get_graph('MaxFlowSampleData.csv');
graph, FIRST_NODE, LAST_NODE = get_graph('MaxFlowInput.csv');
print("graph:", graph)

print("FIRST_NODE: ", FIRST_NODE)
print("LAST_NODE: ", LAST_NODE)

# while flow remaining: iterate through paths (minimum amount) and update residual network
paths_taken = []
max_flow = 0

while check_residual_network():

    entire_path_flow = get_one_path()
    if entire_path_flow is False:
        break
    else:
        paths_taken.append(entire_path_flow)
    max_flow += entire_path_flow[0][1]
    print("Entire path discovered: ", entire_path_flow)

    update_graph(entire_path_flow)
    print("Updates graph: ", graph)

print("Paths taken: ", paths_taken)
print("Max Flow: ", max_flow)
