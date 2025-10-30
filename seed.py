from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Group, Student, Teacher, Subject, Grade
from faker import Faker
import random
from datetime import date, timedelta

def seed_database():
    engine = create_engine('postgresql://postgres:1234@localhost:5432/postgres')
    Base.metadata.bind = engine
    Session = sessionmaker(bind=engine)
    session = Session()
    
    fake = Faker()

    try:
        # Clear existing data
        session.query(Grade).delete()
        session.query(Student).delete()
        session.query(Subject).delete()
        session.query(Teacher).delete()
        session.query(Group).delete()

        # Create groups
        groups = []
        for i in range(1, 4):
            group = Group(name=f"Group {i}")
            groups.append(group)
            session.add(group)
        session.commit()

        # Create teachers
        teachers = []
        for _ in range(5):
            teacher = Teacher(name=fake.name())
            teachers.append(teacher)
            session.add(teacher)
        session.commit()

        # Create subjects
        subjects = []
        subject_names = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'History', 'Literature', 'Computer Science', 'Economics']
        for name in subject_names:
            subject = Subject(name=name, teacher_id=random.choice(teachers).id)
            subjects.append(subject)
            session.add(subject)
        session.commit()

        # Create students
        students = []
        for _ in range(30):
            student = Student(
                name=fake.name(),
                group_id=random.choice(groups).id
            )
            students.append(student)
            session.add(student)
        session.commit()

        # Create grades for each student
        for student in students:
            for subject in subjects:
                for _ in range(random.randint(10, 20)):
                    grade = Grade(
                        student_id=student.id,
                        subject_id=subject.id,
                        grade=random.randint(60, 100),
                        date_received=fake.date_between(start_date='-1y', end_date='today')
                    )
                    session.add(grade)
        session.commit()

        print("Database seeded successfully!")
        
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
    finally:
        session.close()

if __name__ == '__main__':
    seed_database()