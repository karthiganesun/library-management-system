from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import models,schemas
from datetime import datetime, timedelta
from sqlalchemy import func

def borrow_return(db:Session,borrow:schemas.BorrowBook):
    db_borrow = db.query(models.Borrow).filter(models.Borrow.Title == borrow.Title.lower(), models.Borrow.UserId == borrow.UserId.lower(), models.Borrow.Status == "Active").all()
    book = db.query(models.Book).filter(models.Book.Title == borrow.Title.lower()).first()
    # db_dupborrow = db.query(models.UPBorrow).filter(models.UPBorrow.UserId == borrow.UserId.lower(), models.UPBorrow.UserId == borrow.UserId.lower()).first() 

    fine_perday = 10
    fine = 0
    
    total_quantity = sum(b.Quantity for b in db_borrow)

    if not book:
        raise HTTPException(status_code=404, detail="Book not Found")


    if not db_borrow:
        raise HTTPException(status_code=404, detail="No active borrow found")
    
    if borrow.Quantity < 1:
        raise HTTPException(status_code=403,detail="Invalid book Quantity")    
    
    if borrow.Quantity > total_quantity:
        raise HTTPException(status_code=403, detail=f"Return quantity exceeds borrowed quantity")    
    

    remaining = borrow.Quantity

    for db_borrowing in db_borrow:
        if remaining ==0:
            break
        current_return = min(db_borrowing.Quantity, remaining)


        if db_borrowing.Due_Date < datetime.now().date():
            late_days = (datetime.now().date() -  db_borrowing.Due_Date).days
            fine = late_days * fine_perday
            db_borrow.Fine = fine        
    
        db_return = models.Return(Title=db_borrowing.Title.lower(), UserId=db_borrowing.UserId.lower(), Quantity=borrow.Quantity, Borrow_Date=db_borrowing.Borrow_Date, Due_Date=db_borrowing.Due_Date, Return_Date=datetime.now().date(), Fine=fine,Status="Returned")
        db.add(db_return)
        db_borrowing.Quantity -= current_return

        if db_borrowing.Quantity == 0:
            db_borrowing.Status = "Returned"
        else:
            db_borrowing.Status = "Active" 

        remaining -= current_return    

    
    
    book.Quantity += borrow.Quantity
    
    # db_borrow.Status = "Returned"   

  
          
    
    db.commit()   
    db.refresh(db_return)         

    # if db_dupborrow.Quantity == 0 and db_dupborrow.Fine == 0:
    #     db.delete(db_dupborrow)   # bug_ID = 4       

    # if db_borrow.Quantity >= 1:   # bug_ID = 5
    #     db_return = models.Return(Title=db_borrow.Title.lower(), UserId=db_borrow.UserId.lower(), Quantity=borrow.Quantity, Borrow_Date=db_borrow.Borrow_Date, Due_Date=db_borrow.Due_Date, Return_Date=datetime.now().date(), Fine=fine,Status="Aactive")
     
    # db.add(db_return)     
    # db.commit()   
    # db.refresh(db_return) 

    return db_return    





def getid_return(db:Session, user_id:str):
    db_user =  db.query(models.Return).filter(models.Return.UserId == user_id.lower()).all()
    

    if not db_user:
        raise HTTPException(status_code=404, detail="User not Found")
    else:
        return db_user   
