import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# -----------------------------
# CONFIGURATION
# -----------------------------

# CSV file path
csv_file = "../data/daily_usage.csv"

# Cost per unit (₹)
cost_per_unit = {
    'Fan': 5,
    'Light': 5,
    'AC': 10
}

# Usage thresholds for alert (units)
thresholds = {
    'Fan': 0.010,
    'Light': 0.005,
    'AC': 0.020
}

# -----------------------------
# EMAIL SETTINGS (Optional)
# -----------------------------
ENABLE_EMAIL = False   # True = send email alerts, False = skip for demo
sender_email = "youremail@gmail.com"
receiver_email = "receiver@gmail.com"
password = "your_16_char_app_password"  # Gmail App Password if ENABLE_EMAIL=True

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv(csv_file)
df['Date'] = pd.to_datetime(df['Date'])

# Group by appliance
appliance_units = df.groupby('Appliance')['Units_Consumed'].sum().to_dict()

# -----------------------------
# USAGE SUMMARY
# -----------------------------
print("\nENERGY USAGE ANALYSIS REPORT\n")
total_units = 0
for appliance, units in appliance_units.items():
    cost = units * cost_per_unit.get(appliance, 0)
    total_units += units
    print(f"{appliance}: {units:.3f} units | ₹{cost:.2f}")

print(f"\nTOTAL ELECTRICITY CONSUMED: {total_units:.3f} units")

if total_units > sum(thresholds.values()):
    print("⚠ Usage is above normal range")
else:
    print("✅ Usage is within normal range")

# -----------------------------
# EMAIL ALERTS (Optional)
# -----------------------------
if ENABLE_EMAIL:
    alert_msg = ""
    for appliance, units in appliance_units.items():
        if units > thresholds.get(appliance, 0):
            alert_msg += f"{appliance} usage high! ({units:.3f} units)\n"

    if alert_msg:
        msg = MIMEText(alert_msg)
        msg['Subject'] = "⚠ Energy Usage Alert"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)

        print("✅ Alert email sent!")
    else:
        print("✅ All appliances within normal range")
else:
    print("✅ Email alerts disabled for demo")

# -----------------------------
# APPLIANCE STATISTICS
# -----------------------------
print("\nAPPLIANCE STATISTICS:")
for appliance, units in appliance_units.items():
    print(f"{appliance}: total units = {units:.3f}")
