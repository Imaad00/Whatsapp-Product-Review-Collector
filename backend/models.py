from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from db import Base

# Table to store final product reviews
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    contact_number = Column(String, index=True)
    user_name = Column(String)
    product_name = Column(String)
    product_review = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


# Table to store temporary conversation session per user
class SessionState(Base):
    __tablename__ = "sessions"

    contact_number = Column(String, primary_key=True, index=True)
    step = Column(String, nullable=False)  # ask_product | ask_name | ask_review
    temp_product = Column(String, nullable=True)
    temp_name = Column(String, nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
