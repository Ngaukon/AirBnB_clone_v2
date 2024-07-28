#!/usr/bin/python3
"""
Contains the FileStorage class for serializing and deserializing instances
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Mapping of class names to class objects
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """Handles the storage of instances in a JSON file"""

    # string - path to the JSON file for storage
    __file_path = "file.json"
    # dictionary - stores all objects with key format <class name>.id
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of all objects or filtered by class if cls is specified

        Args:
            cls (type or str): The class type or class name to filter the objects by.

        Returns:
            dict: Dictionary of objects with keys in format <class name>.id
        """
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                # Check if the class matches the provided class type or name
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """Adds a new object to the storage dictionary

        Args:
            obj (BaseModel): The object to add to the storage.
        """
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """Serializes the __objects dictionary to the JSON file specified by __file_path"""
        json_objects = {}
        for key, obj in self.__objects.items():
            json_objects[key] = obj.to_dict()  # Convert object to dictionary
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)  # Write dictionary to JSON file

    def reload(self):
        """Deserializes the JSON file and loads objects into the __objects dictionary"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)  # Load JSON data from file
            for key, value in jo.items():
                # Create an instance of the class based on the __class__ key
                self.__objects[key] = classes[value["__class__"]](**value)
        except FileNotFoundError:
            pass  # If the file does not exist, do nothing

    def delete(self, obj=None):
        """Removes an object from the storage dictionary if it exists

        Args:
            obj (BaseModel): The object to remove from the storage.
        """
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]  # Remove object from dictionary

    def close(self):
        """Deserializes the JSON file to objects by calling reload()"""
        self.reload()
