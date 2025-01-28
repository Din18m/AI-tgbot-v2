"""
Обращения к БД для 'студента'
"""
import psycopg2
from psycopg2 import sql

import config

db_config = {
    'dbname': config.DB_NAME,
    'user': config.DB_USER,
    'password': config.DB_PASSWORD,
    'host': config.DB_HOST,
    'port': config.DB_PORT,
}


def db_connection():
    return psycopg2.connect(**db_config)


async def get_all_info(user_id: int) -> list[dict]:
    """
    Взять всю информацию студента
    :param user_id:
    :return:
    """
    connection = db_connection()
    cursor = connection.cursor()

    try:
        get_all_query = sql.SQL("""
            SELECT * FROM students WHERE id = %s
            """)
        cursor.execute(get_all_query, (user_id,))

        rows = cursor.fetchall()

        user_info = [
            {"id": row[0], "nickname": row[1], "name": row[2], "grade": row[3], "sphere": row[4], "bio": row[5]}
            for row in rows
        ]

        return user_info

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


async def insert_all(user_id: int, name: str, grade: str, sphere: str, bio: str, nickname: str) -> None:
    """
    Добавить в БД характеристику юзера
    :param user_id:
    :param name:
    :param grade:
    :param sphere:
    :param bio:
    :param nickname:
    :return:
    """
    connection = db_connection()
    cursor = connection.cursor()

    try:
        insert_all_query = sql.SQL("""
            insert into students (id, name, grade, sphere, description, nickname) VALUES (%s, %s, %s, %s, %s, %s)
            """)
        cursor.execute(insert_all_query, (user_id, name, grade, sphere, bio, nickname))

        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


async def update_all(user_id:int, name: str, grade: str, sphere: str, bio: str) -> None:
    """
    Обновить характеристику юзера
    :param user_id:
    :param name:
    :param grade:
    :param sphere:
    :param bio:
    :return:
    """
    connection = db_connection()
    cursor = connection.cursor()

    try:
        update_all_query = sql.SQL("""
            UPDATE students
            SET name = %s,
                grade = %s,
                sphere = %s,
                description = %s
            WHERE id = %s
            """)
        cursor.execute(update_all_query, (name, grade, sphere, bio, user_id))

        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()



async def get_all_teachers(id_student: int) -> (list[dict], list):
    """
    Взять всех учителей, у которых show = true
    для обычного поиска
    :param id_student:
    :return:
    """
    connection = db_connection()
    cursor = connection.cursor()
    try:
        get_all_teachers_query = sql.SQL("""
            SELECT name, grade, sphere, description, id, cnt_came, cnt_pass
            FROM teachers
            WHERE show = true
            and id!=%s
            """)
        cursor.execute(get_all_teachers_query, (id_student,))

        rows = cursor.fetchall()

        teachers_info = [
            {"name": row[0], "grade": row[1], "sphere": row[2], "bio": row[3], "id": row[4],
             "cnt_came": row[5], "cnt_pass": row[6]}
            for row in rows
        ]

        get_students_teachers_query = sql.SQL("""
            SELECT id_teacher
            FROM windows
            WHERE id_student=%s
            """)

        cursor.execute(get_students_teachers_query, (id_student,))

        rows = cursor.fetchall()

        sign_up_ids = [
            row[0]
            for row in rows
        ]

        return teachers_info, sign_up_ids

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


all_grades = ["No_work", "Intern", "Junior", "Middle", "Senior"]
all_spheres = ["NLP", "CV", "RecSys", "Audio", "Classic_ML", "Any"]


async def get_filter_teachers(grade:str, sphere:str, id_student:int) -> (list[dict], list):
    """
    Взять всех учителей, у которых show = true и походящими под фильтры
    :param grade:
    :param sphere:
    :param id_student:
    :return:
    """
    connection = db_connection()
    cursor = connection.cursor()

    try:
        get_all_fteachers_query = sql.SQL("""
        SELECT name, grade, sphere, description, id, cnt_came, cnt_pass 
        FROM teachers
        WHERE grade similar to %s and
        sphere similar to %s and
        show = true and
        id!=%s;
        """)

        if (not grade) and sphere:
            cursor.execute(get_all_fteachers_query,
                           ("%(" + "|".join(all_grades) + ")%", "%(" + "|".join(sphere.split(", ")) + ")%", id_student))
        elif (not sphere) and grade:
            cursor.execute(get_all_fteachers_query,
                           ("%(" + "|".join(grade.split(", ")) + ")%", "%(" + "|".join(all_spheres) + ")%", id_student))
        elif (not grade) and (not sphere):
            cursor.execute(get_all_fteachers_query,
                           ("%(" + "|".join(all_grades) + ")%", "%(" + "|".join(all_spheres) + ")%", id_student))
        else:
            cursor.execute(get_all_fteachers_query,
                           ("%(" + "|".join(grade.split(", ")) + ")%", "%(" + "|".join(sphere.split(", ")) + ")%", id_student))
        rows = cursor.fetchall()

        teachers_info = [
            {"name": row[0], "grade": row[1], "sphere": row[2], "bio": row[3], "id": row[4],
             "cnt_came": row[5], "cnt_pass": row[6]}
            for row in rows
        ]

        get_students_teachers_query = sql.SQL("""
                    SELECT id_teacher
                    FROM windows
                    WHERE id_student=%s
                    """)

        cursor.execute(get_students_teachers_query, (id_student,))

        rows = cursor.fetchall()

        sign_up_ids = [
            row[0]
            for row in rows
        ]

        return teachers_info, sign_up_ids

    except (Exception, psycopg2.DatabaseError) as error:
        return error

    finally:
        if connection:
            cursor.close()
            connection.close()


