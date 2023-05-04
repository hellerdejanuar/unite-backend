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

    # CUSTOM METHODS --------
    def get_friends(self):
        """ Returns a list of friends showing just its public attrs """

        return_list = []

        for friend in self.friends:
            if friend.status == True:           # return only active users
                friend_dict = { key: getattr(friend, key)  # parse just public attrs (default)
                                for key in User.attrs() if hasattr(friend, key) }
                return_list.append( friend_dict )

        return return_list


    # COMMON METHODS --------
    @classmethod
    def attrs(cls, attr_selector=None):
        """ Returns a list of or attributes for the given class
            attr_selector is a string that calls a list of attributes
            as stated below """
            
        base_attrs = BaseModel.attrs()

        public_attrs = [ 
                "name",
                "email",
                "phone",
                "image_URL",
                "status"]

        private_attrs = [
                "hosted_events",
                "attending_events",
                "admin_groups",
                "admin_channels",
                "friends"
                #"contacts",
                #"in_contacts_of",
                ]
        
        sys_excl = ["password"]

        match attr_selector:
            case None:
                return base_attrs + public_attrs
            case "all":
                return base_attrs + public_attrs + private_attrs
            case "private":
                return private_attrs
            case "password":
                return sys_excl
