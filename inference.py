import requests
from transformers import pipeline
import matplotlib.pyplot as plt

# FREE AI MODEL
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

BASE_URL = "http://localhost:8000"

TASKS = ["easy", "medium", "hard"]
CATEGORIES = ["Promotions", "Work", "Finance", "Social", "Job"]

all_scores = []

for task in TASKS:
    print(f"\n[START] task={task}")

    res = requests.post(BASE_URL + "/reset")
    obs = res.json()

    rewards = []

    for step in range(5):
        email_text = obs["email"]

        result = classifier(email_text, CATEGORIES)
        category = result["labels"][0]

        action = {"category": category}

        res = requests.post(BASE_URL + "/step", json=action)
        data = res.json()

        reward = data["reward"]["value"]
        done = data["done"]

        rewards.append(reward)

        # 🔥 EXPLANATION OUTPUT
        print(f"\nEmail: {email_text}")
        print(f"Predicted: {category} | Reward: {reward:.2f}")

        if done:
            break

        obs = data["observation"]

    score = sum(rewards) / len(rewards)
    all_scores.append(score)

    print(f"[END] score={score:.2f}")

# 📊 GRAPH
plt.plot(TASKS, all_scores, marker='o')
plt.title("Agent Performance Across Tasks")
plt.xlabel("Task Difficulty")
plt.ylabel("Score")
plt.grid()

plt.savefig("performance.png")
print("\n📊 Graph saved as performance.png")