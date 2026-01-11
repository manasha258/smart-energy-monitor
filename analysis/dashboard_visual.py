import csv
import matplotlib.pyplot as plt

# CSV file path
file_path = "../data/daily_usage.csv"

appliance_units = {}
dates = []

# Read CSV and aggregate units per appliance
with open(file_path, mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        appliance = row["Appliance"]
        units = float(row["Units_Consumed"])
        date = row["Date"]

        if appliance not in appliance_units:
            appliance_units[appliance] = {}
        if date not in appliance_units[appliance]:
            appliance_units[appliance][date] = 0

        appliance_units[appliance][date] += units

        if date not in dates:
            dates.append(date)

# Define fixed colors for appliances
colors = {
    "Fan": "blue",
    "Light": "yellow",
    "AC": "red"
}

# Plot bar graph per appliance
plt.figure(figsize=(10, 6))
for appliance in appliance_units:
    values = [appliance_units[appliance][d] for d in dates]
    plt.bar(dates, values, label=appliance, color=colors[appliance])
plt.title("Daily Electricity Usage by Appliance", fontsize=16)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Units Consumed", fontsize=12)
plt.legend(loc="upper right")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()

# Plot total daily usage line chart
total_units_per_day = []
for d in dates:
    total = sum(appliance_units[a][d] for a in appliance_units)
    total_units_per_day.append(total)

plt.figure(figsize=(10, 6))
plt.plot(dates, total_units_per_day, marker='o', color='red', linewidth=2)
plt.title("Total Daily Electricity Usage", fontsize=16)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Units Consumed", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()
