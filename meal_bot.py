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
Veg/non Veg: Veg food or egg options only. No Non-Veg
Dislikes: Deep Fried Food, Food maid from maida, High Sugar Food, High Calorie Food
Likes: Paneer, dal, rice, roti, Rajma, simple sabzi, Kadi, Brinjal, Potato, light dinners, Rajasthani food, protein rich food,
Constraints
- Lunch can be wholesome
- Dinner should be light
- All the meals should be protein rich
- Avoid any meal having calorie more than 500
- Avoid any Deep fried Food
- Avoid repeating same main dish on consecutive days
- Prefer Indian foods mostly


IMPORTANT FORMAT RULES:
- Do NOT use Markdown.
- Do NOT use *, **, ###, or bullet symbols.
- Use plain text only.
- Use headings with bold font:

Output format:
Meal Plan for <date>

Lunch:
Dish:
Calories:

Dinner:
Dish:
Calories:


"""

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def generate_menu():
    if not OPENAI_API_KEY:
        raise Exception("OPENAI_API_KEY is not set in GitHub Secrets")

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
        timeout=30,
    )

    data = response.json()

    # Defensive check so it never crashes silently
    if "choices" not in data:
        raise Exception(f"OpenAI API Error: {data}")

    return data["choices"][0]["message"]["content"]


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
