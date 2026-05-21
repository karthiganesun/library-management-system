from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models, schemas, crud, crud_book, borrow_crud,crud_return
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/", response_model=schemas.UserResponse) #, status_code=status.HTTP_201_CREATED)
def createuser(user:schemas.UserCreate, db:Session = Depends(get_db)):
	return crud.createuser(db,user)

@app.get("/users/", response_model=list[schemas.UserResponse])
def read_user(db:Session=Depends(get_db)):
	return crud.get_users(db)

@app.post("/login/",response_model=schemas.LoginResponse)
def log(user:schemas.UserLogin,db:Session=Depends(get_db)):
	return crud.login(db,user)	

@app.put("/user_update/{UserId}")
def update_user(user:schemas.UserUpdate,db:Session=Depends(get_db)):
	return crud.update_user(db,user)

@app.delete("/user_delete/{UserId}")
def delete_user(UserId:str,Password:str, db:Session=Depends(get_db)):
	return crud.delete_user(db,UserId,Password)






@app.post("/add_book/", response_model=schemas.BookResponse)
def add_book(book:schemas.CreateBook, db:Session=Depends(get_db)):
	return crud_book.create_book(db, book)

@app.get("/view_books/",response_model = list[schemas.BookResponse])
def readall_book(db:Session=Depends(get_db)):
	return crud_book.get_book(db)

@app.put("/book_update/{Title}")
def update_book(Title:str, book:schemas.BookUpdate, db:Session=Depends(get_db)):
	return crud_book.update_book(db, Title, book)

@app.delete("/delete_book/{Title}")
def remove_book(Title:str,db:Session=Depends(get_db)):
	return crud_book.delete_book(db,Title)

@app.get("/book_report/",response_model=schemas.ReportResponse)
def book_report(db:Session=Depends(get_db)):
	return crud_book.book_report(db)



@app.get("/search_book/{title}", response_model=list[schemas.BookResponse])
def search_book(title:str, db:Session=Depends(get_db)):
	return crud_book.search_book(db, title)

@app.get("/search_Author/{title}", response_model=list[schemas.BookResponse])
def search_book(author:str, db:Session=Depends(get_db)):
	return crud_book.search_author(db, author)





@app.post("/borrow_book/",response_model= schemas.BorrowResponse)
def borrow_book(borrow:schemas.BorrowBook, db:Session=Depends(get_db)):
	return borrow_crud.borrow_book(db,borrow)

@app.get("/get_borrow/",response_model=list[schemas.BorrowResponse])
def get_borrow(db:Session=Depends(get_db)):
	return borrow_crud.get_borrow(db)

@app.get("/borrow_getbyID/{user_id}",response_model= list[schemas.BorrowResponse])
def getid_borrow(user_id: str,db:Session=Depends(get_db)):
	return borrow_crud.getid_borrow(db,user_id)







@app.get("/return_getbyID/{user_id}",response_model= list[schemas.ReturnResponse])
def getid_return(user_id: str,db:Session=Depends(get_db)):
	return crud_return.getid_return(db,user_id)

@app.post("/return_book/",response_model= schemas.ReturnResponse)
def borrow_return(borrow:schemas.ReturnBook, db:Session=Depends(get_db)):
	return crud_return.borrow_return(db, borrow)




@app.put("/pay_fine/{userid}")
def pay_fine(userid:str, amount:float, db:Session=Depends(get_db)):
	return borrow_crud.pay_fine(db,userid,amount)

@app.get("/view_fine/")
def view_fine(userid:str, db:Session=Depends(get_db)):
	return borrow_crud.view_fine(db,userid)