import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.title("Smart Energy Monitoring Dashboard")

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("../data/daily_usage.csv")
df['Date'] = pd.to_datetime(df['Date'])

# Appliances list
appliances = df['Appliance'].unique().tolist()
selected_appliance = st.sidebar.selectbox("Select Appliance", appliances)

# Date range selector
min_date = df['Date'].min()
max_date = df['Date'].max()
start_date = st.sidebar.date_input("Start Date", min_date)
end_date = st.sidebar.date_input("End Date", max_date)

# Filter data by date range
mask = (df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))
data_filtered = df[mask]

# Group by Date
daily = data_filtered.groupby(['Date','Appliance'])['Units_Consumed'].sum().reset_index()
pivot = daily.pivot(index='Date', columns='Appliance', values='Units_Consumed').fillna(0)

# -----------------------------
# Show Selected Appliance Trend
# -----------------------------
st.subheader(f"Usage Trend for {selected_appliance}")
st.line_chart(pivot[selected_appliance])

# -----------------------------
# Predict Next Day Usage
# -----------------------------
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

st.subheader("Predicted Next Day Usage")
for appliance, units in predictions.items():
    st.write(f"{appliance}: {units:.3f} units")

# -----------------------------
# Last Day vs Predicted Bar Chart
# -----------------------------
fig, ax = plt.subplots(figsize=(8,5))
last_day = pivot.index[-1]
ax.bar(pivot.columns, pivot.iloc[-1], color=['blue','yellow','red'], alpha=0.6, label='Last Day')
ax.bar(predictions.keys(), predictions.values(), color=['blue','yellow','red'], alpha=0.3, label='Predicted Next Day')
ax.set_ylabel("Units Consumed")
ax.set_title("Actual vs Predicted Usage")
ax.legend()
st.pyplot(fig)

# -----------------------------
# Historical Trend Analytics
# -----------------------------
st.subheader("Historical Trend Analytics")

# Weekly trend
weekly = pivot.resample('W').sum()
st.line_chart(weekly)

# Monthly trend
monthly = pivot.resample('M').sum()
st.line_chart(monthly)
