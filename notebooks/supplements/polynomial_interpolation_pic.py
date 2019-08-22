import numpy as np
import matplotlib.pyplot as plt

def P(x):
    return 0.5*(x**4 - 2*x**2 + x + 3)

x = np.linspace(-2 , 2.2, 200)
xpts = np.array([-1, 0, 1, 2])
ypts = P(xpts)
fig = plt.figure(figsize=(5,5))
xmin, xmax =  np.min(x) - 0.5, np.max(x) + 0.5
ymin, ymax =  np.min(y) - 2, np.max(y) + 2
plt.xlim(xmin, xmax)
plt.ylim(ymin, ymax)
ax = plt.gca()
ax.set_xticklabels([])
ax.set_yticklabels([])
plt.grid(ls="-", lw=0.5, alpha=0.5)
plt.plot(x, P(x), '--', lw=4, color = "steelblue", alpha = 1, zorder = 10)
plt.text(xpts[0] + 0.1, ypts[0] - 0.7, r'$(x_1, y_1)$', size=16)
plt.text(xpts[1] - 0.9, ypts[1] + 0.4, r'$(x_2, y_2)$', size=16)
plt.text(xpts[2], ypts[2] - 0.9, r'$(x_3, y_3)$', size=16)
plt.text(xpts[3] - 1, ypts[3], r'$(x_4, y_4)$', size=16)

plt.plot(xpts, ypts, "o", markerfacecolor='r', markeredgecolor="steelblue",  ms=12, zorder = 20)
plt.tight_layout(pad=0)
plt.savefig("test.svg")
