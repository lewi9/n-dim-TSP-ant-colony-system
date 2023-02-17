import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

points = pd.read_csv("points.txt", sep='\t', names=["distance","cost"])
paretoFront = pd.read_csv("paretoFront.txt", sep='\t', names=["distance","cost"])

fig,ax = plt.subplots(1,1)
ax.scatter(x = points["distance"], y = points["cost"], c = "blue", alpha = 0.1)
ax.scatter(x = paretoFront["distance"], y = paretoFront["cost"], c = "red", s = 100, alpha = 0.3)
plt.show()