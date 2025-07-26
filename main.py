
import os
import time
import pytz
import requests
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load email and password securely from environment variables
MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("EMAIL_PASSWORD")
TO_EMAIL = "mahatonikita929@gmail.com"

# Location details
MY_LAT = 51.507351  # Example: London latitude
MY_LONG = -0.127758  # Example: London longitude
LOCAL_TIMEZONE = pytz.timezone("Asia/Kolkata")  # Your local timezone

def is_iss_overhead():
    """Check if the ISS is within ±5° of your location."""
    try:
        response = requests.get("http://api.open-notify.org/iss-now.json", timeout=10)
        response.raise_for_status()
        data = response.json()
        iss_lat = float(data["iss_position"]["latitude"])
        iss_long = float(data["iss_position"]["longitude"])
        return (MY_LAT - 5 <= iss_lat <= MY_LAT + 5) and (MY_LONG - 5 <= iss_long <= MY_LONG + 5)
    except Exception as e:
        print(f"Error fetching ISS location: {e}")
        return False

def is_night():
    """Check if it's currently nighttime at your location."""
    try:
        params = {
            "lat": MY_LAT,
            "lng": MY_LONG,
            "formatted": 0,
        }
        response = requests.get("https://api.sunrise-sunset.org/json", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        sunrise_utc = datetime.strptime(data["results"]["sunrise"], "%Y-%m-%dT%H:%M:%S%z")
        sunset_utc = datetime.strptime(data["results"]["sunset"], "%Y-%m-%dT%H:%M:%S%z")

        sunrise_local = sunrise_utc.astimezone(LOCAL_TIMEZONE).time()
        sunset_local = sunset_utc.astimezone(LOCAL_TIMEZONE).time()
        now_local = datetime.now(LOCAL_TIMEZONE).time()

        print(f"Sunrise: {sunrise_local}, Sunset: {sunset_local}, Now: {now_local}")
        return now_local >= sunset_local or now_local <= sunrise_local
    except Exception as e:
        print(f"Error fetching sunrise/sunset times: {e}")
        return False

def send_email():
    """Send an email alert."""
    msg = MIMEMultipart()
    msg["From"] = MY_EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = "🚀 ISS Overhead Alert!"
    body = "👆 Look Up!\nThe ISS is currently above your location in the sky."
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, PASSWORD)
            connection.sendmail(MY_EMAIL, TO_EMAIL, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Main loop
print("ISS Alert System Started. Checking every 60 seconds...")
while True:
    try:
        if is_iss_overhead() and is_night():
            send_email()
        else:
            print("No alert. ISS not overhead or it’s not night.")
    except Exception as e:
        print(f"Unexpected error in main loop: {e}")
    time.sleep(60)


