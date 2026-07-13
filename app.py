from fastapi import FastAPI , HTTPException ,Depends ,status
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from models import Base , Student
    
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Hello World Tushar"}

@app.post("/addstudent")
def post_student(name: str, age: int ,db: Session = Depends(get_db)):
    if age <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Age must be greater than 0"
        )
    student = Student(name=name, age=age)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@app.get('/students')
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

@app.put('/students/{id}')
def update_student(id: int, name:str ,age: int,db: Session = Depends(get_db)):
    if age <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Age must be greater than 0"
        )
    student = db.query(Student).filter(Student.id == id).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Student with id {id} not found"
        )
    
    student.name=name
    student.age=age

    db.commit()
    db.refresh(student)

    return {"message": "User updated successfully", "user": student}

@app.patch('/students_age/{id}')
def update_student(id: int, age: int, db: Session = Depends(get_db)):
    if age <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Age must be greater than 0"
        )
    student = db.query(Student).filter(Student.id == id).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Student with id {id} not found"
        )
    
    
    student.age=age

    db.commit()
    db.refresh(student)

    return {"message": "Student updated successfully", "student": student}

@app.patch('/students_name/{id}')
def update_student(id: int, name: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Student with id {id} not found"
        )
    
    
    student.name=name

    db.commit()
    db.refresh(student)

    return {"message": "Student updated successfully", "student": student}

@app.delete('/students/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_student(id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {id} not found"
        )
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}
