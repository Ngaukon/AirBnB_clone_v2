#!/usr/bin/python3
"""Defines the State class"""

import models
from models.base_model import BaseModel, Base
from models.city import City
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Representation of a State in the database or in memory"""

    # Use SQLAlchemy ORM mapping if storage_t is set to "db"
    if models.storage_t == "db":
        __tablename__ = 'states'
        
        # Name of the state
        name = Column(String(128), nullable=False)
        
        # Relationship to the City class (one-to-many)
        cities = relationship("City", backref="state")
    else:
        # In-memory representation when not using a database
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializes a State instance"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def cities(self):
            """Returns a list of City instances related to the state

            The list is built by filtering all cities stored in the in-memory storage 
            to find those associated with the current state instance.

            Returns:
                list: List of City instances related to the current State
            """
            city_list = []
            all_cities = models.storage.all(City)  # Get all cities from storage
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
