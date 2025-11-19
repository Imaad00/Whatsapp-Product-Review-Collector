# 📦 WhatsApp Product Review Collector

AI Full-stack app using **FastAPI**, **PostgreSQL**, **Docker**, **React**, and **Twilio WhatsApp Sandbox**.

This project allows users to submit product reviews via WhatsApp.  
The backend uses FastAPI and stores reviews in PostgreSQL (via Docker).  
The frontend (React) displays all stored reviews in an interactive table.

---

## ⭐ Features

- ✔ WhatsApp → Server → Database conversation flow  
- ✔ Full conversation state handling  
- ✔ Stores review in PostgreSQL  
- ✔ REST API (`GET /api/reviews`)  
- ✔ React UI showing all reviews  
- ✔ Dockerized backend + database  
- ✔ Twilio WhatsApp Sandbox integration  
- ✔ ngrok tunneling for local testing  
- ✔ Fully testable with curl (no phone required)  

---

## 🚀 Tech Stack

### **Backend**
- Python 3.11  
- FastAPI  
- SQLAlchemy  
- PostgreSQL  
- Docker / Docker Compose  
- Twilio API (Webhook)  

### **Frontend**
- React  
- Create React App  
- Fetch API  
- Minimal responsive table  

---

## 📁 Project Structure

```
Whatsapp review/
├── backend/
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── requirements.txt
│   ├── .env
│   ├── Dockerfile
│   └── ...
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
├── docker-compose.yml
└── README.md
```

---

## 🧪 1. Local Development (NO WhatsApp required)

You can fully test the project **without Twilio**, using **curl.exe**.

### **Start backend + database**

From project root:

```bash
docker-compose up --build -d
```

Show status:

```bash
docker-compose ps
```

Follow backend logs (optional):

```bash
docker-compose logs -f backend --tail=200
```

Check backend API:

```bash
curl.exe http://localhost:8000/api/reviews
```

Expected:

```json
[]
```

---

### **Start frontend**

```bash
cd frontend
npm install
npm start
```

Open:

👉 http://localhost:3000

---

## 🧪 2. Test Full Conversation Flow (LOCAL TESTING)

Simulate WhatsApp messages **with curl.exe**.  
Use the same phone number for all steps.

### **1) User says Hi**
```bash
curl.exe -X POST "http://localhost:8000/webhook/whatsapp" -d "From=whatsapp:+1111" -d "Body=Hi"
```

### **2) Product name**
```bash
curl.exe -X POST "http://localhost:8000/webhook/whatsapp" -d "From=whatsapp:+1111" -d "Body=iPhone 15"
```

### **3) User name**
```bash
curl.exe -X POST "http://localhost:8000/webhook/whatsapp" -d "From=whatsapp:+1111" -d "Body=Aditi"
```

### **4) Product review**
```bash
curl.exe -X POST "http://localhost:8000/webhook/whatsapp" -d "From=whatsapp:+1111" -d "Body=Amazing battery life"
```

### **5) Check stored review**
```bash
curl.exe http://localhost:8000/api/reviews
```

Expected:

```json
[
  {
    "id": 1,
    "contact_number": "whatsapp:+1111",
    "user_name": "Aditi",
    "product_name": "iPhone 15",
    "product_review": "Amazing battery life",
    "created_at": "..."
  }
]
```

---

## 📞 3. Real WhatsApp Integration (Twilio Sandbox)

### **Step A — Activate Twilio Sandbox**

Log in:

https://console.twilio.com

Navigate to:

```
Messaging → Try It Out → WhatsApp Sandbox
```

You will see:

- Sandbox number → **+1 415 523 8886**  
- Join code → **join xxxx-yyyy**

### Join the sandbox:

Send this via WhatsApp:

```
join your-code-here
```

to:

📱 **+1 415 523 8886**

---

## 🌐 4. Expose Backend with ngrok

Run:

```bash
.\ngrok http 8000
```

Copy the HTTPS URL:

```
https://abcd1234.ngrok.io
```

---

## 🔗 5. Set Twilio Webhook

In Twilio Sandbox settings:

```
WHEN A MESSAGE COMES IN:
https://abcd1234.ngrok.io/webhook/whatsapp
```

Click **Save**.

---

## 📥 6. Test on Real WhatsApp

Send:

```
Hi
iPhone 15
Aditi
Amazing battery life
```

Backend receives it → Review instantly appears on the React UI.

---

## 🗄 Database Schema

### **reviews table**

| Column          | Type        |
|----------------|-------------|
| id             | integer (PK) |
| contact_number | text         |
| user_name      | text         |
| product_name   | text         |
| product_review | text         |
| created_at     | timestamp    |

### **sessions table**
Used internally to track conversation state.

---

## 🔧 Environment Variables (backend/.env)

```
DATABASE_URL=postgresql://postgres:postgres@db:5432/reviewsdb
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

---

## 🐳 Docker Commands

Start everything:

```bash
docker-compose up -d
```

Rebuild backend:

```bash
docker-compose build backend
docker-compose up -d
```

Logs:

```bash
docker-compose logs -f backend
docker-compose logs -f db
```

Reset session state:

```bash
docker-compose exec db psql -U postgres -d reviewsdb -c "DELETE FROM sessions;"
```

---

## 🌐 API Documentation

### **GET /api/reviews**

Response:

```json
[
  {
    "id": 1,
    "contact_number": "whatsapp:+1111",
    "user_name": "Aditi",
    "product_name": "iPhone 15",
    "product_review": "Amazing battery life",
    "created_at": "2025-11-17T12:34:56Z"
  }
]
```

---

## 🛰 Why ngrok is Required

Twilio cannot reach `localhost`.

ngrok provides:

- Public HTTPS → local FastAPI webhook  
- Secure tunnel  
- Enables testing WhatsApp → Twilio → your backend locally  

To run ngrok in PowerShell:

```bash
Go to the ngrok path (eg: C:\ngrok)
.\ngrok http 8000
```
