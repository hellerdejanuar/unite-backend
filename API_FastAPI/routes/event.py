from fastapi import APIRouter, Response, status
from config.db import engine, Session
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.event import Event
from models.user import User, attending_event_rel
from schemas.event import EventSchema
from starlette.status import (HTTP_204_NO_CONTENT, 
                              HTTP_404_NOT_FOUND, 
                              HTTP_405_METHOD_NOT_ALLOWED, 
                              HTTP_409_CONFLICT)
from sqlalchemy import insert, select, update, delete
from datetime import datetime

eventAPI = APIRouter()
conn = engine.connect()

# GET -----------------------
"""@eventAPI.get('/event/{id}', response_model=EventSchema, tags=["Events"])
def get_event(id: int):
    Get event by id 
    return conn.execute(select(Event).where(Event.id == id)).first()
"""

@eventAPI.get('/event/{id}', response_model=EventSchema, tags=["Events"])
def get_event(id: int):
    """ Get event by id """

    public_data = conn.execute(select(Event).where(Event.id == id)).first()
    print(public_data.keys())
    if public_data is None:
        return Response(status_code=HTTP_404_NOT_FOUND)

    participants_list = conn.execute( # Many to many relationship join query
        select(attending_event_rel, User)
        .join(User, attending_event_rel.c.user_id == User.id)
        .where(attending_event_rel.c.event_id == id)).all()
    
    # This loop creates a dict from the query object's basic attributes (not relational)
    dic = {}
    for key in Event.attrs():
        dic[key] = public_data.__getattribute__(key)

    # This loops parses only needed attrs from the relational query response
    dic["participants"] = []
    for i, row in enumerate(participants_list):
        dic["participants"].append({})
        for key in User.attrs():
            dic["participants"][i][key] = getattr(row, key)

    return JSONResponse(jsonable_encoder(dic))


@eventAPI.get('/event', response_model=List[EventSchema], tags=["Events"])
def get_all_events():                         # TODO: update attr parsing to list comprehension
    """ All active events """
    with Session() as session:

        public_data = session.query(Event).where(Event.status == True)

        # This loop creates a dict from the query object's basic attributes (not relational)
        list = []
        for i, row in enumerate(public_data):
            list.append({})
            for key in Event.attrs():
                list[i][key] = getattr(row, key)

        return JSONResponse(jsonable_encoder(list))


"""@eventAPI.get('/event/inactive', response_model=List[EventSchema], tags=["Events"])
def get_inactive_events():
    #All inactive 
    with Session() as session:

        public_data = session.query(Event).where(Event.status == False)

        # This loop creates a dict from the query object's basic attributes (not relational)
        list = []
        for i, row in enumerate(public_data):
            list.append({})
            for key in Event.attrs():
                list[i][key] = getattr(row, key)

        return JSONResponse(jsonable_encoder(list))"""


# CREATE, UPDATE, DELETE ----
@eventAPI.post('/event', response_model=EventSchema, tags=["Events"])
def create_event(this_event: EventSchema):
    """ Create new event """

    new_event = {"name": this_event.name,
                 "event_host_id": this_event.event_host_id,
                 "event_datetime": this_event.event_datetime,
                 "location": this_event.location, 
                 "description": this_event.description,
                 "image_URL": this_event.image_URL,
                 "icon": this_event.icon,
                 "max_people": this_event.max_people, 
                 "config": this_event.config}

    # Realiza la conexion con la base de datos para insertar el nuevo usuario
    with Session() as session:
        result = session.execute(insert(Event).values(new_event))
        session.commit()
        if result is None:
            return HTTP_405_METHOD_NOT_ALLOWED
        
        print("NEW EVENT . id: ", result.lastrowid)
        # Busca en la base de datos el ultimo evento creado y lo retorna para confirmar que se cre
        new_event["id"] = result.lastrowid
        return new_event


@eventAPI.put('/event/{id}', response_model=EventSchema, tags=["Events"], response_model_exclude_unset=True)
def update_event(id: int, this_event: EventSchema):
    """ Update event """
    
    conn.execute(update(Event).values(
                 name=this_event.name,
                 event_datetime=this_event.event_datetime,
                 location=this_event.location, 
                 description=this_event.description,
                 image_URL=this_event.image_URL,
                 icon=this_event.icon,
                 max_people=this_event.max_people, 
                 config=this_event.config,
                 updated_at=datetime.now()).where(Event.id == id))
    conn.commit()
    return conn.execute(select(Event).where(Event.id == id)).first()


@eventAPI.delete('/event/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Events"])
def delete_event(id: int): 
    """ Delete (deactivate) event """

    conn.execute(update(Event).values(
        status=False,
        updated_at=datetime.now()).where(Event.id == id))
    conn.commit()
    return Response(status_code=HTTP_204_NO_CONTENT) # Delete successful, no redirection needed


# JOIN & UNJOIN -------------
@eventAPI.post('/event/{event_id}/join', tags=["Events"])
def join_event(event_id: int, user_id: int):
    """ Join event by ID """
    event = conn.execute(select(Event).where(Event.id == event_id)).first()
    if event is None:
        return Response(status_code=HTTP_404_NOT_FOUND)

    if event.event_host_id == user_id:
        return Response(status_code=HTTP_405_METHOD_NOT_ALLOWED)

    if event.people_count < event.max_people: 
        conn.execute(insert(attending_event_rel)
                    .values(user_id=user_id, event_id=event_id)
                    .prefix_with("IGNORE", dialect="mysql"))

        conn.execute(update(Event)      # Increment people count 
                        .values(people_count=Event.people_count + 1)
                        .where(Event.id == event_id))
        conn.commit()

        new = conn.execute(select(attending_event_rel)  # Select attended event
                            .where(attending_event_rel.c.user_id == user_id)
                            .where(attending_event_rel.c.event_id == event_id)).first()
        return new or Response(status_code=HTTP_404_NOT_FOUND)

    else: return Response(status_code=HTTP_409_CONFLICT) # Already reached max_people

@eventAPI.delete('/event/{event_id}/join', tags=["Events"])
def unjoin_event(event_id: int, user_id: int):
    """ Unjoin event by ID """

    event = conn.execute(select(attending_event_rel)
                .where(attending_event_rel.c.user_id == user_id)
                .where(attending_event_rel.c.event_id == event_id)).first()

    if event is not None:
        conn.execute(delete(attending_event_rel)
                .where(attending_event_rel.c.user_id == user_id)
                .where(attending_event_rel.c.event_id == event_id))

        conn.execute(update(Event)      # Decrement people count 
                    .values(people_count=Event.people_count - 1)
                    .where(Event.id == event_id))
        conn.commit()
        return Response(status_code=HTTP_204_NO_CONTENT) # Successfully deleted

    else:
        return Response(status_code=HTTP_404_NOT_FOUND)
