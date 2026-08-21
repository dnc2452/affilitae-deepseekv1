import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import DB_PATH
from .models import Base, Product, Post

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        logger.info(f"Database initialized: {db_path}")
    
    def add_product(self, product_data):
        session = self.Session()
        try:
            product = Product(**product_data)
            session.add(product)
            session.commit()
            logger.info(f"Product added: {product.name}")
            return product
        except Exception as e:
            session.rollback()
            logger.error(f"Error adding product: {e}")
            return None
        finally:
            session.close()
    
    def add_post(self, post_data):
        session = self.Session()
        try:
            post = Post(**post_data)
            session.add(post)
            session.commit()
            logger.info(f"Post added: {post.platform}")
            return post
        except Exception as e:
            session.rollback()
            logger.error(f"Error adding post: {e}")
            return None
        finally:
            session.close()
    
    def get_all_products(self):
        session = self.Session()
        try:
            products = session.query(Product).all()
            return products
        finally:
            session.close()
    
    def get_all_posts(self):
        session = self.Session()
        try:
            posts = session.query(Post).all()
            return posts
        finally:
            session.close()