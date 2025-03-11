🚆 Train Booking System with M-Pesa Integration

A web-based train reservation system built with Django, allowing users to book train seats and make payments securely via M-Pesa.

🛠 Features

✅ User Authentication – Sign up, log in, and manage bookings
✅ Train Schedule Management – View train schedules and available seats
✅ Seat Reservation – Book train seats with real-time availability updates
✅ M-Pesa Payment Integration – Secure mobile payments via M-Pesa API
✅ Booking Confirmation – Receive booking status and payment receipts
✅ Internationalization (i18n) – Multi-language support for a global audience
✅ Retry Logic – Automatic retry mechanism for failed transactions
✅ Admin Dashboard – Manage users, bookings, and payments
✅ Email & SMS Notifications – Booking confirmation via email/SMS

📌 Installation Guide

1️⃣ Clone the Repository
git clone https://github.com/Dtorredo/Derrick.git
cd Derrick
2️⃣ Set Up a Virtual Environment
python -m venv myvenv
source myvenv/bin/activate  # On Windows, use myvenv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Apply Migrations
python manage.py migrate
5️⃣ Run the Development Server
python manage.py runserver
Visit http://127.0.0.1:8000/ in your browser.
💰 M-Pesa Payment Integration

This project uses M-Pesa Daraja API for mobile payments.

📌 Steps to Enable M-Pesa
Create an M-Pesa Developer Account at Safaricom Daraja API.
Generate API Keys for M-Pesa transactions.
Store API credentials securely in credentials.py:
MPESA_CONSUMER_KEY = "your_consumer_key"
MPESA_CONSUMER_SECRET = "your_consumer_secret"
MPESA_SHORTCODE = "your_shortcode"
Make a Payment Request via views.py:
import requests
headers = {"Authorization": "Bearer YOUR_ACCESS_TOKEN"}
response = requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest", headers=headers)
🌍 Internationalization (i18n)

This project supports multiple languages using Django’s built-in localization settings.

Enable a Different Language
Open settings.py and update:
LANGUAGE_CODE = 'es'  # Change to 'fr', 'de', etc.
Collect translations:
django-admin compilemessages
Restart the server:
python manage.py runserver
📂 Project Structure

derrick/
│── db.sqlite3              # SQLite Database  
│── manage.py               # Django Project Manager  
│── train/                  # Main Train App  
│   ├── models.py           # Database Models  
│   ├── views.py            # Business Logic  
│   ├── urls.py             # URL Routing  
│── templates/              # HTML Templates  
│── static/                 # CSS, JS, and Images  
│── myvenv/                 # Virtual Environment  
🛠 Additional Features

📌 Enhanced Logging with Rich
This project supports color-coded logging using the rich library, improving error visibility in the terminal.

To enable detailed logs, modify settings.py:

from rich import print
from rich.console import Console

console = Console()

console.log("Train Booking System is running...", style="bold green")
📌 Error Handling with Tenacity
The Tenacity package is used for automatic retry logic in case of API failures (e.g., M-Pesa requests).

Example: Retrying M-Pesa requests if they fail

from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def process_mpesa_payment():
    # Call M-Pesa API here
    console.log("[yellow]Retrying payment request...[/yellow]")
If an M-Pesa request fails, the system will retry up to 3 times with exponential backoff.
📌 Secure API Requests with Urllib3
urllib3 is used for secure API communication with external services like M-Pesa.
Modify the credentials.py file to store API keys securely:

import urllib3

http = urllib3.PoolManager()
response = http.request("GET", "https://api.safaricom.co.ke/mpesa")
📌 Future Improvements

Google Maps Integration – Display train routes
Dockerize the project for easier deployment
Automated testing with Pytest
Deploy on AWS/GCP
🚀 Running the Project

source myvenv/bin/activate
python manage.py runserver
👥 Contributing

Feel free to submit a pull request if you'd like to improve the system!
