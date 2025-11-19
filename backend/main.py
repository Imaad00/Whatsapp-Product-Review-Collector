import os
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# local imports (same folder)
from db import SessionLocal, engine, Base
import models

# load .env if present
load_dotenv()

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="WhatsApp Product Review Collector")

# Allow frontend (React dev server) to call the API
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Twilio will POST form-encoded data with fields like 'From' and 'Body'.
    We maintain a simple per-number session in the `sessions` table and
    drive a 3-step flow: ask_product -> ask_name -> ask_review.
    """
    form = await request.form()
    from_number = form.get("From")  # e.g., "whatsapp:+1415XXXXXXX"
    body = (form.get("Body") or "").strip()

    if not from_number:
        raise HTTPException(status_code=400, detail="Missing 'From' in webhook payload")

    # allow user to restart at any time
    if body.lower() in ("restart", "reset"):
        existing = db.query(models.SessionState).filter(models.SessionState.contact_number == from_number).first()
        if existing:
            db.delete(existing)
            db.commit()
        twiml = MessagingResponse()
        twiml.message("Session reset. Which product is this review for?")
        return Response(content=str(twiml), media_type="application/xml")

    # load or create session
    session = db.query(models.SessionState).filter(models.SessionState.contact_number == from_number).first()

    if session is None:
        # start flow
        session = models.SessionState(contact_number=from_number, step="ask_product")
        db.add(session)
        db.commit()
        twiml = MessagingResponse()
        twiml.message("Hello 👋 — Which product is this review for?")
        return Response(content=str(twiml), media_type="application/xml")

    # handle steps
    if session.step == "ask_product":
        session.temp_product = body
        session.step = "ask_name"
        db.add(session)
        db.commit()
        twiml = MessagingResponse()
        twiml.message("What's your name?")
        return Response(content=str(twiml), media_type="application/xml")

    if session.step == "ask_name":
        session.temp_name = body
        session.step = "ask_review"
        db.add(session)
        db.commit()
        twiml = MessagingResponse()
        twiml.message(f"Please send your review for {session.temp_product}.")
        return Response(content=str(twiml), media_type="application/xml")

    if session.step == "ask_review":
        # save review
        review = models.Review(
            contact_number=from_number,
            user_name=session.temp_name or "Anonymous",
            product_name=session.temp_product or "Unknown",
            product_review=body
        )
        db.add(review)
        # clear session
        db.delete(session)
        db.commit()
        twiml = MessagingResponse()
        twiml.message(f"Thanks {review.user_name} — your review for {review.product_name} has been recorded.")
        return Response(content=str(twiml), media_type="application/xml")

    # fallback: reset and ask product
    session.step = "ask_product"
    session.temp_product = None
    session.temp_name = None
    db.add(session)
    db.commit()
    twiml = MessagingResponse()
    twiml.message("Sorry, I didn't understand. Which product is this review for?")
    return Response(content=str(twiml), media_type="application/xml")


@app.get("/api/reviews")
def list_reviews(db: Session = Depends(get_db)):
    """
    Return all reviews as JSON, newest first.
    """
    rows = db.query(models.Review).order_by(models.Review.created_at.desc()).all()
    result = []
    for r in rows:
        result.append({
            "id": r.id,
            "contact_number": r.contact_number,
            "user_name": r.user_name,
            "product_name": r.product_name,
            "product_review": r.product_review,
            "created_at": r.created_at.isoformat() if r.created_at else None
        })
    return JSONResponse(result)
