from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
import requests

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
    




