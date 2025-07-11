# Complaint-service
Система для обработки жалоб клиентов с использованием публичных API

## Установка зависимостей

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

2. Установите зависимости из requirements.txt:
```bash
pip install -r requirements.txt
```

Пример содержимого requirements.txt:
```
fastapi>=0.95.0
uvicorn>=0.21.0
sqlalchemy>=2.0.0
asyncpg>=0.27.0
requests>=2.28.0
python-dotenv>=0.21.0
```

## Запуск приложения

1. Создайте файл `.env` в корне проекта с настройками:
```
API_LAYER_TOKEN=your_api_layer_key
SENTIMENT_API_URL=https://api.apilayer.com/sentiment/analysis
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
```

2. Запустите сервер:
```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: http://127.0.0.1:8000

## Примеры запросов

### Создание жалобы (POST)

#### cURL:
```bash
curl -X POST "http://127.0.0.1:8000/complaints/" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "text=I'm very disappointed with your service"
```

#### Postman:
1. Метод: POST
2. URL: http://127.0.0.1:8000/complaints/
3. Body:
   - Выберите `x-www-form-urlencoded`
   - Добавьте параметр:
     - Key: text
     - Value: I'm very disappointed with your service

#### Пример ответа:
```json
{
  "id": 1,
  "text": "I'm very disappointed with your service",
  "sentiment": "negative",
  "created_at": "2023-05-15T12:00:00"
}
```

### Получение списка жалоб (GET)

#### cURL:
```bash
curl -X GET "http://127.0.0.1:8000/complaints/"
```

#### Postman:
1. Метод: GET
2. URL: http://127.0.0.1:8000/complaints/

#### Пример ответа:
```json
[
  {
    "id": 1,
    "sentiment": "negative",
    "created_at": "2023-05-15T12:00:00"
  },
  {
    "id": 2,
    "sentiment": "positive",
    "created_at": "2023-05-15T12:05:00"
  }
]
```

## Дополнительная информация

Приложение автоматически определяет тональность текста жалобы с помощью API Layer Sentiment Analysis. В случае недоступности API или ошибки анализа, тональность устанавливается как "unknown".