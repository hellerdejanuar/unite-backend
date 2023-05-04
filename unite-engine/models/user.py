from sqlalchemy import Table, Column, ForeignKey
from models.user_rel import attending_event_rel, contact_rel, friendship_rel
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean
from models.base_model import BaseModel, Base

class User(BaseModel):

    __tablename__ = "user_data"
    name = Column(String(255))

    email = Column(String(255))
    password = Column(String(255))
    phone = Column(String(255))
    image_URL = Column(String(511), default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460__480.png")
    #Column("login_token", String(255)),
    status = Column(Boolean, default=True)

    # Relationships --
    hosted_events = relationship('Event', back_populates='event_host')
    attending_events = relationship('Event', secondary=attending_event_rel, 
                                            back_populates='participants')

    contacts = relationship("User", secondary=contact_rel, 
                                    primaryjoin="User.id==contact_rel.c.user_id",
                                    secondaryjoin="User.id==contact_rel.c.contact_id",
                                    back_populates='in_contacts_of')

    in_contacts_of = relationship("User", secondary=contact_rel,
                                        primaryjoin="User.id==contact_rel.c.contact_id",
                                        secondaryjoin="User.id==contact_rel.c.user_id",
                                        back_populates='contacts')

    friends = relationship("User", secondary=friendship_rel,
                                   primaryjoin="User.id==friendship_rel.c.user_id",
                                   secondaryjoin="User.id==friendship_rel.c.friend_id",
                                   backref='friend_of')

    admin_groups = relationship('Group', back_populates='group_admin')
    admin_channels = relationship('Channel', back_populates='channel_admin')

    @classmethod
    def attrs(cls, str=None):
        """ Returns a list of or attributes for the given class """
        base_attrs = BaseModel.attrs()

        public_attrs = [
                "name",
                "email",
                "phone",
                "image_URL",
                "status"]

        priv_attrs = [
                "hosted_events",
                "attending_events",
                "admin_groups",
                "admin_channels"
                #"contacts",
                #"in_contacts_of"
                ]
        
        sys_excl = ["password"]

        if str == None:
            return base_attrs + public_attrs
        elif str == "all":
            return base_attrs + public_attrs + priv_attrs
        elif str == "rel":
            return priv_attrs
