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
        newborrow = models.Borrow(Title=borrow.Title.lower() , UserId=borrow.UserId.lower(), Quantity=borrow.Quantity , Data_Quantity = borrow.Quantity, Borrow_Date=datetime.now(), Due_Date=Due_Date, Status="Active")
        # newborrowdup = models.UPBorrow(Title=borrow.Title.lower() , UserId=borrow.UserId.lower(), Quantity=borrow.Quantity , Borrow_Date=datetime.now(), Due_Date=Due_Date, Status="Active")
        db_book.Quantity-=borrow.Quantity

        db.add(newborrow)
     
        db.commit()
        
        db.refresh(newborrow)
       
    return newborrow    


def get_borrow(db:Session):
    # return db.query(models.Borrow).all() # bug_ID = 6
    return db.query(models.Borrow).filter( models.Borrow.Status == "Active").all()






def getid_borrow(db:Session, user_id:str):
    db_user =  db.query(models.Borrow).filter(models.Borrow.UserId == user_id.lower()).all()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not Found")
    else:
        return db_user






    


def pay_fine(db:Session, userid:str, amount:float):
    db_user = db.query(models.Return).filter(models.Return.UserId == userid.lower(),models.Return.Fine >0).all()
    # db_dupborrow = db.query(models.UPBorrow).filter(models.UPBorrow.UserId == borrow.UserId.lower()).first() 
    db_borrow = db.query(models.Borrow).filter(models.Borrow.UserId == userid.lower()).first() 
    db_fine = db.query(models.Return).filter(models.Return.UserId == userid.lower()).first() 
    # data = [db_user,db_borrow]

    total_fine = sum(f.Fine for f in db_user)

    # balance_fine = total_fine - amount

    if not db_user:
        raise HTTPException(status_code=404, detail="No outstanding fines found")
    
    if amount<=0:
        raise HTTPException(status_code=403, detail="something went wrong, Amount!")
    
    if  total_fine < amount:
        raise HTTPException(status_code=403, detail="Amount exceeds of Fine amount")
    
    remaining_payment = amount
    for item in db_user:
        if remaining_payment <= 0:
            break

        if item.Fine <= remaining_payment:
            remaining_payment -= item.Fine
            item.Fine = 0

        else:
            item.Fine -= remaining_payment
            remaining_payment = 0

    remaining_fine = sum(item.Fine for item in db_user)    


    try:
        db.commit()

    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Payment Failed")    
    return {
        "message":f"Fine paid successfully for {userid}",
        "paid_amount" : amount,
        "remaining_fine": remaining_fine
    }    




def view_fine(db:Session, userid:str):
    db_user = db.query(models.Return).filter(models.Return.UserId == userid.lower(),models.Return.Fine >0).all()
    
    total_fine = sum(f.Fine for f in db_user)

    if not db_user:
        # raise HTTPException(status_code=404, detail="No pending fine found") # bug_ID = 7
        return {"message":"No outstanding fines found"}

    return total_fine
    