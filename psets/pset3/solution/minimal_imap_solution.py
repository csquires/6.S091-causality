# === IMPORTS: BUILT-IN ===
import os
import itertools as itr

# === IMPORTS: THIRD-PARTY ===
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# === IMPORTS: LOCAL ===
from utils import compute_pvalue


def minimal_imap(samples, permutation, alpha):
    d = nx.DiGraph()
    # d.add_nodes_from(permutation)

    for u, v in itr.combinations(range(len(permutation)), r=2):
        i = permutation[u]
        j = permutation[v]
        S = permutation[:u] + permutation[(u+1):v]
        pval = compute_pvalue(samples, i, j, S)
        if pval <= alpha:
            d.add_edge(i+1, j+1)
    
    return d


if __name__ == "__main__":
    imap_samples = np.loadtxt("imap_samples.csv")
    g12345 = minimal_imap(imap_samples, [0, 1, 2, 3, 4], 0.05)
    print(g12345.edges())

    g54123 = minimal_imap(imap_samples, [4, 3, 0, 1, 2], 0.05)
    print(g54123.edges())

    g54321 = minimal_imap(imap_samples, [4, 3, 2, 1, 0], 0.05)
    print(g54321.edges())

    
    draw_options = dict(
        with_labels=True,
        node_size=600,
        arrowsize=20,
        font_size=20
    )
    fig, axes = plt.subplots(1, 3)
    fig.set_size_inches(9, 3)
    os.makedirs("minimal_imap_outputs", exist_ok=True)
    pos = nx.circular_layout(g12345)
    nx.draw(g12345, pos, ax=axes[0], **draw_options)
    nx.draw(g54123, pos, ax=axes[1], **draw_options)
    nx.draw(g54321, pos, ax=axes[2], **draw_options)
    axes[0].set_title("$\mathcal{G}_{\pi_a}$")
    axes[1].set_title("$\mathcal{G}_{\pi_b}$")
    axes[2].set_title("$\mathcal{G}_{\pi_c}$")
    plt.savefig("minimal_imap_outputs/minimal_imaps.pdf")


    g1 = g12345
    g2 = g12345.copy()
    g2.add_edge(5, 4)
    g3 = g2.copy()
    g3.remove_edge(1, 5)
    g3.add_edge(5, 1)
    g4 = g54123

    fig, axes = plt.subplots(1, 4)
    fig.set_size_inches(12, 3)
    nx.draw(g1, pos, ax=axes[0], **draw_options)
    nx.draw(g2, pos, ax=axes[1], **draw_options)
    nx.draw(g3, pos, ax=axes[2], **draw_options)
    nx.draw(g4, pos, ax=axes[3], **draw_options)
    plt.savefig("minimal_imap_outputs/chickering_sequence.pdf")