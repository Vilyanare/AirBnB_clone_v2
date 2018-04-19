#!/usr/bin/python3
'''
    Define class DBStorage
'''
import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models.base_model import Base
import models


class DBStorage:
    '''
        Links the MySQL database
    '''
    __engine = None
    __session = None

    def __init__(self):
        '''
            Initializes the database storage engine
        '''
        username = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            username, password, host, db), pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        '''
            Returns dictionary of all of type class
            or all of all types if cls == None
                key = <class-name>.<object-id>
                value = object
        '''
        result = {}
        clses = [v for k, v in models.classes.items() if "BaseModel" not in k]
        if cls is not None:
            if isinstance(cls, str):
                cls = models.classes[cls]
            clses = [cls]
        for c in clses:
            for instance in self.__session.query(c):
                key = "{}.{}".format(c().__class__.__name__, instance.id)
                result[key] = instance
        return result

    def new(self, obj):
        '''
            Add obj to current database session
        '''
        self.__session.add(obj)

    def save(self):
        '''
            Commits all changes to the current database session
        '''
        self.__session.commit()

    def delete(self, obj=None):
        '''
            Deletes obj from current database session if obj != None
        '''
        if obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        '''
            Creates all tables in database and creates session
        '''
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                 expire_on_commit=False))
        self.__session = Session()

    def close(self):
        '''
            Removes current session
        '''
        scoped_session(sessionmaker(bind=self.__engine,
                                 expire_on_commit=False)).remove()
