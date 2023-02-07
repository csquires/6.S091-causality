import numpy as np
import networkx as nx


def covered_edge_neighbors(dag):
    covered_edges = {
        (i, j) for i, j in dag.edges()
        if set(dag.predecessors(i)) == set(dag.predecessors(j)) - {i}
    }

    neighbors = []
    for (i, j) in covered_edges:
        dag2 = dag.copy()
        dag2.remove_edge(i, j)
        dag2.add_edge(j, i)
        neighbors.append(dag2)
    
    return neighbors


def search_mec(starting_dag, ending_dag):
    starting_state = frozenset(starting_dag.edges())
    state2path = {starting_state: [starting_state]}
    state2dag = {starting_state: starting_dag}
    
    queue = [starting_state]
    visited = set(starting_state)
    while queue:
        current_state = queue.pop(0)
        current_dag = state2dag[current_state]
        current_path = state2path[current_state]

        for new_dag in covered_edge_neighbors(current_dag):
            new_state = frozenset(new_dag.edges())

            if new_state not in visited:
                # UPDATE DICTIONAREIS
                # print(len(current_path))
                new_path = current_path + [current_state]
                state2path[new_state] = new_path
                state2dag[new_state] = new_dag

                # UPDATE DEPTH-FIRST SEARCH PARAMETERS
                queue.append(new_state)
                visited.add(new_state)

                if set(new_dag.edges()) == set(ending_dag.edges()):
                    return new_path



if __name__ == "__main__":
    num_examples = 3

    examples = []
    for ix in range(num_examples):
        a1 = np.loadtxt(f"mec_examples/starting_dag{ix}.csv")
        a2 = np.loadtxt(f"mec_examples/ending_dag{ix}.csv")
        starting_dag = nx.from_numpy_array(a1, create_using=nx.DiGraph)
        ending_dag = nx.from_numpy_array(a2, create_using=nx.DiGraph)
        examples.append((starting_dag, ending_dag))

    # PART A
    for starting_dag, _ in examples:
        num_neighbors = len(covered_edge_neighbors(starting_dag))
        print(f"Number of neighbors: {num_neighbors}")

    # PART B
    for starting_dag, ending_dag in examples:
        path = search_mec(starting_dag, ending_dag)
        print(f"Length of path: {len(path) - 1}")
    


