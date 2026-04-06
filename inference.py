import requests

BASE_URL = "http://localhost:8000"

TASKS = ["easy", "medium", "hard"]

for task in TASKS:
    print(f"[START] task={task}")

    res = requests.post(BASE_URL + "/reset")
    obs = res.json()

    rewards = []

    for step in range(3):
        action = {"category": "Promotions"}

        res = requests.post(BASE_URL + "/step", json=action)
        data = res.json()

        reward = data["reward"]["value"]
        done = data["done"]

        rewards.append(reward)

        print(f"[STEP] step={step} reward={reward}")

        if done:
            break

    score = sum(rewards) / len(rewards)
    print(f"[END] score={score}")