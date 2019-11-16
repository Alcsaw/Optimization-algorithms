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

    def __init__(self, items_weights, items_values, supported_weight=200, stop_after=3, rounds_for_tabu_list=3):
        self.items_weights = items_weights
        self.items_values = items_values
        self.supported_weight = supported_weight
        self.stop_after = stop_after
        self.rounds_for_tabu_list - rounds_for_tabu_list


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
                current_neighbor[i] = 0

            neighbors.append((current_neighbor.copy(), i))

        print("Neighbors of ", current_solution, ":")
        for neighbor in neighbors:
            print(neighbor[0])
        return neighbors

    # def filter_valid_neighbors(self, neighbors: list) -> list:
    #     """
    #     Returns a new list of neighbors, same as the passed as parameter, except the combinations which total weight is
    #     greater than the supported weight.
    #
    #     :param neighbors: list of 0/1 indicating if the item at each index is (1) in the knapsack or (0) not
    #     :return: valid_neighbors
    #     """
    #
    #     # "smart code" alert! Just to learn some fancy moves...
    #     # zip returns a list of tuples containing the weight of the item and a 0/1 indicating if it is in the knapsack
    #     # this list is destructured in the for loop that also makes a list comprehension for the sum() method that will
    #     # compute the total weight for the combination in the current neighbor. All of this is occurring in the for loop
    #     # of neighbors, which is another list comprehension that will return the current neighbor if the calculated sum
    #     # is lesser than the supported weight
    #
    #     valid_neighbors = [neighbor
    #                        for neighbor
    #                        in neighbors
    #                        if sum(weight * selected_items
    #                               for (weight, selected_items)
    #                               in zip(self.items_weights, neighbor[0]))
    #                        < self.supported_weight]
    #     return valid_neighbors
    #
    #     # same as:
    #     # to_remove = []
    #     #
    #     # for neighbor_index, neighbor in enumerate(neighbors):
    #     #     weight = 0
    #     #     for index, item in enumerate(neighbor[0]):
    #     #         if item == 1:
    #     #             weight = weight + self.items_weights[index]
    #     #         if weight > self.supported_weight:
    #     #             to_remove.append(neighbor_index)
    #     # for item in to_remove:
    #     #     neighbors.remove(item)
    #
    # def calc_utility(self, item_combination: list) -> int:
    #     """
    #     Computes the utility of a given combination of items
    #
    #     :param item_combination: list of 0/1 indicating if the item at each index is (1) in the knapsack or (0) not
    #     :return: utility - a number that is the sum of the utility of each item in the knapsack for a given combination
    #     """
    #     utility = 0
    #     for index, item in enumerate(item_combination):
    #         if item == 1:
    #             utility = utility + self.item_values[index]
    #     return utility

    def select_neighbor(self, neighbors: list):
        greater_utility_in_neighbors = 0
        selected_neighbor = 0
        tabu_index = 0

        for neighbor_index, neighbor in enumerate(neighbors):
            # walks for each neighbor and filter the valid ones (supported weight) while also computing its utility
            current_weight = 0
            current_utility = 0
            valid_neighbor = True

            for index, item in enumerate(neighbor[0]):
                if item == 1:
                    current_weight = current_weight + self.items_weights[index]
                    current_utility = current_utility + self.items_values[index]
                if current_weight > self.supported_weight:
                    valid_neighbor = False
                    break

            if valid_neighbor:
                if current_utility > self.best_utility:
                    # aspiration criteria: it doesn't matter if the neighbor was in the tabu list, because its utility
                    # is the best so far
                    self.best_utility = current_utility
                    self.best_solution = neighbor[0]

                    # so it's the best utility and the selected_neighbor
                    greater_utility_in_neighbors = current_utility
                    selected_neighbor = neighbor

                elif current_utility > greater_utility_in_neighbors and neighbor[1] not in self.tabu_list:
                    # normal cases need to respect the tabu list
                    greater_utility_in_neighbors = current_utility
                    selected_neighbor = neighbor

        # and return only the item combination of the neighbor and its changed index so we can append it to the tabu
        # list later
        return selected_neighbor

    def get_initial_solution(self) -> list:
        """
        Gets the initial solution using Greedy algorithm
        :return: a list of 0/1 with the same size of the items_weight
        """
        total_weight = 0
        initial_solution = []
        for item in self.items_weights:
            initial_solution.append(0 if total_weight >= self.supported_weight else 1)
            total_weight += item

        return initial_solution

    def compute(self):
        if len(self.items_weights) != len(self.items_values):
            print("ERROR: invalid input. The length of items_weight is different of the the length of items_values")
            return False
        current_solution = self.get_initial_solution()
        for i in range(self.stop_after):
            # starts the iteration process to get the best solution

            if len(self.tabu_list) and (i - self.tabu_list[0][0] > self.rounds_for_tabu_list):
                # checks if the oldest item in the tabu_list is already old enough to be removed from it and remove it
                # Just a reminder: at each iteration, only 1 item is added to the tabu list, so we only need to
                # check the first one of the list
                self.tabu_list.pop(0)

            neighbors = self.get_all_local_neighbors(current_solution)
            selected_neighbor = self.select_neighbor(neighbors)
            print("selected_neighbor: ", selected_neighbor)
            current_solution = selected_neighbor[0]

            # append the changed index of the selected_neighbor and the current iteration counter to the tabu_list
            # This control is done here and not in the select_neighbor method because we need to track how many
            # iterations an item index must stay on the tabu list
            self.tabu_list.append((selected_neighbor[1], i))
            print("tabu_list: ", self.tabu_list)
            print("best solution so far: ", self.best_solution)
            print("best solution's utility: ", self.best_utility)
        return self.best_solution


def main():

    items_weights = [64, 12, 22, 30, 50, 4, 2, 7, 14, 21, 90, 55, 44, 33, 22, 11]
    items_values = [70, 20, 20, 40, 2, 5, 8, 8, 9, 20, 30, 40, 50, 44, 55, 16]
    tabu_search = TabuSearch(items_weights, items_values)
    tabu_search.compute()

    print("Best solution: ", tabu_search.best_solution)
    print("best solution's utility: ", tabu_search.best_utility)


if __name__ == "__main__":
    main()
