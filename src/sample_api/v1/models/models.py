from sqlalchemy import CHAR, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class HousingType(Base):
    __tablename__ = 'housing_types'
    __table_args__ = {'schema': 'housing'}
    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('housing.housing_type_id_seq'::regclass)"))
    code = Column(CHAR(3), nullable=False, unique=True)
    description = Column(String(50), nullable=False)


class Housing(Base):
    __tablename__ = 'housing'
    __table_args__ = {'schema': 'housing'}
    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('housing.housing_id_seq'::regclass)"))
    address = Column(String(50), nullable=False)
    street = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    postal_code = Column(CHAR(6), nullable=False)
    housing_type_id = Column(ForeignKey(
        'housing.housing_types.id'), nullable=False)
    housing_type = relationship('HousingType')
