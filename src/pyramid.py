import pandas as pd
import matplotlib.pyplot as plt
def population_pyramid(row: pd.Series, bins=[(0,14),(15,64),(65,100)], title=None):
  labels=[f"{a}-{b if b<100 else '+'}" for a,b in bins]
  male=[row[f"pop_{a:02d}_{b:02d}_male"] for a,b in bins]
  female=[row[f"pop_{a:02d}_{b:02d}_female"] for a,b in bins]
  y=list(range(len(bins)))
  plt.barh(y, [-m for m in male], label="Male", alpha=0.8)
  plt.barh(y, female, label="Female", alpha=0.8)
  plt.yticks(y, labels)
  plt.xlabel("Population")
  if title: plt.title(title)
  plt.legend()
  plt.tight_layout()
  plt.show()