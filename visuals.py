import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv("./data/data.csv")
value_counts = data.Same.value_counts().to_dict()
plt.bar(['not same', 'same'], list(value_counts.values()), color ='maroon',
        width = 0.4)
plt.title('Label Distribution in the Created Pairs')
plt.xlabel('Label')
plt.ylabel('Number of Pairs')
plt.savefig('./figures/label_hist.png')