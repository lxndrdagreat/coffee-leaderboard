# database.py
from pymongo import MongoClient

from coffee_leaderboard import app

db_client = MongoClient()
db = db_client.coffee

# handle database authentication
if 'DATABASE_USERNAME' in app.config and len(app.config['DATABASE_USERNAME']) > 0:
    db.authenticate(app.config['DATABASE_USERNAME'], app.config['DATABASE_PASSWORD'])


class BaseModel:
    """Base database model that the other models inherit from."""
    __collection__ = None
    __requiredfields__ = ()

    @classmethod
    def find(cls, query):
        collection = db[cls.__collection__]

        return list(map(lambda x: cls(x), [entry for entry in collection.find(query)]))

    @classmethod
    def find_one(cls, query):
        collection = db[cls.__collection__]

        val = collection.find_one(query)

        if not val:
            return None

        return cls(val)

    @classmethod
    def wipe(cls):
        collection = db[cls.__collection__]

        return collection.delete_many({})

    def as_dict(self):
        """Returns the entity as a dictionary. Requires overriding by child classes."""
        return None

    def save(self):
        """Saves a record to the database"""
        collection = db[self.__collection__]

        self_dict = self.as_dict()        

        if self_dict is None:
            raise Exception(f'{self.__class__} has not overridden as_dict() function.')
        
        for field in self.__requiredfields__:
            if field not in self_dict or self_dict[field] is None:
                raise Exception(f'{self.__class__} requires missing field "{field}".')
        # this is so new objects are saved properly
        if self._id is None:
            del self_dict['_id']
        new_id = collection.save(self_dict, manipulate=True)
        if new_id:
            self._id = new_id

    def delete(self):
        """Removes the entity from the collection."""
        if self._id is None:
            raise Exception(f'{self.__class__} Cannot DELETE without id.')
        
        collection = db[self.__collection__]

        result = collection.delete_one({'_id': self._id})
        return result


class UserProfile(BaseModel):
    __collection__ = 'profiles'   
    __requiredfields__ = ('username',) 

    def __init__(self, values=None):
        self.username = None
        self.experience = 0
        self.level = 1
        self.prestige = 0
        self.private = True # user's profile defaults to private
        self._id = None

        if values:
            self.username = values['username']
            self.experience = values['experience']
            self.level = values['level']
            self.prestige = values['prestige']
            self.private = values['private']
            self._id = values['_id']

    def as_dict(self):
        return {
            'username': self.username,
            'experience': self.experience,
            'private': self.private,
            '_id': str(self._id),
            'level': self.level,
            'prestige': self.prestige
        }
