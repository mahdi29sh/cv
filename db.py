from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref,sessionmaker
 
engine = create_engine('sqlite:///data.db', echo=True)
Base = declarative_base()
 
########################################################################
class User(Base):
    """"""
    __tablename__ = "users"
 
    uid = Column(Integer, primary_key=True , nullable = True)
    username = Column(String , unique = True)
    password = Column(String)
    email = Column(String)
    admin = Column(Integer)

 
    #----------------------------------------------------------------------
    def __init__(self, id, username, password, email, admin):
        """"""
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.admin = admin
########################################################################

class cv(Base):
    __tablename__="cv"

    cvid = Column(Integer,primary_key=True)
    uid = Column(Integer ,ForeignKey(User.uid))
    user = relationship('User')
    img = Column(Text)
    education = Column(Text)
    content = Column(Text)
    document = Column(Text)
    def __init__(self,cvid , uid ,img, education, content  , document):
        self.cvid = cvid
        self.uid = uid
        self.img = img
        self.education = education
        self.content = content
        self.document = document
# create tables
class Comments(Base):
    """"""
    __tablename__ = "comments"
 
    cid = Column(Integer, primary_key=True)
    name = Column(String , ForeignKey(User.uid))
    user = relationship('User')
    content = Column(String)
    cvid = Column(Integer , ForeignKey(cv.cvid))
    cv = relationship('cv')
 
    #----------------------------------------------------------------------
    def __init__(self, cid, name, content, cvid):
        """"""
        self.id = id
        self.name = name
        self.content = content
        self.cvid = cvid
Base.metadata.create_all(engine)

