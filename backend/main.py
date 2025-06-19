from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
import os
import hmac
import hashlib
import urllib.parse
import logging
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()

# Loglama ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Statik frontend klasörünü bağla
app.mount(
    "/frontend",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../frontend")),
    name="frontend",
)

# Ana dizini frontend'e yönlendir
@app.get("/")
def root():
    return RedirectResponse(url="/frontend/index.html")

# 🔐 initData doğrulama fonksiyonu
def verify_init_data(init_data: str, bot_token: str) -> bool:
    try:
        parsed = urllib.parse.parse_qs(init_data, strict_parsing=True)
        data_check_string = "\n".join(
            f"{k}={v[0]}" for k, v in sorted(parsed.items()) if k != "hash"
        )
        received_hash = parsed["hash"][0]

        secret_key = hashlib.sha256(bot_token.encode()).digest()
        computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        return computed_hash == received_hash
    except Exception as e:
        logger.warning(f"initData doğrulama hatası: {e}")
        return False

# Stars ödeme bağlantısı oluşturur
@app.get("/create-stars-form")
async def create_stars_form(
    amount: int = Query(...),
    initData: str = Query("")
):
    BOT_TOKEN = os.getenv("BOT_TOKEN", "DEVELOPMENT_TOKEN_HERE")

    if not verify_init_data(initData, BOT_TOKEN):
        raise HTTPException(status_code=403, detail="Geçersiz initData")

    # Gerçek ödeme linki — kullanıcıyı bot üzerinden ödeme yapmaya yönlendir
    payment_url = f"https://t.me/CabbarVIPBot?start=stars_payment_{amount}"

    return JSONResponse({"payment_url": payment_url})


# Lokal geliştirme için çalıştırma komutu
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
