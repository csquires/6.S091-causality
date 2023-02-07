import numpy as np

import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


samples = np.loadtxt("nongaussian_samples.csv")

lr = LinearRegression(fit_intercept=False)
lr.fit(X=samples[:, [0]], y=samples[:, 1])
beta_12 = lr.coef_
print(f"beta_12 = {beta_12}")
lr.fit(X=samples[:, [1]], y=samples[:, 0])
beta_21 = lr.coef_
print(f"beta_21 = {beta_21}")

plt.clf()
fig, axes = plt.subplots(1, 2)
fig.set_size_inches(8, 4)
axes[0].scatter(samples[:, 0], samples[:, 1] - beta_12 * samples[:, 0])
axes[0].set_xlabel("$X_1$")
axes[0].set_ylabel("$X_2 - \widehat{\\beta}_{12} X_1$")

axes[1].scatter(samples[:, 1], samples[:, 0] - beta_21 * samples[:, 1])
axes[1].set_xlabel("$X_2$")
axes[1].set_ylabel("$X_1 - \widehat{\\beta}_{21} X_2$")

plt.tight_layout()
plt.savefig("residuals.png")