from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id = Column(String, primary_key=True)
    name = Column(String)
    price = Column(Float)
    commission_rate = Column(Float)
    sales_count = Column(Integer)
    rating = Column(Float)
    category = Column(String)
    affiliate_link = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Product {self.name}>"

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(String, primary_key=True)
    product_id = Column(String)
    platform = Column(String)  # tiktok, facebook
    video_path = Column(String)
    caption = Column(String)
    post_url = Column(String)
    status = Column(String)  # posted, scheduled, failed
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    earnings = Column(Float, default=0)
    posted_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Post {self.platform} - {self.status}>"