async def get_teacher_by_id(user_id: int) -> list[dict]:
    """
    Взять характеристику учителя
    :param user_id:
    :return:
    """
    connection = db_connection()
    cursor = connection.cursor()
    try:
        get_teacher_by_id_query = sql.SQL("""
            SELECT name, grade, sphere, description, nickname FROM teachers WHERE id = %s
            """)
        cursor.execute(get_teacher_by_id_query, (user_id,))

        rows = cursor.fetchall()

        user_info = [
            {"name": row[0], "grade": row[1], "sphere": row[2], "bio": row[3], "nickname": row[4]}
            for row in rows
        ]

        return user_info

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()



async def check_student_id(user_id: int) -> (list[dict]|str, int):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        # Проверяем наличие пользователя с данным user_id
        check_query = sql.SQL("SELECT EXISTS (SELECT 1 FROM students WHERE id = %s)")
        cursor.execute(check_query, (user_id,))
        exists = cursor.fetchone()[0]
        TMP = sql.SQL("SELECT id, name, grade, sphere, description, nickname from students WHERE id = %s")
        cursor.execute(TMP, (user_id,))
        if exists:
            # Если пользователь существует, извлекаем информацию
            get_all_query = sql.SQL("SELECT id, name, grade, sphere, description, nickname FROM students WHERE id = %s")
            cursor.execute(get_all_query, (user_id,))
            rows = cursor.fetchall()
            user = [
                {"id": row[0], "name": row[1], "grade": row[2], "sphere": row[3], "description": row[4], "nickname": "@" + row[5]}
                for row in rows
            ]
            return user[0], 1
        else:
            user = []
            return user, 0

    except (Exception, psycopg2.DatabaseError) as error:
        return error, -1,
    finally:
        if connection:
            cursor.close()
            connection.close()


async def get_student_windows(id_student: int) -> list[dict]:
    connection = db_connection()
    cursor = connection.cursor()
    try:
        get_student_windows_query = sql.SQL("""
SELECT w.id_teacher,
       w.time,
       w.description,
       t.nickname,
       w.id
FROM windows w
JOIN teachers t
ON w.id_teacher = t.id
WHERE w.id_student = %s
order by w.time;
                """)
        cursor.execute(get_student_windows_query, (id_student,))

        rows = cursor.fetchall()

        student_windows = [
            {"id_teacher": rows[i][0], "time": rows[i][1], "description": rows[i][2], "t_nickname": rows[i][3], "window_id": rows[i][4]}
            for i in range(len(rows))
        ]

        return student_windows

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()



async def cancel_student_window(id_user, id_window: int) -> None|str:
    connection = db_connection()
    cursor = connection.cursor()

    try:
        canceling_window_query = sql.SQL("""
            UPDATE windows SET id_student=null where id=%s;
            """)
        cursor.execute(canceling_window_query, (id_window,))

        cancel_counter_query = sql.SQL("""
                    UPDATE students SET cnt_cancel=cnt_cancel+1 where id=%s;
                    """)
        cursor.execute(cancel_counter_query, (id_user,))

        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


async def get_all_teacher_windows(id_teacher) -> list[dict]:
    connection = db_connection()
    cursor = connection.cursor()

    try:
        get_teacher_windows_query = sql.SQL("""
SELECT time,
       description,
       id
FROM windows 
WHERE (id_teacher=%s) AND (id_student is null )
ORDER BY time;
                """)
        cursor.execute(get_teacher_windows_query, (id_teacher,))

        rows = cursor.fetchall()

        teacher_windows = [
            {"time": row[0], "description": row[1], "id": row[2]}
            for row in rows
        ]

        return teacher_windows

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


async def sign_up_student(id_student, id_teacher, id_window) -> None:
    """
    Реквест на запись к учителю на определенное окно
    :param id_student:
    :param id_teacher:
    :param id_window:
    :return:
    """
    connection = db_connection()
    cursor = connection.cursor()

    try:
        signing_up_query = sql.SQL("""
        INSERT INTO requests (id_student, id_teacher, id_window) VALUES (%s, %s, %s);
        """)

        cursor.execute(signing_up_query, (id_student, id_teacher, id_window))
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()