import os
import requests
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_URL = "http://localhost:8000"

TASKS = ["easy", "medium", "hard"]

for task in TASKS:
    print(f"[START] task={task}")

    res = requests.post(BASE_URL + "/reset")
    obs = res.json()

    rewards = []

    for step in range(5):
        email_text = obs["email"]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an email classification assistant. Categories: Promotions, Work, Finance, Social, Job."
                },
                {
                    "role": "user",
                    "content": f"Classify this email into one category: {email_text}"
                }
            ]
        )

        category = response.choices[0].message.content.strip()

        action = {"category": category}

        res = requests.post(BASE_URL + "/step", json=action)
        data = res.json()

        reward = data["reward"]["value"]
        done = data["done"]

        rewards.append(reward)

        print(f"[STEP] step={step} action={category} reward={reward:.2f} done={done}")

        if done:
            break

        obs = data["observation"]

    score = sum(rewards) / len(rewards)
    print(f"[END] score={score:.2f}\n")