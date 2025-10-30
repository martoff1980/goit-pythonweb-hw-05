import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models import Base, Group, Student, Teacher, Subject, Grade
from datetime import datetime

# Database setup
def get_session():
    engine = create_engine('postgresql://postgres:1234@localhost:5432/postgres')
    Session = sessionmaker(bind=engine)
    return Session()

def create_model(model, **kwargs):
    session = get_session()
    try:
        if model == 'Group':
            obj = Group(name=kwargs.get('name'))
        elif model == 'Student':
            obj = Student(name=kwargs.get('name'), group_id=kwargs.get('group_id'))
        elif model == 'Teacher':
            obj = Teacher(name=kwargs.get('name'))
        elif model == 'Subject':
            obj = Subject(name=kwargs.get('name'), teacher_id=kwargs.get('teacher_id'))
        elif model == 'Grade':
            # Parse date if provided
            date_received = kwargs.get('date_received')
            if date_received and isinstance(date_received, str):
                date_received = datetime.strptime(date_received, '%Y-%m-%d').date()
            elif not date_received:
                date_received = datetime.now().date()
                
            obj = Grade(
                grade=kwargs.get('grade'),
                date_received=date_received,
                student_id=kwargs.get('student_id'),
                subject_id=kwargs.get('subject_id')
            )
        else:
            print(f"Unknown model: {model}")
            return
        
        session.add(obj)
        session.commit()
        print(f"✓ Created {model}: {obj}")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"✗ Error creating {model}: {e}")
    except Exception as e:
        session.rollback()
        print(f"✗ Unexpected error: {e}")
    finally:
        session.close()

def list_model(model):
    session = get_session()
    try:
        if model == 'Group':
            objects = session.query(Group).all()
            print(f"\n--- {len(objects)} Groups ---")
            for obj in objects:
                print(f"ID: {obj.id}, Name: {obj.name}")
        elif model == 'Student':
            objects = session.query(Student).all()
            print(f"\n--- {len(objects)} Students ---")
            for obj in objects:
                print(f"ID: {obj.id}, Name: {obj.name}, Group ID: {obj.group_id}")
        elif model == 'Teacher':
            objects = session.query(Teacher).all()
            print(f"\n--- {len(objects)} Teachers ---")
            for obj in objects:
                print(f"ID: {obj.id}, Name: {obj.name}")
        elif model == 'Subject':
            objects = session.query(Subject).all()
            print(f"\n--- {len(objects)} Subjects ---")
            for obj in objects:
                print(f"ID: {obj.id}, Name: {obj.name}, Teacher ID: {obj.teacher_id}")
        elif model == 'Grade':
            objects = session.query(Grade).all()
            print(f"\n--- {len(objects)} Grades ---")
            for obj in objects:
                print(f"ID: {obj.id}, Student: {obj.student_id}, Subject: {obj.subject_id}, Grade: {obj.grade}, Date: {obj.date_received}")
        else:
            print(f"Unknown model: {model}")
    except Exception as e:
        print(f"Error listing {model}: {e}")
    finally:
        session.close()

def update_model(model, id, **kwargs):
    session = get_session()
    try:
        if model == 'Group':
            obj = session.query(Group).filter_by(id=id).first()
            if obj and 'name' in kwargs:
                obj.name = kwargs['name']
        elif model == 'Student':
            obj = session.query(Student).filter_by(id=id).first()
            if obj:
                if 'name' in kwargs:
                    obj.name = kwargs['name']
                if 'group_id' in kwargs:
                    obj.group_id = kwargs['group_id']
        elif model == 'Teacher':
            obj = session.query(Teacher).filter_by(id=id).first()
            if obj and 'name' in kwargs:
                obj.name = kwargs['name']
        elif model == 'Subject':
            obj = session.query(Subject).filter_by(id=id).first()
            if obj:
                if 'name' in kwargs:
                    obj.name = kwargs['name']
                if 'teacher_id' in kwargs:
                    obj.teacher_id = kwargs['teacher_id']
        elif model == 'Grade':
            obj = session.query(Grade).filter_by(id=id).first()
            if obj:
                if 'grade' in kwargs:
                    obj.grade = kwargs['grade']
                if 'date_received' in kwargs:
                    date_received = kwargs['date_received']
                    if isinstance(date_received, str):
                        date_received = datetime.strptime(date_received, '%Y-%m-%d').date()
                    obj.date_received = date_received
                if 'student_id' in kwargs:
                    obj.student_id = kwargs['student_id']
                if 'subject_id' in kwargs:
                    obj.subject_id = kwargs['subject_id']
        else:
            print(f"Unknown model: {model}")
            return
        
        if obj:
            session.commit()
            print(f"✓ Updated {model} with ID: {id}")
        else:
            print(f"✗ {model} with ID {id} not found")
    except Exception as e:
        session.rollback()
        print(f"✗ Error updating {model}: {e}")
    finally:
        session.close()

def remove_model(model, id):
    session = get_session()
    try:
        if model == 'Group':
            obj = session.query(Group).filter_by(id=id).first()
        elif model == 'Student':
            obj = session.query(Student).filter_by(id=id).first()
        elif model == 'Teacher':
            obj = session.query(Teacher).filter_by(id=id).first()
        elif model == 'Subject':
            obj = session.query(Subject).filter_by(id=id).first()
        elif model == 'Grade':
            obj = session.query(Grade).filter_by(id=id).first()
        else:
            print(f"Unknown model: {model}")
            return
        
        if obj:
            session.delete(obj)
            session.commit()
            print(f"✓ Removed {model} with ID: {id}")
        else:
            print(f"✗ {model} with ID {id} not found")
    except Exception as e:
        session.rollback()
        print(f"✗ Error removing {model}: {e}")
    finally:
        session.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Database CRUD Operations')
    parser.add_argument('-a', '--action', required=True, choices=['create', 'list', 'update', 'remove'], help='CRUD action')
    parser.add_argument('-m', '--model', required=True, choices=['Group', 'Student', 'Teacher', 'Subject', 'Grade'], help='Model name')
    parser.add_argument('--id', type=int, help='ID for update/remove operations')
    parser.add_argument('-n', '--name', help='Name for create/update operations')
    parser.add_argument('--group_id', type=int, help='Group ID for Student')
    parser.add_argument('--teacher_id', type=int, help='Teacher ID for Subject')
    parser.add_argument('--student_id', type=int, help='Student ID for Grade')
    parser.add_argument('--subject_id', type=int, help='Subject ID for Grade')
    parser.add_argument('--grade', type=int, help='Grade value')
    parser.add_argument('--date_received', help='Date received for Grade (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    kwargs = {k: v for k, v in vars(args).items() if v is not None and k not in ['action', 'model', 'id']}
    
    if args.action == 'create':
        create_model(args.model, **kwargs)
    elif args.action == 'list':
        list_model(args.model)
    elif args.action == 'update':
        if not args.id:
            print("✗ Error: --id is required for update operation")
        else:
            update_model(args.model, args.id, **kwargs)
    elif args.action == 'remove':
        if not args.id:
            print("✗ Error: --id is required for remove operation")
        else:
            remove_model(args.model, args.id)