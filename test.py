import pandas as pd
import matplotlib.pyplot as plt

# Example DataFrame
data = pd.DataFrame({'x': [0, 1, 2, 3, 4], 'height': [3, 5, 1, None, 2]})

# Handle NaN/None values
data.dropna(inplace=True)  # Replace NaN/None with a default value

# Plot
plt.bar(data['x'], data['height'], width=0.8)
plt.show()