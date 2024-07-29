#!/usr/bin/python3
"""Holds the State class"""
import models
from models.base_model import BaseModel, Base
from models.city import City
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Representation of a State in the database"""

    if models.storage_t == "db":
        __tablename__ = 'states'
        # State name
        name = Column(String(128), nullable=False)
        # Relationship with City: one-to-many relationship
        cities = relationship("City", backref="state")
    else:
        # In filesystem storage mode, name is a simple attribute
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializes a new State instance"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def cities(self):
            """
            Getter for a list of City instances related to the State.

            This method is used only in filesystem storage mode where
            relationships are not handled by SQLAlchemy.

            Returns:
                list: A list of City instances related to the current State.
            """
            city_list = []
            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list

