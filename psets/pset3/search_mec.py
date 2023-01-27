import numpy as np
import networkx as nx


def covered_edge_neighbors(dag):
    # TODO
    pass


def search_mec(starting_dag, ending_dag):
    # TODO
    pass


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

    # PART B
    for starting_dag, ending_dag in examples:
        path = search_mec(starting_dag, ending_dag)
        print(f"Length of path: {len(path)}")