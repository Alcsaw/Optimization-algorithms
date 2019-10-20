# Create graph -> Identify nodes

# JSON array:
'''
[
    {
        node: 1,
        connections: [
            {
                destiny: 4,
                cost: 10
            },
            {
                destiny: 5,
                cost: 11,
            },
             
         ]
    },
    { node: 2, connections: [{}]},
]
... not worth it converting...
'''

# Matriz, sendo que a ordem em que os vetores aparecem no vetor mais externo não importa. cada vetor interno tem a estrutura: origem, destino, custo; Leitura a partir do CSV...
graph = [[]]
FIRST_NODE = 10
LAST_NODE = 0

def identify_first_and_last_nodes():
    
    for path in graph:
        if path[0] < FIRST_NODE:
            FIRST_NODE = path[0]
        if path[1] > LAST_NODE:
            LAST_NODE = path[1]

# Identify potential flow remaining
def check_residual_network():
    residual = False
    flag_residual_from_first = False
    flag_residual_to_last = False

    for path in graph:
        if path[0] == FIRST_NODE and path[2] > 0:
            flag_residual_from_first = True
        if path[1] == LAST_NODE and path[2] > 0:
            flag_residual_to_last = True
        if flag_residual_from_first and flag_residual_to_last:
            break
    
    return flag_residual_from_first and flag_residual_to_last
        

# while flow remaining: iterate through paths (minimum amount) and update residual network

entire_path_flow = []
pointer = 0     # controls the position on the entire_path_flow (sequence on the path)
current_node = FIRST_NODE

#while check_residual_network():
while current_node < LAST_NODE:
    # entire_path_flow[pointer] = 0
    entire_path_flow.append(0)
    
    for path in graph:
        # If there is potential flow starting from the current node, gets the higher
        if path[0] == current_node and path[2] > entire_path_flow[pointer]:
            # to where ([1] and how much flow [2]
            chosen_path = [path[1], path[2]]
            entire_path_flow.insert[pointer] = chosen_path
    
    # Got the best path from the current node, so the next "current_node" is the destiny (the node inserted on the entire_path_flow)
    current_node = entire_path_flow[pointer][0]
    
    pointer += 1    # updates the pointer
    
    #TODO: verify when the path is blocked and we need to go back 1 node
    
# checks the minimum supported flow
supported_flow = entire_path_flow[0][1]

for node in entire_path_flow:
    # updates the supported_flow to the least potential on the path
    if node[1] < supported_flow:
        supported_flow = node[1]

# updates the entire_path_flow, setting all paths with the correct flow amount
for node in entire_path_flow:
    node[1] = supported_flow

# Updates the graph - discounts the flow throughout the entire_path_flow on the graph
current_node = FIRST_NODE

for next_node in entire_path_flow:

    for path in graph:
        # if the path is the one selected
        if path[0] == current_node and path[1] == next_node[0]
            # updates the remaining potential flow
            path[2] = path[2] - next_node[1]
    
