from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import and_, select, update
from datetime import datetime, timedelta, timezone
from contextlib import asynccontextmanager
import requests
import json
from pyngrok import ngrok
import uvicorn
import nest_asyncio
import subprocess

from app.database import get_db, init_db
from app.models import Complaint
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/complaints/", status_code=status.HTTP_201_CREATED)
async def create_complaint(text: str, db: AsyncSession = Depends(get_db)):
    try:
        complaint = Complaint(text=text)

        try: 
            response = requests.request("POST", settings.SENTIMENT_API_URL, 
                                        headers={"apikey":settings.API_LAYER_TOKEN}, data=text)
            result = response.text

            if response.status_code // 100 == 2:
                result = response.json()
                sentiment = result.get('sentiment', 'unknown')
            else:
                sentiment = 'unknown'

        except (requests.exceptions.RequestException, ValueError) as e:
            sentiment = "unknown"
        
        try:
            url = f"{settings.NGROK_URL}/generate" 
            data = {"text": f"Ответь одним словом: 'техническая', 'оплата' или 'другое' на жалобу: '{text}'. Ничего больше не пиши", "max_length": 20}
            response = requests.post(url, json=data)
            response_text = response.json()["response"]
            category = "другое"
            for word in ["техническая", "оплата", "другое"]:
                if response_text.lower().count(word) > 1:
                    category = word
                    break

        except (requests.exceptions.RequestException, ValueError) as e:
            category = "другое"

        complaint.sentiment = sentiment
        complaint.category = category
        db.add(complaint)
        await db.commit()
        await db.refresh(complaint)
        return complaint.to_schema()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.get("/complaints")
async def get_complaints(status: str = "open", hours: int = 1, db: AsyncSession = Depends(get_db)):
    now = datetime.now(timezone.utc)
    one_hour_ago = now - timedelta(hours=hours)
    print(now, one_hour_ago)
    stmt = select(Complaint).filter(Complaint.timestamp >= one_hour_ago, Complaint.status==status)
    res = await db.execute(stmt)
    if not res:
        raise NoResultFound(detail="Not found")
    res = [row[0].to_n8n() for row in res.all()]
    print(res)
    return res

@app.put("/complaints")
async def update_complaints(id: int, status: str = "closed", db: AsyncSession = Depends(get_db)):
    stmt = update(Complaint).where(Complaint.id==id).values(status=status)
    res = await db.execute(stmt)
    if not res:
        raise NoResultFound(detail="Not found")
    await db.commit()
    return {"status": "OK"}

result = subprocess.run(
    ["ngrok", "config", "add-authtoken", settings.NGROK_TOKEN],
    capture_output=True,
    text=True
)
ngrok_tunnel = ngrok.connect(8000)  # Открываем туннель к порту 8000
print("Public URL:", ngrok_tunnel.public_url)  # Копируем этот URL для FastAPI

# nest_asyncio.apply()  # Для работы в Colab
# uvicorn.run(app, host="0.0.0.0", port=8001)  # Запускаем сервер
