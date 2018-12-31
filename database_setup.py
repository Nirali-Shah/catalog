# -*- coding: utf-8 -*-
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Base is a instance class of declarative_base
Base = declarative_base()

#create a database structure
class Restaurant(Base):
    __tablename__ = 'restaurant'
    
    id = Column( Integer, primary_key = True)   
    name = Column(String(80), nullable = False)
    
    #add JSON file data structure
    @property
    def serialize(self):
        #returns object data easily in a serialize format
        return{
               'name': self.name,
               'id': self.id,
               }

class MenuItem(Base):
    __tablename__ = 'menu_item'
    
    name = Column(String (80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant) 
    
    #add JSON file data structure
    @property
    def serialize(self):
        #returns object data easily in a serialize format
        return{
               'name': self.name,
               'description': self.description,
               'id': self.id,
               'price': self.price,
               'course': self.course,
               }
    
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)