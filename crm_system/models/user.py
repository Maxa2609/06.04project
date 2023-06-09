from crm_system.models.database import Base
from sqlalchemy import Column, Integer, String
from flask_login import UserMixin

class User(UserMixin,Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    password = Column(String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password