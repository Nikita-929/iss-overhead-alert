# iss-overhead-alert
# ISS Alert Script

Sends an email when the International Space Station is overhead and it's nighttime at your location.

## How it works:
- Checks ISS position using open-notify API
- Checks sunrise/sunset with sunrise-sunset.org
- Sends email using Gmail + app password

## Setup:
1. Set environment variables:
   - `MY_EMAIL`
   - `EMAIL_PASSWORD`
2. Run: `python main.py`
