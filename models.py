from sqlalchemy import Column, Integer, String, Date,DateTime, Text
from datetime import datetime
from .database import Base 

class User(Base):
	__tablename__ = "user_register"

	Id = Column(Integer, primary_key=True,index=True)
	Name = Column(String,index=True,nullable=False)
	UserId = Column(String, unique=True,nullable=False)
	Email = Column(String,unique=True,index=True,nullable=False)
	Password = Column(String,index=True,nullable=False)
	Role = Column(String,index=True,nullable=False)
	Failed_attempt = Column(Integer,default=0)
	Lock_until = Column(DateTime,nullable=True)
	
	


class Book(Base):
	__tablename__ = "Book_Management"
	
	Id = Column(Integer, primary_key=True, index=True)
	Image = Column(Text,nullable=True)
	Title = Column(String,unique=True,index=True,nullable=False)
	Author = Column(String,index=True,nullable=False)
	Created_At = Column(Date,nullable=False)
	Updated_At = Column(Date,nullable=True)
	Quantity = Column(Integer,index=True,nullable=False)
	Total_Quantity = Column(Integer,index=True,nullable=False)



class Borrow(Base):

	__tablename__ = "Borrow_Book"

	Id = Column(Integer, primary_key=True, index=True)
	Title = Column(String,index=True,nullable=False)
	UserId = Column(String,index=True,nullable=False)
	Quantity = Column(Integer,nullable=False)
	Data_Quantity = Column(Integer,nullable=False)
	Borrow_Date = Column(Date,nullable=False)
	Due_Date = Column(Date,nullable=False)
	Return_Date = Column(Date,nullable=True)
	Fine = Column(Integer,default=0)
	Status = Column(String,index=True,default="None")

"""	
Bug_ID - 3
# class UPBorrow(Base):

# 	__tablename__ = "Clone_Borrow_Book"

# 	Id = Column(Integer, primary_key=True, index=True)
# 	Title = Column(String,index=True,nullable=False)
# 	UserId = Column(String,index=True,nullable=False)
# 	Quantity = Column(Integer,nullable=False)
# 	Borrow_Date = Column(Date,nullable=False)
# 	Due_Date = Column(Date,nullable=False)
# 	Return_Date = Column(Date,nullable=True)
# 	Fine = Column(Integer,default=0)
# 	Total_book = Column(Integer,default=0)
# 	Status = Column(String,index=True,default="Null")

"""

class Return(Base):

	__tablename__ = "Return_Book"
	Id = Column(Integer, primary_key=True, index=True)
	Title = Column(String,index=True,nullable=False)
	UserId = Column(String,index=True,nullable=False)
	Quantity = Column(Integer,nullable=False)
	Borrow_Date = Column(Date,nullable=False)
	Due_Date = Column(Date,nullable=False)
	Return_Date = Column(Date,nullable=True)
	Fine = Column(Integer,default=0)
	Status = Column(String,index=True)




