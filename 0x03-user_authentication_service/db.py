#!/usr/bin/env python3
"""DB module
"""
from user import Base, User
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''Creates and persists in the database a new user'''
        if all(isinstance(el, str) for el in [email, hashed_password]):
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
            return new_user
        else:
            return None

    def find_user_by(self, **kwargs) -> User:
        '''Retrieves an existing user from the database'''
        all_users = self._session.query(User).all()
        if all_users:
            for user in all_users:
                for k in kwargs:
                    if k not in User.__table__.columns:
                        raise InvalidRequestError
                    if getattr(user, k) != kwargs[k]:
                        raise NoResultFound
                return user
            return None
        return None

    def update_user(self, user_id: int, **kwargs) -> None:
        '''Updates an existing User'''
        user = self.find_user_by(id=user_id)
        if not user:
            return None
        for k in kwargs:
            if k not in user.__table__.columns:
                raise ValueError
            setattr(user, k, kwargs[k])
        self._session.commit()
        return None
