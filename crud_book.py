from fastapi import FastAPI,HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from . import schemas, models
from sqlalchemy import func



def create_book(db:Session,user:schemas.CreateBook):
	db_book = db.query(models.Book).filter(models.Book.Title == user.Title.lower()).first()
	

	if db_book:
		raise HTTPException(status_code=409,detail="Book already exists ")
	
	# if 1 < db_book.Quantity > 15:
	# 	raise HTTPException(status_code=403, detail="add only 0 to 20 books ")
	
	else:
		# book = models.Book(Book_Id = user.Book_Id.lower(), Title = user.Title.lower(), Author = user.Author.lower(), Quantity = user.Quantity)
		# book = models.Book(Title = user.Title.lower(), Author = user.Author.lower(), Quantity = user.Quantity) #---bud_ID - 1
		book = models.Book(Image = user.Image,Title = user.Title.lower(), Author = user.Author.lower(), Quantity = user.Quantity, Total_Quantity = user.Quantity, Created_At = datetime.now())
		db.add(book)
		db.commit()
		db.refresh(book)
	return book


def update_book(db:Session, Title:str, user:schemas.CreateBook):
	db_book = db.query(models.Book).filter(models.Book.Title == Title.lower()).first()
	
	if not db_book:
		raise HTTPException(status_code=404, detail="Book not Found ")
	
	# if user.Total_Quantity is not None:
	# 	if not(0 < user.Total_Quantity > 15):
	# 		raise HTTPException(status_code=403, detail="add only 0 to 20 books")
	
	else:

		for key, value in user.dict(exclude_unset=True).items():						
			setattr(db_book, key, value.lower() if isinstance(value, str) else value)
			#setattr(db_book, key, value)

		db_book.Updated_At = datetime.now().date()
		db_book.Total_Quantity = user.Quantity
		db.commit()
		db.refresh(db_book)	

	return {"message":"successfull updated"}


def get_book(db:Session):
	return db.query(models.Book).all()

def delete_book(db:Session, Title:str, ):
	db_book = db.query(models.Book).filter(models.Book.Title == Title.lower()).first()
	
	if not db_book:
		raise HTTPException(status_code=404, detail="Book not Found ")
	
	else:
		db.delete(db_book)
		db.commit()
	return{"message":"successfully deleted"}



def search_book(db:Session, title:str):
    db_title = db.query(models.Book).filter(models.Book.Title.ilike(f"%{title.lower()}%")).all()

    if not db_title:
        raise HTTPException(status_code=404, detail="Book not Found")
    return db_title 


def search_author(db:Session, author:str):
	db_author = db.query(models.Book).filter(models.Book.Author.ilike(f"%{author.lower()}%"))
	 
	if not db_author:
		raise HTTPException(status_code=404, detail="Book not Found")
	
	return db_author 


def book_report(db:Session):
	db_book = db.query(func.sum(models.Book.Total_Quantity)).scalar() or 0
	db_stock = db.query(func.sum(models.Book.Quantity)).scalar() or 0
	
	db_borrow = db.query(func.sum(models.Borrow.Quantity)).scalar() or 0

	return {"Total_Books":db_book,
		 	"Stock":db_stock,
		 	"Borrow_Quantity": db_borrow
		 }