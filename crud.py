from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .auth import hashed_password , verify_password
from datetime import datetime, timedelta



def createuser(db:Session,user:schemas.UserCreate):

	db_email = db.query(models.User).filter(
		models.User.Email == user.Email.lower()
		).first()
	db_UserId = db.query(models.User).filter(
		models.User.UserId == user.UserId.lower()
		).first()

	if db_email:
		raise HTTPException(status_code=409,detail="Email Already Exists")
	elif db_UserId:
		raise HTTPException(status_code=409,detail="UserId Already Exists")
	else:
		db_user = models.User(Name = user.Name.lower(), UserId = user.UserId.lower(), Email = user.Email.lower(), Password = hashed_password(user.Password), Role = user.Role.lower() )	
		db.add(db_user)
		db.commit()
		db.refresh(db_user)
	return db_user


def get_users(db:Session):
	return db.query(models.User).all()	


def update_user(db:Session,  user:schemas.UserUpdate):

	db_user = db.query(models.User).filter(models.User.UserId==user.UserId.lower()).first()

	if not db_user:
		raise HTTPException(status_code=404,detail="User not found")
	
	if not verify_password(user.current_Password,db_user.Password):
			raise HTTPException(status_code=401, detail="invalid Password" ) 
	
	else:
		for key, value in user.dict(exclude_unset = True).items():
			if key in ["current_password", "UserId"]:
				continue
			if key == "NewPassword" and value:
				db_user.Password = hashed_password(value)
			else:
				setattr(db_user,key,value.lower() if isinstance(value, str) else value)	

		db.commit()
		db.refresh(db_user)		

		return{"message":"successfull updated"}


def delete_user(db:Session, UserId:str,Password:str):
	db_user = db.query(models.User).filter(models.User.UserId==UserId.lower()).first()
	# db_pass = db.query(models.User).filter(models.User.Password==hashed_password(user.Password)).first()

	if not db_user:
		raise HTTPException(status_code=404,detail="User not found") 
	else:
		# if db_user.Password != hashed_password(Password):
		# 	raise HTTPException(status_code=401, detail="invalid Password" )
		if not verify_password(Password,db_user.Password):
			raise HTTPException(status_code=401, detail="invalid Password" )
		else:

			db.delete(db_user)
			db.commit()
			
			return{"message":"successfully deleted"}	



def login(db:Session, user:schemas.UserLogin):
	db_UserId = db.query(models.User).filter(
		models.User.UserId == user.UserId.lower()
		).first()
	
	max_attempt = 3
	lock_time = 30 


	if not db_UserId :
		raise HTTPException(status_code=404,detail="User not found")
	
	if db_UserId.Lock_until and db_UserId.Lock_until > datetime.now():
		raise HTTPException(status_code=403, detail="Account locked. Try again later")
	
	if verify_password(user.Password, db_UserId.Password):
		db_UserId.Failed_attempt = 0
		db_UserId.Lock_until = None

		db.commit()
		
		# if db_UserId.Role == "student":
		# 	return {"message": "welcome student",  "role": db_UserId.Role}			
			
		# elif db_UserId.Role == "admin":
		# 	return {"message": "welcome admin", "role": db_UserId.Role}
			
		# else:
		# 	raise HTTPException(status_code=403, detail="Invalid role")	
		return {"message":"Login successful",
		  		"UserId": db_UserId.UserId, 
		  		"Role": db_UserId.Role				
				}
					
	
	else:
		db_UserId.Failed_attempt +=1
		db.commit()
		# raise HTTPException(status_code=401,detail="Incorrect Password") 

		if db_UserId.Failed_attempt >= max_attempt:
			db_UserId.Lock_until = datetime.now() + timedelta(seconds= lock_time)	
			db.commit()		
			raise HTTPException(status_code=403,detail="Incorrect password. Too many failed attempts. Account locked for 30 seconds")
		
	

		raise HTTPException(status_code=401,detail=f"Incorrect password. Attempts left: {max_attempt - db_UserId.Failed_attempt}")

	

	
	
		 





"""
	if db_UserId :
		if db_UserId.Password == hashed_password(user.Password) :
			
			if db_UserId.Role == "student":
				return {"message": "welcome student",  "role": db_UserId.Role}
				
				
			elif db_UserId.Role == "admin":
				return {"message": "welcome admin", "role": db_UserId.Role}
				# if True :
				# 	return manage_book()
				# elif False:
				# 	return get_book()
				# else:
				# 	return "thank you"
			else:
				raise HTTPException(status_code=403, detail="Invalid role")				
		
		else:
			raise HTTPException(status_code=401,detail="Incorrect Password") 		

	else:
		raise HTTPException(status_code=404,detail="User not found") 
	
"""




# def add_book(db:Session,user:schemas.CreateBook):
# 	db_book = db.query(models.User).filter(models.User.Book_Id == user.Book_Id).first()

# 	if db_book:
# 		raise HTTPException(status_code=409,detail="BookID already exists ")
	
# 	else:
# 		book = models.book(Book_Id = user.Book_Id.lower(), Title = user.Title.lower(), Author = user.Author.lower(), Quantity = user.Quantity)
# 		db.add(book)
# 		db.commit()
# 		db.refresh(book)
# 	return book


# def get_book(db:Session):
# 	return db.query(models.Book).all()



# def update_book(db:Session, user:schemas.CreateBook):
# 	db_book = db.query(models.User).filter(models.User.Book_Id == user.Book_Id).first()
# 	# db_book = db.query(models.User).filter(models.User.Book_Id == user.Book_Id).first()

# 	if not db_book:
# 		raise HTTPException(status_code=404, detail="Book not Found ")
	
# 	else:
# 		for key, value in user.dict(exclude=True).items():
# 			setattr(user, key, value)

# 	return


   