import psycopg2


def create_db(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS student(
                      id SERIAL PRIMARY KEY,
                      name VARCHAR(100) NOT NULL,
                      gpa DECIMAL(10, 2),
                      birth TIMESTAMP WITH TIME ZONE
                      );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS course(
                      id SERIAL PRIMARY KEY,
                      name VARCHAR(100) NOT NULL
                      );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS studying(
                      student_id INT REFERENCES student(id),
                      course_id INT REFERENCES course(id),
                      CONSTRAINT student_course_pk PRIMARY KEY(student_id, course_id)
                      );''')


def get_students(cursor, course_id): # возвращает студентов определенного курса
    cursor.execute('''SELECT B.name, B.gpa, B.birth
                      FROM studying A
                      JOIN student B ON A.student_id = B.id
                      WHERE A.course_id = %s;
                      ''', (course_id, ))
    return cursor.fetchall()


def add_students(connection, cursor, course_id, students): # создает студентов и
                                       # записывает их на курс
    try:
        for student in students:
            add_student(cursor, **student)
            cursor.execute('''SELECT id
                              FROM student
                              WHERE student.name = %s;
                              ''', (student['name'], ))
            student_id = cursor.fetchone()
            add_student_to_course(cur, student_id, course_id)
        connection.commit()
        print('Successful commit')
    except Exception:
        connection.rollback()
        print('Commit was canceled. Error were caught.')


def add_student(cursor, **student): # просто создает студента
    cursor.execute('''INSERT INTO student (name, gpa, birth) VALUES(
                      %s, %s, %s
                      );''', (student['name'], student['gpa'], student['birth']))


def add_student_to_course(cursor, student_id, course_id):
    cursor.execute('''INSERT INTO studying VALUES (%s, %s)''', (student_id, course_id))


def get_student(cursor, student_id):
    cursor.execute('''SELECT name, gpa, birth
                      FROM student
                      WHERE student.id = %s;
                      ''', (student_id, ))
    return cursor.fetchone()


def add_course(cursor, course_name): # просто создает студента
    cursor.execute('''INSERT INTO course (name) VALUES(
                      %s );''', (course_name, ))


if __name__ == '__main__':
    with psycopg2.connect(database='test', user='test', password='test',
                          host='localhost', port=5432) as conn:
        cur = conn.cursor()

        print('Creating tables...')
        create_db(cur)

        print('Adding student...')
        student = dict(name='Mr Smith', gpa=7, birth='01-01-1989')
        add_student(cur, **student)

        print('Checking if student inserted correct...')
        print(get_student(cur, 1))

        print('Adding course...')
        add_course(cur, "PostgreSQL")

        print('Adding student to course...')
        students = (dict(name='Mike', gpa=7, birth='05-07-1999'),
                    dict(name='John', gpa=3, birth='01-11-1996'),
                    dict(name='Kate', gpa=8, birth='30-04-1996'))
        add_students(conn, cur, 1, students)

        print('Checking if studying group inserted correct...')
        students = get_students(cur, 1)
        for student in students:
            print(student)

        print('Well done!')
