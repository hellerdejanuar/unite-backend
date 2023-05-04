from datetime import datetime
from config.db import engine, Session
from cryptography.fernet import Fernet
from fastapi import APIRouter, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.user import User
from models.user_rel import attending_event_rel, contact_rel, friendship_rel
from models.event import Event
from models.group import Group
from models.channel import Channel
from models.util import unpack, unpack_many
from schemas.user import UserSchema, UserSchemaDetail, UserSchemaCreation
from schemas.event import EventSchema
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_200_OK
from sqlalchemy import insert, select, update, delete, join, inspect, and_, or_, not_
from typing import List
import json
import itertools

key = Fernet.generate_key()
f = Fernet(key)

userAPI = APIRouter()
conn = engine.connect()


# QUERIES -------------------
# FEED ----------------------
@userAPI.get('/user/{id}/feed', response_model=List[EventSchema], tags=["Users"])
async def get_feed(id: int):
    with Session() as session:
        user = session.get(User, id)
        friends_events_list = [ friend.hosted_events for friend in user.friends ]

        events_feed = list(itertools.chain.from_iterable(friends_events_list))  # this adds up all the lists of events into a single one
                                                                                # > pending: remove already joined events, 
                                                                                # > pending: FUTURE: remove repeated events 
        hosted_events_list = user.hosted_events
        attending_events_list = user.attending_events
        
        dic = {'events_feed': events_feed,
               'hosted_events': hosted_events_list,
               'attending_events': attending_events_list}

        return JSONResponse(jsonable_encoder(dic))


# GET -----------------------
@userAPI.get('/user/{id}/info', response_model=UserSchemaDetail, tags=["Users"])
def get_user_info(id: int):
    """ Get detailed info of the user """
    with Session() as session:
        this_user = session.get(User, id)
        if this_user is None:
            return Response(status_code=HTTP_404_NOT_FOUND)

        public_attrs = { key: getattr(this_user, key) 
                        for key in User.attrs() 
                        if hasattr(this_user, key)}
        
        hosted_events_list = this_user.hosted_events        # TODO: parsear solo attrs relevantes
        attending_events_list = this_user.attending_events  # con Event.Attrs()
        admin_channels_list = this_user.admin_channels      #
        admin_groups_list = this_user.admin_groups          #

        friends_list = this_user.get_friends() 

        return_dict = public_attrs
        
        return_dict.update({"hosted_events": this_user.hosted_events,
                    "attending_events": this_user.attending_events,
                    "admin_channels": this_user.admin_channels,
                    "admin_groups": admin_groups_list,
                    "friends": friends_list})

        return JSONResponse(jsonable_encoder(return_dict))

@userAPI.get('/user/{id}', response_model=UserSchema, tags=["Users"])
def get_user(id: int):
    """ Get user by id """
    with Session() as session:
        obj = session.get(User, id)
    # conn.execute(select(User).where(User.id == id)).first()  # old query
    return obj or Response(status_code=HTTP_404_NOT_FOUND)
    

@userAPI.get('/user', response_model=List[UserSchema], tags=["Users"])
def get_all_users():
    """ Get all active users """
    # conn.execute(select(User).where(User.status == True)).fetchall()  # Todos los elementos activos
    with Session() as session:
        return session.query(User).filter(User.status == True).all()  # Todos los elementos activos


@userAPI.get('/user/{}/inactive', tags=["Users"])
def get_inactive_users():
    """ All inactive """
    with Session() as session:
        return session.query(User).filter(User.status != True).all()  # Todos los elementos inactivos


# CREATE, UPDATE, DELETE ----
@userAPI.post('/user', response_model=UserSchemaCreation, tags=["Users"], 
                       response_model_exclude_defaults=True,
                       status_code=201)
def create_user(this_user: UserSchema):
    """ Create user """

    new_user = {"name": this_user.name, 
                "email": this_user.email,
                "image_URL": this_user.image_URL,
                "phone": this_user.phone,}

    new_user["password"] = f.encrypt(this_user.password.encode("utf-8"))
    

    with Session() as session:
        result = session.execute(insert(User).values(new_user))
        session.commit()
        new_user["id"] = result.lastrowid
        return new_user


