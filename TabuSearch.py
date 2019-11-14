from operator import itemgetter


class TabuSearch:
    """
    Global variables definition:
    - itemsWeight is a list with the weight of each item available;
    - itemsValue is a list with the value of each item available;
    - tabu_list is... the tabu list!
    - supported_weight is an integer that limits how much weight we can carry in the knapsack, i.e., the sum of weights
    for all items in a given solution cannot be greater then this value;
    """
    items_weights = []
    items_values = []
    tabu_list = []  # stores the index that was changed in a given solution to create a neighbor that became the new
    # solution. This index should not be changed anymore for new neighbors
    rounds_for_tabu_list = 3    # parameter that defines how many rounds an item should remain in tabu_list
    supported_weight = 200
    best_utility = 0
    best_solution = []
    stop_after = 50     # stop condition: repeats the algorithm for stop_after times
    # TODO: add another stop condition for number of rounds without best_solution change. E.g. stop after 5 rounds
    #   without changing the best_solution

    """
    possible better data structure?
    a list of dicts, which each dict has the following structure:
    {
        'item_name': 'Teddy Bear',
        'item_value': 980,
        'item_weight': 2,
        'is_in_knapsack': True
    }
    """

    def get_all_local_neighbors(self, current_solution: list) -> list:
        """
        Get all possible neighbors for a given solution
        :param current_solution: list of 0/1
        :return neighbors: list of tuples (lists of 0/1, changed_index)
        """
        neighbors = []
        for i in range(len(current_solution)):
            current_neighbor = current_solution.copy()
            if current_solution[i] == 0:
                current_neighbor[i] = 1
            else:
                current_neighbor = 0

            neighbors.append((current_neighbor.copy(), i))

        print("Neighbors of ", current_solution, ":")
        for neighbor in neighbors:
            print(neighbors[0])
        return neighbors

    def filter_valid_neighbors(self, neighbors: list) -> list:
        """
        Returns a new list of neighbors, same as the passed as parameter, except the combinations which total weight is
        greater than the supported weight.

        :param neighbors: list of 0/1 indicating if the item at each index is (1) in the knapsack or (0) not
        :return: valid_neighbors
        """

        # "smart code" alert! Just to learn some fancy moves...
        # zip returns a list of tuples containing the weight of the item and a 0/1 indicating if it is in the knapsack
        # this list is destructured in the for loop that also makes a list comprehension for the sum() method that will
        # compute the total weight for the combination in the current neighbor. All of this is occurring in the for loop
        # of neighbors, which is another list comprehension that will return the current neighbor if the calculated sum
        # is lesser than the supported weight

        valid_neighbors = [neighbor
                           for neighbor
                           in neighbors
                           if sum(weight * selected_items
                                  for (weight, selected_items)
                                  in zip(self.items_weights, neighbor[0]))
                           < self.supported_weight]
        return valid_neighbors

        # same as:
        # to_remove = []
        #
        # for neighbor, neighbor_index in enumerate(neighbors):
        #     weight = 0
        #     for item, index in enumerate(neighbor[0]):
        #         if item == 1:
        #             weight = weight + self.items_weights[index]
        #         if weight > self.supported_weight:
        #             to_remove.append(neighbor_index)
        # for item in to_remove:
        #     neighbors.remove(item)

    def calc_utility(self, item_combination: list) -> int:
        """
        Computes the utility of a given combination of items

        :param item_combination: list of 0/1 indicating if the item at each index is (1) in the knapsack or (0) not
        :return: utility - a number that is the sum of the utility of each item in the knapsack for a given combination
        """
        utility = 0
        for item, index in enumerate(item_combination):
            if item == 1:
                utility = utility + self.item_values[index]
        return utility

    def select_neighbor(self, neighbors: list) -> list:
        greater_utility_in_neighbors = 0
        selected_neighbor = 0
        tabu_index = 0

        for neighbor, neighbor_index in enumerate(neighbors):
            current_weight = 0
            current_utility = 0
            valid_neighbor = True

            for item, index in enumerate(neighbor[0]):
                if item == 1:
                    current_weight = current_weight + self.items_weights[index]
                    current_utility = current_utility + self.items_values[index]
                if current_weight > self.supported_weight:
                    valid_neighbor = False
                    break

            if valid_neighbor:
                if current_utility > self.best_utility:
                    self.best_utility = current_utility
                    self.best_solution = neighbor[0]

                    # aspiration criteria: it doesn't matter if the neighbor was in the tabu list, because its utility
                    # is the best so far
                    greater_utility_in_neighbors = current_utility
                    selected_neighbor = neighbor
                # normal cases need to respect the tabu list
                elif current_utility > greater_utility_in_neighbors and neighbor[1] not in self.tabu_list:
                    greater_utility_in_neighbors = current_utility
                    selected_neighbor = neighbor

        self.tabu_list.append(selected_neighbor[1])
