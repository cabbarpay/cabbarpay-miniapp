from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "CabbarPay Mini App başarılı şekilde çalışıyor 🎉"}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))  # Render 8000 portunu dinler
    uvicorn.run(app, host="0.0.0.0", port=port)
