from datetime import datetime
from fastapi import APIRouter, Response, status
from config.db import engine
from typing import List
from models.channel import Channel
from schemas.channel import ChannelSchema
from starlette.status import HTTP_204_NO_CONTENT
from sqlalchemy import insert, select, update, delete

channelAPI = APIRouter()
conn = engine.connect()

@channelAPI.get('/channel', response_model=List[ChannelSchema], tags=["Channels"])
def get_all_channels():
    return conn.execute(select(Channel).where(Channel.status == True)).fetchall()  # consulta a toda la tabla


@channelAPI.get('/channel/inactive', response_model=List[ChannelSchema], tags=["Channels"])
def get_inactive_channels():
    return conn.execute(select(Channel).where(Channel.status == False)).fetchall()  # consulta a toda la tabla


@channelAPI.get('/channel/{id}', response_model=ChannelSchema, tags=["Channels"])
def get_channel(id: str):
    """ Get channel by id """
    return conn.execute(select(Channel).where(Channel.id == id)).first()


@channelAPI.post('/channel', response_model=ChannelSchema, tags=["Channels"])
def create_channel(this_channel: ChannelSchema):
    """ Create group """
    
    new_channel = {"name": this_channel.name, 
                "description": this_channel.description,
                "channel_admin_id": this_channel.channel_admin_id}

    result = conn.execute(insert(Channel).values(new_channel)) # Realiza la conexion con la base de datos para insertar el nuevo canal
    conn.commit()
    print("NEW CHANNEL . id: ", result.lastrowid)
    # Busca en la base de datos el ultimo grupo canal y lo retorna para confirmar que se creó
    return conn.execute(select(Channel).where(Channel.id == result.lastrowid)).first()


@channelAPI.put('/channel/{id}', response_model=ChannelSchema, tags=["Channels"])
def update_channel(id: str, this_channel: ChannelSchema):
    """ Update Channel """

    conn.execute(update(Channel).values(
                 name=this_channel.name,
                 description=this_channel.description,
                 channel_admin_id=this_channel.channel_admin_id,
                 updated_at=datetime.now()
                 ).where(Channel.id == id))
    conn.commit()

    return conn.execute(select(Channel).where(Channel.id == id)).first()


@channelAPI.delete('/channel/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Channels"])
def delete_channel(id: str):
    """ Delete (deactivate) channel """

    conn.execute(update(Channel).values(
        status=False,
        updated_at=datetime.now()).where(Channel.id == id))
    conn.commit()

    return Response(status_code=HTTP_204_NO_CONTENT) # Delete successful, no redirection needed