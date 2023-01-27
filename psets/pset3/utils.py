# === IMPORTS: BUILT-IN ===
from math import erf, sqrt

# === IMPORTS: THIRD-PARTY ===
import numpy as np
from numpy import corrcoef
from numpy import arctanh
from sklearn.linear_model import LinearRegression


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