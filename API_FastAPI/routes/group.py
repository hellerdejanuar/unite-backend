from fastapi import APIRouter, Response, status
from config.db import engine
from typing import List
from models.group import Group
from schemas.group import GroupSchema
from starlette.status import HTTP_204_NO_CONTENT
from sqlalchemy import insert, select, update, delete

groupAPI = APIRouter()
conn = engine.connect()

# GET -----------------------
@groupAPI.get('/group', response_model=List[GroupSchema], tags=["Groups"])
def get_all_groups():
    """ All active groups """
    return conn.execute(select(Group).where(Group.status == True)).fetchall() # TEST this


@groupAPI.get('/group/inactive', response_model=List[GroupSchema], tags=["Groups"])
def get_inactive_groups():
    """ All inactive """
    return conn.execute(select(Group).where(Group.status == False)).fetchall()  # consulta a toda la tabla


@groupAPI.get('/group/{id}', response_model=GroupSchema, tags=["Groups"])
def get_group(id: str):
    """ Get group by id """
    return conn.execute(select(Group).where(Group.id == id)).first()


# CREATE, UPDATE, DELETE ----
@groupAPI.post('/group', response_model=GroupSchema, tags=["Groups"])
def create_group(this_group: GroupSchema):
    """ Create group """
    
    new_group = {"name": this_group.name, 
                "description": this_group.description,
                "group_admin_id": this_group.group_admin_id}

    result = conn.execute(insert(Group).values(new_group)) # Realiza la conexion con la base de datos para insertar el nuevo grupo
    print("NEW GROUP . id: ", result.lastrowid)
    conn.commit()    
    # Busca en la base de datos el ultimo grupo creado y lo retorna para confirmar que se creó
    return conn.execute(select(Group).where(Group.id == result.lastrowid)).first()


@groupAPI.put('/group/{id}', response_model=GroupSchema, tags=["Groups"])
def update_group(id: str, this_group: GroupSchema):
    """ Update Group """

    conn.execute(update(Group).values(
                 name=this_group.name,
                 description=this_group.description,
                 group_admin_id=this_group.group_admin_id,
                 updated_at=datetime.now()
                 ).where(Group.id == id))
    conn.commit()

    return conn.execute(select(Group).where(Group.id == id)).first()


@groupAPI.delete('/group/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Groups"])
def delete_group(id: str):
    """ Delete (deactivate) group """

    conn.execute(update(Group).values(
        status=False,
        updated_at=datetime.now()).where(Group.id == id))
    conn.commit()

    return Response(status_code=HTTP_204_NO_CONTENT) # Delete successful, no redirection needed