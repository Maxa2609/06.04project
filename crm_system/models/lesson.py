from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship

from crm_system.models.database import Base

association_table = Table('association', Base.metadata, Column('lesson_id', Integer, ForeignKey('lesson.id')),
                          Column('group_id', Integer, ForeignKey('groups.id')))

class Lesson(Base):
    __tablename__ = 'lesson'

    id = Column(Integer, primary_key=True)
    lesson_title = Column(String)
    groups = relationship('Group', secondary=association_table,backref='group_lesson')

    def __repr__(self):
        return f'Lesson [ID: {self.id}, Name: {self.lesson_title}]'