from fastapi import FastAPI, Query
from server.oauth import router as oauth_router
from env import EmailEnv, Action
from gmail import get_emails
from transformers import pipeline
from collections import Counter
import uvicorn

# ✅ CREATE APP FIRST
app = FastAPI()

# ✅ INCLUDE ROUTER AFTER APP
app.include_router(oauth_router, prefix="/auth")

# ✅ INIT ENV
env = EmailEnv()

# 🔹 ROOT
@app.get("/")
def home():
    return {"message": "Email AI Environment Running"}

# 🔹 OPENENV ROUTES
@app.post("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return env.state()


# 🔥 LOAD MODEL ONCE (IMPORTANT)
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

CATEGORIES = ["Promotions", "Work", "Finance", "Social", "Job"]


# 🔥 DASHBOARD API (FILTER + COUNTS + LOAD MORE)
@app.get("/gmail-dashboard")
def gmail_dashboard(
    max_results: int = 10,
    keyword: str = None,
    category_filter: str = None
):
    emails = get_emails(max_results)

    results = []

    for email in emails:
        # 🔍 KEYWORD FILTER
        if keyword and keyword.lower() not in email.lower():
            continue

        result = classifier(email, CATEGORIES)
        label = result["labels"][0]

        # 🎯 CATEGORY FILTER
        if category_filter and label.lower() != category_filter.lower():
            continue

        results.append({
            "email": email,
            "category": label
        })

    # 📊 CATEGORY COUNTS
    counts = Counter([r["category"] for r in results])

    return {
        "total_emails": len(results),
        "category_counts": counts,
        "results": results
    }


# 🔹 RUN SERVER
def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()