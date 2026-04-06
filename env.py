from pydantic import BaseModel
from typing import Dict, Any

class Observation(BaseModel):
    email: str

class Action(BaseModel):
    category: str

class Reward(BaseModel):
    value: float


class EmailEnv:
    def __init__(self, task="easy"):
        self.task = task
        self.index = 0

        self.data = {
            "easy": [
                ("Big discount offer just for you!", "Promotions"),
                ("Meeting scheduled tomorrow", "Work"),
            ],
            "medium": [
                ("Your bank account alert", "Finance"),
                ("Join our community event", "Social"),
            ],
            "hard": [
                ("Limited time job opportunity apply now", "Job"),
                ("Important project deadline approaching", "Work"),
            ]
        }

    def reset(self):
        self.index = 0
        email, _ = self.data[self.task][self.index]
        return Observation(email=email)

    def step(self, action: Action):
        email, correct = self.data[self.task][self.index]

        if action.category.lower() == correct.lower():
            reward = 1.0
        elif action.category.lower() in correct.lower():
            reward = 0.5
        else:
            reward = 0.0

        self.index += 1
        done = self.index >= len(self.data[self.task])

        next_obs = {}
        if not done:
            next_email, _ = self.data[self.task][self.index]
            next_obs = Observation(email=next_email)

        return next_obs, Reward(value=reward), done, {}

    def state(self) -> Dict[str, Any]:
        return {"index": self.index, "task": self.task}