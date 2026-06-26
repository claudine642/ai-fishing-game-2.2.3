from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fishing import cmd
import uvicorn

app = FastAPI(title="AI钓鱼游戏 API")

class FishRequest(BaseModel):
    action: str
    times: int = 1

@app.post("/fish")
def play_fishing(request: FishRequest):
    """
    执行钓鱼动作，返回结果字符串。
    """
    try:
        results = []
        for _ in range(request.times):
            result = cmd(request.action)
            results.append(result)
        return {"status": "success", "output": "\n".join(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "AI钓鱼游戏 API 运行中，请 POST 到 /fish"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)