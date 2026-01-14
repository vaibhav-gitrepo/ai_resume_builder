import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import hashlib

# Fetch credentials from secrets.toml
db_conf = st.secrets["database"]
connection_string = f"mssql+pyodbc://{db_conf['username']}:{db_conf['password']}@{db_conf['server']}/{db_conf['database']}?driver={db_conf['driver']}"

engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    password = Column(String(255))
    full_name = Column(String(100))
    email = Column(String(100))
    
    internships = relationship("Internship", back_populates="owner")

class Internship(Base):
    __tablename__ = "internships"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    organization = Column(String(100))
    role = Column(String(100))
    duration = Column(String(50))
    details = Column(Text)
    
    owner = relationship("User", back_populates="internships")

def init_db():
    Base.metadata.create_all(bind=engine)

def hash_pass(password):
    return hashlib.sha256(str.encode(password)).hexdigest()