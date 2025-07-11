import requests

complaint_text = "Денежные транзакции не работают"
url = "https://202e96845e72.ngrok-free.app//generate" 
data = {"text": f"Определи категорию жалобы: '{complaint_text}'. Варианты: техническая, оплата, другое. Ответ только одним словом", "max_length": 150}
data2 = {"text": "Как звали лермонтова?", "max_length": 150}
data3 = {"text": f"Ответь одним словом: 'техническая', 'оплата' или 'другое' на жалобу: '{complaint_text}'. Ничего больше не пиши", "max_length": 20}


response = requests.post(url, json=data3)
print(response.json()["response"])