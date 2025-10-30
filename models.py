from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Group(id={self.id}, name='{self.name}')"

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))
    
    # Relationships
    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")
    
    def __init__(self, name, group_id=None):
        self.name = name
        self.group_id = group_id

    def __repr__(self):
        return f"Student(id={self.id}, name='{self.name}', group_id={self.group_id})"

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    
    # Relationships
    subjects = relationship("Subject", back_populates="teacher")
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Teacher(id={self.id}, name='{self.name}')"

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    
    # Relationships
    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")
    
    def __init__(self, name, teacher_id=None):
        self.name = name
        self.teacher_id = teacher_id

    def __repr__(self):
        return f"Subject(id={self.id}, name='{self.name}', teacher_id={self.teacher_id})"

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    grade = Column(Integer, nullable=False)
    date_received = Column(Date, nullable=False)
    
    # Relationships
    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")
    
    def __init__(self, grade, date_received, student_id=None, subject_id=None):
        self.grade = grade
        self.date_received = date_received
        self.student_id = student_id
        self.subject_id = subject_id

    def __repr__(self):
        return f"Grade(id={self.id}, student_id={self.student_id}, subject_id={self.subject_id}, grade={self.grade})"

# Set up back-populates for Group
Group.students = relationship("Student", back_populates="group")