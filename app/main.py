from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
import requests

from app.database import get_db, init_db
from app.models import Complaint
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создание БД при запуске
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/complaints/", status_code=status.HTTP_201_CREATED)
async def create_complaint(text: str, db: AsyncSession = Depends(get_db)):
    try:
        complaint = Complaint(text=text)

        try:
            # Отправка текста API_LAYER на анализ тональности 
            response = requests.request("POST", settings.SENTIMENT_API_URL, 
                                        headers={"apikey":settings.API_LAYER_TOKEN}, data=text)
            result = response.text

            if response.status_code // 100 == 2:
                result = response.json()
                sentiment = result.get('sentiment', 'unknown')
            else:
                sentiment = 'unknown'

        # Если API не доступен, тональность unknown
        except (requests.exceptions.RequestException, ValueError) as e:
            sentiment = "unknown"
        
        complaint.sentiment = sentiment
        db.add(complaint)
        await db.commit()
        await db.refresh(complaint)
        return complaint.to_schema()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    




