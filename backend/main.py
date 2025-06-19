from fastapi import FastAPI, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
import os

app = FastAPI()

# Statik frontend klasörünü bağla
app.mount(
    "/frontend",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../frontend")),
    name="frontend",
)

# Ana sayfaya gelenleri frontend'e yönlendir
@app.get("/")
def root():
    return RedirectResponse(url="/frontend/index.html")

# Stars ödeme linki oluşturur (gerçek initData ile)
@app.get("/create-stars-form")
async def create_stars_form(
    request: Request,
    amount: int = Query(...),
    initData: str = Query("")
):
    # Kontrol/log için initData'yı terminale yazalım
    print("✅ initData alındı:", initData)

    # Ödeme linki: gerçek sistemde initData doğrulaması da yapılmalı
    payment_url = f"https://t.me/CabbarVIPBot?start=stars_payment_{amount}"

    return JSONResponse({"payment_url": payment_url})

# Uygulama başlat (yerel geliştirme için)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
