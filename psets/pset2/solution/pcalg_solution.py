# === IMPORTS: BUILT-IN ===
import itertools as itr
from math import erf, sqrt

# === IMPORTS: THIRD-PARTY ===
import numpy as np
from numpy import corrcoef
from numpy import arctanh
from sklearn.linear_model import LinearRegression
import networkx as nx


def compute_partial_correlation(samples, i, j, S):
    if len(S) > 0:
        lr = LinearRegression(fit_intercept=True)

        # get residuals of i
        lr.fit(samples[:, S], samples[:, i])
        beta_iS = lr.coef_
        residuals_i = samples[:, i] - samples[:, S] @ beta_iS

        # get residuals of j
        lr.fit(samples[:, S], samples[:, j])
        beta_jS = lr.coef_
        residuals_j = samples[:, j] - samples[:, S] @ beta_jS
    else:
        residuals_i = samples[:, i]
        residuals_j = samples[:, j]

    return corrcoef(residuals_i, residuals_j)[0, 1]


def compute_test_statistic(samples, i, j, S):
    rho = compute_partial_correlation(samples, i, j, S)
    return np.sqrt(samples.shape[0] - len(S) - 3) * arctanh(rho)


def compute_pvalue(samples, i, j, S):
    z = compute_test_statistic(samples, i, j, S)
    return 2 * (1 - phi(np.abs(z)))


def phi(x):
    return (1.0 + erf(x / sqrt(2.0))) / 2.0


def pcalg_skeleton(samples, alpha):
    nnodes = samples.shape[1]
    current_skeleton = nx.Graph(itr.combinations(range(nnodes), 2))

    d = 0
    separator_function = {}
    while max(degree for _, degree in current_skeleton.degree()) >= d:
        for i, j in current_skeleton.edges():
            adj_i = set(current_skeleton.neighbors(i))
            adj_j = set(current_skeleton.neighbors(j))
            sets_to_test = set(itr.combinations(adj_i - {j}, r=d)) | set(itr.combinations(adj_j - {i}, r=d))

            for S in sets_to_test:
                if compute_pvalue(samples, i, j, S) > alpha:
                    current_skeleton.remove_edge(i, j)
                    separator_function[frozenset({i, j})] = S
                    break
        d += 1

    return current_skeleton, separator_function


def pcalg_orient(skeleton, separator_function):
    nnodes = len(skeleton.nodes)
    pairs = {frozenset(s) for s in itr.combinations(range(nnodes), r=2)}
    adjacent_pairs = {frozenset(s) for s in skeleton.edges()}
    nonadjacent_pairs = pairs - adjacent_pairs

    unshielded_colliders = list()
    for i, j in nonadjacent_pairs:
        s = separator_function[frozenset({i, j})]
        for k in set(skeleton.neighbors(i)) & set(skeleton.neighbors(j)):
            if k not in s:
                unshielded_colliders.append((i, k, j))
    
    return unshielded_colliders


def pcalg(samples, alpha):
    skeleton, separator_function = pcalg_skeleton(samples, alpha)

    



pcalg_samples = np.loadtxt("pcalg_samples.csv")

# === SANITY CHECKS FOR (a) and (b)
rho1 = compute_partial_correlation(pcalg_samples, 0, 6, [2, 3])
print(f"Sanity check, partial correlation for X1 and X7 given X3, X4: {rho1}")
rho2 = compute_partial_correlation(pcalg_samples, 0, 6, [])
print(f"Sanity check, partial correlation for X1 and X7: {rho2}")

# === SANITY CHECKS FOR (c)
z1 = compute_test_statistic(pcalg_samples, 0, 6, [2, 3])
print(f"Sanity check, test statistic X1 and X7 given X3, X4: {z1}")
z2 = compute_test_statistic(pcalg_samples, 0, 6, [])
print(f"Sanity check, test statistic for X1 and X7: {z2}")

# === SANITY CHECKS FOR (d)
z1 = compute_pvalue(pcalg_samples, 0, 6, [2, 3])
print(f"Sanity check, p value for X1 and X7 given X3, X4: {z1}")
z2 = compute_pvalue(pcalg_samples, 0, 6, [])
print(f"Sanity check, p value for X1 and X7: {z2}")

# === SANITY CHECKS FOR (e)
estimated_skeleton, separator_function = pcalg_skeleton(pcalg_samples, 0.05)
expected_skeleton = nx.Graph({
    (0, 2), (1, 2),
    (2, 3), (2, 4), (2, 5),
    (3, 4), (4, 5), (3, 5),
    (2, 6), (3, 6)
})
match = expected_skeleton.edges() == estimated_skeleton.edges()
print(f"Skeletons match? {match}")
print(len(estimated_skeleton.edges()))


print('===========')
# === ANSWERS FOR (a) and (b)
rho1 = compute_partial_correlation(pcalg_samples, 0, 3, [])
print(f"partial correlation for X1 and X4: {rho1}")
rho2 = compute_partial_correlation(pcalg_samples, 0, 3, [1, 2])
print(f"partial correlation for X1 and X4 given X2 and X3: {rho2}")

# === ANSWERS FOR (c)
z1 = compute_test_statistic(pcalg_samples, 0, 3, [1, 2])
print(f"test statistic for X1 and X7 given X3, X4: {z1}")

# === ANSWERS FOR (d)
z1 = compute_pvalue(pcalg_samples, 0, 3, [1, 2])
print(f"p value for X1 and X7 given X3, X4: {z1}")

# === ANSWERS FOR (e)
estimated_skeleton, separator_function = pcalg_skeleton(pcalg_samples[:500], 0.2)
print(f"Number of edges when alpha = 0.2: {len(estimated_skeleton.edges())}")

estimated_skeleton, separator_function = pcalg_skeleton(pcalg_samples[:500], 0.001)
print(f"Number of edges when alpha = 0.001: {len(estimated_skeleton.edges())}")

# === ANSWERS FOR (f)
estimated_skeleton, separator_function = pcalg_skeleton(pcalg_samples, 0.05)
unshielded_colliders = pcalg_orient(estimated_skeleton, separator_function)
print(f"Unshielded colliders: {unshielded_colliders}")