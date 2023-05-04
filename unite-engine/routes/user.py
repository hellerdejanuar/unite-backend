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
               'attending_events_list': attending_events_list}

        return JSONResponse(jsonable_encoder(dic))


# GET -----------------------
@userAPI.get('/user/{id}/info', response_model=UserSchemaDetail, tags=["Users"]) #TODO <-
def get_user_info(id: int):
    """ Get detailed info of the user """
    public_data = conn.execute(select(User).where(User.id == id)).first()
    if public_data is None:
        return Response(status_code=HTTP_404_NOT_FOUND)

    hosted_events_list = conn.execute(select(User.hosted_events, Event) # One to many relationship join query
                                    .join(Event)
                                    .where(User.id == id)).all()
                            
    attending_events_list = conn.execute(select(attending_event_rel, Event) # Many to many relationship join query
                    .join(Event, attending_event_rel.c.event_id == Event.id)
                    .where(attending_event_rel.c.user_id == id)).all()

    """contacts_list = conn.execute( # Many to many relationship join query
        select(contact_rel, User)
        .join(User, contact_rel.c.user_id == User.id)
        .where(contact_rel.c.user_id == id)).all()

    in_contacts_of_list = conn.execute(
        select(contact_rel)
        .where(contact_rel.c.contact_id == id)
        .with_entities(contact_rel.c.user_id)).all()"""

    admin_channels_list = conn.execute(select(User.admin_channels, Channel).join(Channel).where(User.id == id)).all()
    admin_groups_list = conn.execute(select(User.admin_groups, Group).join(Group).where(User.id == id)).all()

    dic = {}
    for key in User.attrs():
            dic[key] = public_data.__getattribute__(key)

    """ these loops parse only needed attrs from the relational query response """
    dic["hosted_events"] = []
    for i, row in enumerate(hosted_events_list):
        dic["hosted_events"].append({})
        for key in Event.attrs():
            dic["hosted_events"][i][key] = getattr(row, key)

    dic["attending_events"] = []
    for i, row in enumerate(attending_events_list):
        dic["attending_events"].append({})
        for key in Event.attrs():
            dic["attending_events"][i][key] = getattr(row, key)

    """dic["contacts"] = []
    for i, row in enumerate(contacts_list):
        dic["contacts"].append({})
        for key in User.attrs(): # This gets the format from the list of attrs
            dic["contacts"][i][key] = getattr(row, key)

    dic["in_contacts_of"] = []
    for elem in in_contacts_of_list:
        dic["in_contacts_of"].append(elem)"""

    return JSONResponse(jsonable_encoder(dic))

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
@userAPI.post('/user', response_model=UserSchemaCreation, tags=["Users"], response_model_exclude_defaults=True)
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
@userAPI.post('/user/{user_id}/contacts/add', tags=["Users"])   #pending: refactor conn.execute to session.query
def add_contact(user_id: int, contact_id: int):
    """ add contact """

    resp = conn.execute(select(contact_rel) # Check for preexisting rel
                        .where(and_(contact_rel.c.user_id == user_id,
                                    contact_rel.c.contact_id == contact_id))).first()
                               
    if resp is not None:
        return Response(status_code=HTTP_409_CONFLICT)
    
    conn.execute(insert(contact_rel).values(user_id=user_id,
                                            contact_id=contact_id))
    conn.commit()
    # Return < - TODO


@userAPI.get('/user/{user_id}/contacts', tags=["Users"])    #pending: refactor conn.execute to session.query
def get_user_contacts(user_id: int):
    """ get list of all contacts_id for a user """

    #with Session() as session:
    
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
def add_friend(user_id: int, friend_id:int):            #TODO: IMPLEMENT ! checking both before committing change
    """ add friend """

    with Session() as session:
        session.execute(insert(friendship_rel).values(user_id=user_id,
                                            friend_id=friend_id))
        session.execute(insert(friendship_rel).values(user_id=friend_id, # Bidirectional Friendship
                                            friend_id=user_id))
        session.commit()
        return HTTP_200_OK


@userAPI.get('/user/{user_id}/friends', tags=["Users"])
def get_user_friends(user_id: int):
    """ get the friends of a user """

    with Session() as session:
        user = session.get(User, user_id)
        print([x.hosted_events for x in user.friends])
        return jsonable_encoder([x.id for x in user.friends])