from pydantic import BaseModel,EmailStr, field_validator, Field
from datetime import date
from typing import Optional,Dict
import re





class UserCreate(BaseModel):
    Name: str
    UserId: str
    Email: EmailStr
    Password: str
    Role: str


    @field_validator("UserId")
    @classmethod
    def validate_userid(cls, value):
        value = value.lower()
        pattern = r"^[a-z0-9_]+$"

        if len(value) < 4 or len(value) > 15:
            raise ValueError("UserId must be between 4 and 15 characters")            
        
        if " " in value:
            raise ValueError("UserId cannot contain spaces")
        
        if not re.fullmatch(pattern, value):
            raise ValueError("UserId can contain only letters, numbers and underscore")
        
        if not  re.search(r"[a-z]", value):
            raise ValueError("UserId must contain at least one letter")

        if not  re.search(r"\d", value):
            raise ValueError("UserId must contain at least one number") 
        
        return value
        
    
    @field_validator("Email")
    @classmethod
    def validate_email(cls, value):

        pattern = r"^[a-zA-Z0-9_.]+@[a-zA-Z0-9_.]+\.[a-zA-Z]{2,}$"

        if not re.match(pattern, value):
            raise ValueError("Invalid email format")

        return value
    


    @field_validator("Password")
    @classmethod
    def validate_password(cls, value):

        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

        if not re.match(pattern, value):
            raise ValueError(
                "Password must contain combination of uppercase, lowercase, number, special character and minimum 8 characters"
            )

        return value

    

class UserResponse(BaseModel):
    Id : int
    Name : str
    UserId : str
    Email : EmailStr
    Role : str 


    class Config:
        from_attributes = True 
    
    

class UserLogin(BaseModel):
    UserId : str
    Password : str

class LoginResponse(BaseModel):
    message: str
    UserId : str
    Role : str
    
    class Config:
        from_attributes = True 

class CreateBook(BaseModel): 
    
    Title : str
    Image : Optional[str] = None
    Author: str
    Quantity : int = Field(gt=0,le=20)
    
    # Total_Quantity : int #---bud_ID - 2


class BookResponse(BaseModel):
    
    Id : int
    Image : Optional[str] = None
    Title : str
    Author: str
    Quantity : int
    Total_Quantity : int 
    Created_At: date
    Updated_At :  Optional[date] = None


    class Config:
        from_attributes = True 



class BorrowBook(BaseModel):
    
    Title : str
    UserId : str
    Quantity: int
    # Quantity: int = Field(gt=0)
    # Borrow_Date : date
    

class BorrowResponse(BaseModel): 	
    Title : str
    UserId : str
    Quantity : int
    Due_Date : date
    Status : str



    class Config:
        from_attributes = True 	

class ReturnBook(BaseModel):
    
    Title : str
    UserId : str
    Quantity: int = Field(gt=0,le=3)


class ReturnResponse(BaseModel): 	
    Title : str
    UserId : str
    Quantity : int
    Borrow_Date : date
    Due_Date : date
    Return_Date : Optional[date] = None
    Fine : Optional[float] = None
    Status : str
    

    


    class Config:
        from_attributes = True 

class ReportResponse(BaseModel):
    Total_Books : int 
    Stock : int 
    Borrow_Quantity : int  





    
class UserUpdate(BaseModel):
    UserId : str
    current_Password: str
                
    Name : Optional[str] = None   
    Email : Optional[EmailStr] = None
    NewPassword : Optional[str] = None
    Role : Optional[str] = None

    @field_validator("NewPassword")
    @classmethod
    def validate_password(cls, value):

        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if value is None:
            return value

        if not re.match(pattern, value):
            raise ValueError(
                "Password must contain combination of uppercase, lowercase, number, special character and minimum 8 characters"
            )

        return value



class BookUpdate(BaseModel):
    
    Title : Optional[str] = None
    Author: Optional[str] = None
    Quantity: Optional[int] = Field(default=None, gt=0,le=20)
    # Total_Quantity : Optional[int] = None






# class UserCreate(BaseModel):
# 	Name : str
# 	UserId : str
# 	Email : EmailStr
# 	Password : str
# 	Role : str 


# 	@classmethod
# 	@field_validator('Password')
# 	def validate_password(cls, value):
# 		pattren = r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}"

# 		if not re.match(pattren, value):
# 			 raise ValueError("Password must contain uppercase, lowercase, number, special character and minimum 8 characters")
        
# 		return value