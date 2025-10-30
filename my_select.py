from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade
from datetime import datetime

# Настройка підключення к БД
engine = create_engine('postgresql://postgres:1234@localhost:5432/postgres')
Session = sessionmaker(bind=engine)

def get_session():
    return Session()

def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів"""
    session = get_session()
    try:
        result = session.query(
            Student.name,
            func.avg(Grade.grade).label('average_grade')
        ).join(Grade).group_by(Student.id)\
         .order_by(desc('average_grade'))\
         .limit(5).all()
        return result
    finally:
        session.close()

def select_2(subject_name):
    """Знайти студента із найвищим середнім балом з певного предмета"""
    session = get_session()
    try:
        result = session.query(
            Student.name,
            func.avg(Grade.grade).label('average_grade')
        ).join(Grade).join(Subject)\
         .filter(Subject.name == subject_name)\
         .group_by(Student.id)\
         .order_by(desc('average_grade'))\
         .first()
        return result
    finally:
        session.close()

def select_3(subject_name):
    """Знайти середній бал у групах з певного предмета"""
    session = get_session()
    try:
        result = session.query(
            Group.name,
            func.avg(Grade.grade).label('average_grade')
        ).select_from(Group)\
         .join(Student)\
         .join(Grade)\
         .join(Subject)\
         .filter(Subject.name == subject_name)\
         .group_by(Group.id, Group.name)\
         .all()
        return result
    finally:
        session.close()

def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)"""
    session = get_session()
    try:
        result = session.query(func.avg(Grade.grade)).scalar()
        return round(result, 2) if result else 0
    finally:
        session.close()

def select_5(teacher_name):
    """Знайти які курси читає певний викладач"""
    session = get_session()
    try:
        result = session.query(Subject.name)\
            .join(Teacher)\
            .filter(Teacher.name == teacher_name)\
            .all()
        return [subject[0] for subject in result]
    finally:
        session.close()

def select_6(group_name):
    """Знайти список студентів у певній групі"""
    session = get_session()
    try:
        result = session.query(Student.name)\
            .join(Group)\
            .filter(Group.name == group_name)\
            .all()
        return [student[0] for student in result]
    finally:
        session.close()

def select_7(group_name, subject_name):
    """Знайти оцінки студентів у окремій групі з певного предмета"""
    session = get_session()
    try:
        result = session.query(
            Student.name,
            Grade.grade,
            Grade.date_received
        ).join(Group)\
         .join(Grade)\
         .join(Subject)\
         .filter(Group.name == group_name, Subject.name == subject_name)\
         .order_by(Student.name)\
         .all()
        return result
    finally:
        session.close()

def select_8(teacher_name):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів"""
    session = get_session()
    try:
        result = session.query(func.avg(Grade.grade))\
            .join(Subject)\
            .join(Teacher)\
            .filter(Teacher.name == teacher_name)\
            .scalar()
        return round(result, 2) if result else 0
    finally:
        session.close()

def select_9(student_name):
    """Знайти список курсів, які відвідує певний студент"""
    session = get_session()
    try:
        result = session.query(Subject.name)\
            .join(Grade)\
            .join(Student)\
            .filter(Student.name == student_name)\
            .distinct()\
            .all()
        return [subject[0] for subject in result]
    finally:
        session.close()

def select_10(student_name, teacher_name):
    """Список курсів, які певному студенту читає певний викладач"""
    session = get_session()
    try:
        result = session.query(Subject.name)\
            .join(Teacher)\
            .join(Grade)\
            .join(Student)\
            .filter(Student.name == student_name, Teacher.name == teacher_name)\
            .distinct()\
            .all()
        return [subject[0] for subject in result]
    finally:
        session.close()

# Додаткові запроси
def select_11(teacher_name, student_name):
    """Середній бал, який певний викладач ставить певному студентові"""
    session = get_session()
    try:
        result = session.query(func.avg(Grade.grade))\
            .join(Subject)\
            .join(Teacher)\
            .join(Student)\
            .filter(Teacher.name == teacher_name, Student.name == student_name)\
            .scalar()
        return round(result, 2) if result else 0
    finally:
        session.close()

def select_12(group_name, subject_name):
    """Оцінки студентів у певній групі з певного предмета на останньому занятті"""
    session = get_session()
    try:
        # Остання дата для даной групи і предмету
        latest_date = session.query(func.max(Grade.date_received))\
            .join(Student)\
            .join(Group)\
            .join(Subject)\
            .filter(Group.name == group_name, Subject.name == subject_name)\
            .scalar()
        
        if not latest_date:
            return []
        
        # Оцінка на останню дату
        result = session.query(
            Student.name,
            Grade.grade
        ).join(Group)\
         .join(Grade)\
         .join(Subject)\
         .filter(
             Group.name == group_name,
             Subject.name == subject_name,
             Grade.date_received == latest_date
         ).all()
        
        return result
    finally:
        session.close()