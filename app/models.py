import datetime

from flask_appbuilder import Model
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

mindate = datetime.date(datetime.MINYEAR, 1, 1)


class ContactGroup(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Gender(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Contact(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    address = Column(String(564))
    birthday = Column(Date, nullable=True)
    personal_phone = Column(String(20))
    personal_celphone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey("contact_group.id"), nullable=False)
    contact_group = relationship("ContactGroup")
    gender_id = Column(Integer, ForeignKey("gender.id"), nullable=False)
    gender = relationship("Gender")
    tool_id = Column(Integer, ForeignKey("tool.id"), nullable=True)
    tool = relationship("Tool")
    note = Column(Text)

    def __repr__(self):
        return self.name

    def month_year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, date.month, 1) or mindate

    def year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, 1, 1)

class Child(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    birthday = Column(Date, nullable=True)
    parent_id = Column(Integer, ForeignKey("contact.id"), nullable=False)
    parent = relationship("Contact")

    def __repr__(self):
        return self.name

class Tool(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    description = Column(String(560), nullable=True)
    
    def __repr__(self):
        return self.name
