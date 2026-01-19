import os
import requests
from email.mime.text import MIMEText
import smtplib
from datetime import datetime

# --- YOUR FOOD PREFERENCES (EDIT THIS ANYTIME) ---
PREFERENCES = """
Location: India
Goal: Healthy, sustainable eating (not extreme diet)
Cuisine preference: Indian home-style food
Veg/Non-veg: Veg on weekdays, Non-veg allowed on weekends
Dislikes: Brinjal, overly oily food
Likes: Paneer, dal, rice, roti, simple sabzi, light dinners
Constraints:
- Lunch can be wholesome
- Dinner should be light
- Avoid repeating same main dish on consecutive days
Output format:
Lunch: <dish>
Dinner: <dish>
Add 1 short health tip.
"""

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def generate_menu():
    prompt = f"""
You are a personal Indian meal planner.

User preferences:
{PREFERENCES}

Today is {datetime.now().strftime('%A, %d %B')}.

Generate today's lunch and dinner.
Keep it practical and Indian home-style.
"""

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        },
    )

    return response.json()["choices"][0]["message"]["content"]

def send_email(body):
    msg = MIMEText(body)
    msg["Subject"] = "🍽️ Today's Lunch & Dinner"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_FROM, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

if __name__ == "__main__":
    menu = generate_menu()
    send_email(menu)