@userAPI.put('/user/{id}', status_code=status.HTTP_200_OK, tags=["Users"])
def update_user(id: int, this_user: UserSchema):
    """ Update User """

    with Session() as session:
        result = session.execute(update(User).values(
                name=this_user.name,
                email=this_user.email,
                phone=this_user.phone,
                image_URL=this_user.image_URL,
                password=f.encrypt(this_user.password.encode("utf-8")),
                updated_at=datetime.now()).where(User.id == id))
        session.commit()
        return {}


@userAPI.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(id: int):
    """ Delete (deactivate) user """

    with Session() as session:
        session.execute(update(User).values(
            status=False,
            updated_at=datetime.now()).where(User.id == id))   # check THIS
        session.commit()

    return Response(status_code=HTTP_204_NO_CONTENT) # Delete successful, no redirection needed


# CONTACTS ------------------
@userAPI.post('/user/{user_id}/contacts/add', tags=["Users"])   
def add_contact(user_id: int, contact_id: int):
    """ add contact """
    with Session() as session:
        resp = session.execute(select(contact_rel) # Checking for preexisting rel
                            .where(and_(contact_rel.c.user_id == user_id,
                                        contact_rel.c.contact_id == contact_id))).first()

        print(resp)    
        if resp is not None:
            return Response(status_code=HTTP_409_CONFLICT)
        
        session.execute(insert(contact_rel).values(user_id=user_id,
                                                contact_id=contact_id))
        session.commit()
        # Return < - TODO


@userAPI.get('/user/{user_id}/contacts', tags=["Users"])    #pending: refactor conn.execute to session.query
def get_user_contacts(user_id: int):
    """ get list of all contacts_id for a user """
    resp = conn.execute(select(contact_rel.c.contact_id)
                        .where(contact_rel.c.user_id == user_id)).all()

    print(resp)
    return [x.values()[0] for x in resp] or Response(status_code=HTTP_404_NOT_FOUND)

@userAPI.get('/user/{user_id}/contacts/info', tags=["Users"])   #pending: refactor conn.execute to session.query
def get_user_contacts_info(user_id: int):
    """ get list of all contacts with details for a user """
    resp = conn.execute(select(User, contact_rel)
                        .join(User, contact_rel.c.contact_id==User.id)
                        .where(contact_rel.c.user_id == user_id)).all()

    return resp or Response(status_code=HTTP_404_NOT_FOUND)


# FRIENDS -------------------
@userAPI.post('/user/{user_id}/friends/add', tags=["Users"])
def add_friend(user_id: int, friend_id:int):
    """ add friend """

    with Session() as session:
        this_user = session.get(User, user_id)
        this_friend = session.get(User, friend_id)

        if this_user is None or this_user.status == False:
            return HTTP_404_NOT_FOUND
        if this_friend is None or this_friend.status == False:
            return HTTP_404_NOT_FOUND

        if this_friend in this_user.friends:
            return HTTP_409_CONFLICT

        session.execute(insert(friendship_rel).values(user_id=user_id,
                                            friend_id=friend_id))
        session.execute(insert(friendship_rel).values(user_id=friend_id, # Bidirectional Friendship
                                            friend_id=user_id))
        session.commit()
        return HTTP_200_OK

@userAPI.delete('/user/{user_id}/friends/remove', tags=["Users"])
def remove_friend(user_id: int, friend_id:int):
    """ remove friend """

    with Session() as session:
        this_user_rel = session.query(friendship_rel).filter(friendship_rel.c.user_id == user_id, 
                                                             friendship_rel.c.friend_id == friend_id)
        this_friend_rel = session.query(friendship_rel).filter(friendship_rel.c.user_id == friend_id, 
                                                               friendship_rel.c.friend_id == user_id)

        if this_user_rel.first() is None:
            return HTTP_404_NOT_FOUND
        if this_friend_rel.first() is None:
            return HTTP_404_NOT_FOUND

        this_user_rel.delete()
        this_friend_rel.delete()

        session.commit()
        return HTTP_200_OK

@userAPI.get('/user/{user_id}/friends', tags=["Users"])
def get_user_friends(user_id: int):
    """ get the friends of a user """

    with Session() as session:
        this_user = session.get(User, user_id)
        return this_user.get_friends()