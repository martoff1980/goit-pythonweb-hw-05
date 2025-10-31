from my_select import *

def test_all_queries():
    print("ТЕСТИРОВАННЯ ЗАПРОСІВ\n")
    
    # 1.  5 студентів із найбільшим середнім балом з усіх предметів
    print("1.  5 студентів із найбільшим середнім балом з усіх предметів:")
    result = select_1()
    for student, avg_grade in result:
        print(f"   {student}: {avg_grade:.2f}")
    print()
    
    # 2. Студент із найвищим середнім балом з математики
    print("2. Студент із найвищим середнім балом з математики:")
    result = select_2("Mathematics")
    if result:
        student, avg_grade = result
        print(f"   {student}: {avg_grade:.2f}")
    print()
    
    # 3. Середній бал в групах з математики
    print("3. Середній бал в групах з математики:")
    result = select_3("Mathematics")
    for group_name, avg_grade in result:
        print(f"   {group_name}: {avg_grade:.2f}")
    print()
    
    # 4. Средній бал на потоці
    print("4. Средній бал на потоці:")
    result = select_4()
    print(f"   {result}")
    print()
    
    # 5. Курси преподавателя
    print("5. Курси преподавателя (першого в базі):")
    # Спочатку йде ім'я першого преподавателя
    from my_select import get_session
    session = get_session()
    first_teacher = session.query(Teacher).first()
    if first_teacher:
        result = select_5(first_teacher.name)
        for subject in result:
            print(f"   {subject}")
    session.close()
    print()
    
    # 6. Студенти в групі
    print("6. Студенти в групі 'Group 1':")
    result = select_6("Group 1")
    for student in result[:5]:  # Вивід тільки перших 5
        print(f"   {student}")
    print(f"   ... потім ще {len(result) - 5} студентів")
    print()
    
    # 7. Оцінки студентів в групі з предмету
    print("7. Оцінки студентів в групі 'Group 1' з математики:")
    result = select_7("Group 1", "Mathematics")
    for student, grade, date in result[:5]:  # Вивід тільки перших 5
        print(f"   {student}: {grade} ({date})")
    print()
    
    # 8. Середній бал преподавателя
    print("8. Средній бал преподавателя (першого в базі):")
    if first_teacher:
        result = select_8(first_teacher.name)
        print(f"   {result}")
    print()
    
    # 9. Курси студента
    print("9. Курси студента (першого в базе):")
    first_student = session.query(Student).first()
    if first_student:
        result = select_9(first_student.name)
        for subject in result:
            print(f"   {subject}")
    print()
    
    # 10. Курси студента у преподавателя
    print("10. Курси студента у преподавателя:")
    if first_student and first_teacher:
        result = select_10(first_student.name, first_teacher.name)
        for subject in result:
            print(f"   {subject}")
    print()
    
    # 11. Середній бал преподавателя студенту
    print("11. Середній бал преподавателя студенту:")
    if first_student and first_teacher:
        result = select_11(first_teacher.name, first_student.name)
        print(f"   {result}")
    print()
    
    # 12. Оцінки на останнем занятті
    print("12. Оцінки в групе 'Group 1' з математики на останнем занятті:")
    result = select_12("Group 1", "Mathematics")
    for student, grade in result:
        print(f"   {student}: {grade}")
    print()

if __name__ == "__main__":
    test_all_queries()