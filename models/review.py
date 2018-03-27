#!/usr/bin/python3
'''
    Implementation of the Review class
'''
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Review(BaseModel, Base):
    '''
        Implementation for the Review.
    '''
    __tablename__ = "review"
    text = Column(String(1024), nullable=False)
    place_id = Column(String(1024), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="reviews")
#    place = relationship("Place", "reviews")
