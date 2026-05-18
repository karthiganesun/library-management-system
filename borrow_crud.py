from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import models,schemas
from datetime import datetime, timedelta
from sqlalchemy import func



def borrow_book(db:Session, borrow:schemas.BorrowBook):
    db_book = db.query(models.Book).filter(models.Book.Title == borrow.Title.lower()).first()
    db_user = db.query(models.User).filter(models.User.UserId == borrow.UserId.lower()).first()
    db_borrow = db.query(models.Borrow).filter(models.Borrow.UserId == borrow.UserId.lower()).first()
    # db_dupborrow = db.query(models.UPBorrow).filter(models.UPBorrow.UserId == borrow.UserId.lower()).first() 
    db_rfine = db.query(models.Return).filter(models.Return.UserId == borrow.UserId.lower(),models.Return.Fine >0).all()

    active_fine = sum(f.Fine for f in db_rfine)

    # active_fine = db.query(models.Borrow).filter(models.Borrow.UserId == borrow.UserId.lower(),models.Borrow.Fine >0).first()

    total_book = db.query(func.sum(models.Borrow.Quantity)).filter(models.Borrow.UserId == borrow.UserId.lower()).scalar() or 0

    # borrowed_count = sum(book.Quantity for book in total_book)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not Found")
    
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not Found")

    if active_fine:
        raise HTTPException(status_code=403, detail=f"Kindly pay the Fine amount, {active_fine}")       
         
    if db_book.Quantity <= 0:
        raise HTTPException(status_code=400, detail="Book out of stock")
    
    if borrow.Quantity > db_book.Quantity:
        raise HTTPException(status_code=400,detail=f"Only {db_book.Quantity} books available")
    
    if  borrow.Quantity < 1 or borrow.Quantity > 3:
        raise HTTPException(status_code=400, detail=" Student can borrow between 1 and 3 books")
    
    if total_book + borrow.Quantity >3:
        raise HTTPException(status_code=400, detail="Student can borrow maximum 3 books only")


    else:
        Due_Date = datetime.now() + timedelta(days=7)
        newborrow = models.Borrow(Title=borrow.Title.lower() , UserId=borrow.UserId.lower(), Quantity=borrow.Quantity , Borrow_Date=datetime.now(), Due_Date=Due_Date, Status="Active")
        # newborrowdup = models.UPBorrow(Title=borrow.Title.lower() , UserId=borrow.UserId.lower(), Quantity=borrow.Quantity , Borrow_Date=datetime.now(), Due_Date=Due_Date, Status="Active")
        db_book.Quantity-=borrow.Quantity

        db.add(newborrow)
        # db.add(newborrowdup)

        db.commit()
        
        db.refresh(newborrow)
        # db.refresh(newborrowdup)
    return newborrow    


def get_borrow(db:Session):
    return db.query(models.UPBorrow).all()


def borrow_return(db:Session,borrow:schemas.BorrowBook):
    db_borrow = db.query(models.Borrow).filter(models.Borrow.Title == borrow.Title.lower(), models.Borrow.UserId == borrow.UserId.lower()).first()
    book = db.query(models.Book).filter(models.Book.Title == borrow.Title.lower()).first()
    db_dupborrow = db.query(models.UPBorrow).filter(models.UPBorrow.UserId == borrow.UserId.lower(), models.UPBorrow.UserId == borrow.UserId.lower()).first() 

    fine_perday = 10
    fine = 0
    
    total_book = db.query(func.sum(models.UPBorrow.Quantity)).filter(models.UPBorrow.UserId == borrow.UserId.lower()).scalar() or 0

    if not book:
        raise HTTPException(status_code=404, detail="Book not Found")


    if not db_dupborrow:
        raise HTTPException(status_code=404, detail="No active borrow found")
    
    if borrow.Quantity < 1:
        raise HTTPException(status_code=403,detail="Invalid book Quantity")    
    
    if  db_dupborrow.Quantity < borrow.Quantity:
        raise HTTPException(status_code=403, detail=f"Return quantity exceeds borrowed quantity")    
    
    if db_borrow.Due_Date < datetime.now().date():
        late_days = (datetime.now().date() -  db_borrow.Due_Date).days
        fine = late_days * fine_perday
        db_borrow.Fine = fine
        db_dupborrow.Fine = fine
    
    
    book.Quantity += borrow.Quantity
    db_dupborrow.Quantity -= borrow.Quantity
    db_borrow.Status = "Returned"
    db_dupborrow.Status = "Returned"
    db.commit()  
    

    db_return = models.Return(Title=db_borrow.Title.lower(), UserId=db_borrow.UserId.lower(), Quantity=borrow.Quantity, Borrow_Date=db_borrow.Borrow_Date, Due_Date=db_borrow.Due_Date, Return_Date=datetime.now().date(), Fine=fine,Status="Returned")
           
    db.add(db_return)        

    if db_dupborrow.Quantity == 0 and db_dupborrow.Fine == 0:
        db.delete(db_dupborrow)

    db.commit()   
    db.refresh(db_return)    

    if db_dupborrow.Quantity >= 1:
        db_return = models.Return(Title=db_borrow.Title.lower(), UserId=db_borrow.UserId.lower(), Quantity=borrow.Quantity, Borrow_Date=db_borrow.Borrow_Date, Due_Date=db_borrow.Due_Date, Return_Date=datetime.now().date(), Fine=fine,Status="Aactive")
     
    db.add(db_return)     
    db.commit()   
    db.refresh(db_return) 

    return db_return    




def getid_borrow(db:Session, user_id:str):
    db_user =  db.query(models.Borrow).filter(models.Borrow.UserId == user_id.lower()).all()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not Found")
    else:
        return db_user



def getid_return(db:Session, user_id:str):
    db_user =  db.query(models.Return).filter(models.Return.UserId == user_id.lower()).all()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not Found")
    else:
        return db_user   


    


def pay_fine(db:Session, userid:str, amount:float):
    db_user = db.query(models.Return).filter(models.Return.UserId == userid.lower(),models.Return.Fine >0).all()
    db_dupborrow = db.query(models.UPBorrow).filter(models.UPBorrow.UserId == borrow.UserId.lower()).first() 
    db_borrow = db.query(models.Borrow).filter(models.Borrow.UserId == borrow.UserId.lower()).first() 
    data = [db_user,db_borrow,db_dupborrow]

    total_fine = sum(f.Fine for f in db_user)

    balance_fine = sum(f.Fine for f in db_user) - amount

    if not db_user:
        raise HTTPException(status_code=404, detail="No pending fine found")
    
    if amount<=0:
        raise HTTPException(status_code=403, detail="something went wrong, Amount!")
    
    if amount > balance_fine:
        raise HTTPException(status_code=403, detail="Amount exceeds of Fine amount")
    
    for borrow in data:
        borrow.Fine = balance_fine

    try:
        db.commit()

    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Payment Failed")    
    return {
        "message":f"Fine paid successfully for {userid}",
        "paid_amount" : amount
    }    




def view_fine(db:Session, userid:str):
    db_user = db.query(models.Return).filter(models.Return.UserId == userid.lower(),models.Return.Fine >0).all()
    
    total_fine = sum(f.Fine for f in db_user)

    if not db_user:
        raise HTTPException(status_code=404, detail="No pending fine found")

    return total_fine
    