import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import datetime

# Load CSV
df = pd.read_csv("../data/daily_usage.csv")

# Convert Date to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Group per appliance per day
daily = df.groupby(['Date','Appliance'])['Units_Consumed'].sum().reset_index()

# Pivot table: Date vs Appliance
pivot = daily.pivot(index='Date', columns='Appliance', values='Units_Consumed').fillna(0)

# Linear Regression prediction
predictions = {}
for appliance in pivot.columns:
    pivot['DayNum'] = range(len(pivot))
    X = pivot['DayNum'].values.reshape(-1,1)
    y = pivot[appliance].values
    model = LinearRegression()
    model.fit(X, y)
    
    next_day = [[len(pivot)]]
    pred_units = model.predict(next_day)[0]
    predictions[appliance] = max(pred_units,0)

# Print predicted units
print("\nPREDICTED ENERGY USAGE FOR NEXT DAY:")
for appliance, units in predictions.items():
    print(f"{appliance}: {units:.3f} units")

# Plot Last Day vs Predicted Next Day
plt.figure(figsize=(8,5))
last_day = pivot.index[-1]
plt.bar(pivot.columns, pivot.iloc[-1], color=['blue','yellow','red'], alpha=0.6, label='Last Day')
plt.bar(predictions.keys(), predictions.values(), color=['blue','yellow','red'], alpha=0.3, label='Predicted Next Day')
plt.ylabel("Units Consumed")
plt.title("Actual vs Predicted Energy Usage")
plt.legend()
plt.show()
