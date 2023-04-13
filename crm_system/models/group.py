from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from crm_system.models.database import Base

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    group_name = Column(String)