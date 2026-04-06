from fastapi import FastAPI
from env import EmailEnv, Action
import uvicorn

app = FastAPI()
env = EmailEnv()

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


# 🔥 REQUIRED MAIN FUNCTION
def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


# 🔥 REQUIRED ENTRY POINT
if __name__ == "__main__":
    main()