import time
import csv
from datetime import datetime

# Appliance power ratings (Watts)
appliances = {
    "Fan": 75,
    "Light": 15,
    "AC": 1500
}

# Appliance states
appliance_state = {
    "Fan": False,
    "Light": False,
    "AC": False
}

# Usage time in seconds
usage_time = {
    "Fan": 0,
    "Light": 0,
    "AC": 0
}

csv_file = "../data/daily_usage.csv"

# Create CSV file with header (if not exists)
with open(csv_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Date", "Appliance", "Usage_Hours", "Units_Consumed"])

print("Virtual Smart Meter Started...")
print("Saving data automatically...\n")

start_time = time.time()

try:
    while True:
        time.sleep(5)
        current_time = time.time()
        elapsed = current_time - start_time
        start_time = current_time

        for appliance in appliance_state:
            appliance_state[appliance] = not appliance_state[appliance]
            if appliance_state[appliance]:
                usage_time[appliance] += elapsed

        print("Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        for appliance in appliances:
            status = "ON" if appliance_state[appliance] else "OFF"
            print(f"{appliance}: {status}")
        print("-" * 30)

except KeyboardInterrupt:
    print("\nStopping Virtual Smart Meter...\n")

    today = datetime.now().strftime("%Y-%m-%d")

    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)

        print("FINAL USAGE SUMMARY:")
        for appliance in appliances:
            hours = usage_time[appliance] / 3600
            units = (appliances[appliance] * hours) / 1000

            writer.writerow([today, appliance, round(hours, 2), round(units, 3)])

            print(f"{appliance}: {hours:.2f} hrs | {units:.3f} units")

    print("\nData saved to data/daily_usage.csv")
