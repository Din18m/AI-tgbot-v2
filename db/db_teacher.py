from datetime import datetime, timedelta


import psycopg2
from psycopg2 import sql

import config
import teacher.model
from config import schedule
from teacher import notify

db_config = {
    'dbname': config.DB_NAME,
    'user': config.DB_USER,
    'password': config.DB_PASSWORD,
    'host': config.DB_HOST,
    'port': config.DB_PORT,
}


def db_connection():
    return psycopg2.connect(**db_config)


def check_id(user_id: int) -> (teacher.model.Teacher, int):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        # Проверяем наличие пользователя с данным user_id
        check_query = sql.SQL("SELECT EXISTS (SELECT 1 FROM teachers WHERE id = %s)")
        cursor.execute(check_query, (user_id,))
        exists = cursor.fetchone()[0]
        if exists:
            # Если пользователь существует, извлекаем информацию
            get_all_query = sql.SQL("SELECT id, name, grade, sphere, description, nickname FROM teachers WHERE id = %s")
            cursor.execute(get_all_query, (user_id,))
            rows = cursor.fetchone()
            user = teacher.model.Teacher(
                id=rows[0],
                name=rows[1],
                grade=rows[2],
                sphere=rows[3],
                description=rows[4],
                nickname=rows[5],
            )
            return user, 1
        else:
            user = teacher.model.Teacher
            user.id = user_id
            return user, 0

    except (Exception, psycopg2.DatabaseError) as error:
        return error, -1,
    finally:
        if connection:
            cursor.close()
            connection.close()


def add_user(usr: teacher.model.Teacher):
    connection = db_connection()
    cursor = connection.cursor()

    try:
        user, i = check_id(usr.id)

        if i == 1:  # Пользователь уже существует
            # Обновляем данные пользователя
            update_query = sql.SQL("""
                UPDATE teachers 
                SET  name = %s, grade = %s, sphere = %s, description = %s, nickname = %s
                WHERE id = %s
            """)
            cursor.execute(update_query, (
                usr.name,
                usr.grade,
                usr.sphere,
                usr.description,
                usr.nickname,
                usr.id,
            ))
            cursor.connection.commit()
        elif i == 0:  # Пользователь новый
            # Добавляем нового пользователя
            insert_query = sql.SQL("""
                INSERT INTO teachers (id, name, grade, sphere, description, nickname)
                VALUES (%s, %s, %s, %s, %s, %s)
            """)
            cursor.execute(insert_query, (
                usr.id,
                usr.name,
                usr.grade,
                usr.sphere,
                usr.description,
                usr.nickname
            ))

        else:  # Произошла ошибка при проверке ID
            return False

        connection.commit()
        return True

    except (Exception, psycopg2.DatabaseError) as error:
        return False

    finally:
        if connection:
            cursor.close()
            connection.close()


def change_show(user_id: int, show: bool):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        update_query = sql.SQL("""
                UPDATE teachers
                SET show = %s
                WHERE id = %s
            """)
        cursor.execute(update_query, (
            show, user_id
        ))
        cursor.connection.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        return False

    finally:
        if connection:
            cursor.close()
            connection.close()


def get_cnt_windows(teacher_id: int):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        window = sql.SQL("""
            SELECT cnt_window FROM teachers WHERE id = %s
            """)
        cursor.execute(window, (teacher_id,))
        row = cursor.fetchone()
        cnt_wind = row[0]

        return cnt_wind

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


def get_free_cnt_windows(id_teacher: int):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        window = sql.SQL("""SELECT COUNT(*) FROM windows WHERE id_teacher = %s AND id_student IS NULL;""")
        cursor.execute(window, (id_teacher,))

        cnt = cursor.fetchone()[0]

        return cnt

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


def add_new_window(id_teacher: int, time: datetime, description: str):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        insert_query = sql.SQL("""
                        INSERT INTO windows (id_teacher, time, description) VALUES (%s, %s, %s); 
                    """)
        cursor.execute(insert_query, (
            id_teacher, time, description
        ))
        cnt_wind = get_cnt_windows(id_teacher)
        update_query = sql.SQL("""
                            UPDATE teachers
                            SET cnt_window = %s, show = true
                            WHERE id = %s
                        """)
        cursor.execute(update_query, (
            cnt_wind + 1, id_teacher
        ))
        cursor.connection.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        return False

    finally:
        if connection:
            cursor.close()
            connection.close()


def get_free_window(id_teacher: int):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        window = sql.SQL("""
            SELECT time, description, id FROM windows WHERE id_teacher = %s and id_student IS NULL
            """)
        cursor.execute(window, (id_teacher,))

        rows = cursor.fetchall()

        window = [{"time": row[0], "description": row[1], "id": row[2]} for row in rows]

        return window

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


def get_all_window(id_teacher: int):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        window = sql.SQL("""
            SELECT time, description, id, id_student FROM windows WHERE id_teacher = %s
            """)
        cursor.execute(window, (id_teacher,))

        rows = cursor.fetchall()

        window = [{"time": row[0], "description": row[1], "id": row[2], "student": row[3]} for row in rows]

        return window

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


async def delete_window(id: int):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        window_query = sql.SQL("""
                               SELECT id, time, description, id_student, id_teacher FROM windows WHERE id = %s
                               """)
        cursor.execute(window_query, (id,))

        row = cursor.fetchone()

        window = {"id": row[0], "time": row[1], "description": row[2], "student": row[3]}

        id_teacher = row[4]

        insert_query = sql.SQL("""delete FROM windows WHERE id = %s """)
        cursor.execute(insert_query, (id,))
        window_query = sql.SQL("""
                    SELECT id_student FROM requests WHERE id_window = %s
                    """)
        cursor.execute(window_query, (id,))
        rows = cursor.fetchall()
        for row in rows:
            await notify.dislike(row[0], id_teacher, window)

        id_teacher = cursor.fetchone()[0]
        delete_query = sql.SQL("""DELETE from requests WHERE id_window = %s""")
        cursor.execute(delete_query, (id,))
        cnt_wind = get_cnt_windows(id_teacher)
        if cnt_wind == 1:
            update_query = sql.SQL("""
                                    UPDATE teachers
                                    SET cnt_window = %s, show = false
                                    WHERE id = %s
                                """)
        else:
            update_query = sql.SQL("""
                                    UPDATE teachers
                                    SET cnt_window = %s, show = true
                                    WHERE id = %s
                                """)

        cursor.execute(update_query, (
            cnt_wind - 1, id_teacher
        ))
        cursor.connection.commit()
        return True

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


async def get_requests(id_teacher: int):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        request = sql.SQL("""
            SELECT id, id_window, id_student FROM requests WHERE id_teacher = %s
            """)
        cursor.execute(request, (id_teacher,))

        rows = cursor.fetchall()

        request = [{"id": row[0], "window": row[1], "student": row[2]} for row in rows]
        free_request = []
        for elem in request:
            window = sql.SQL("""
                       SELECT id, time, description, id_student FROM windows WHERE id = %s
                       """)
            cursor.execute(window, (elem["window"],))

            row = cursor.fetchone()

            window = {"id": row[0], "time": row[1], "description": row[2], "student": row[3]}
            elem["window"] = window
            if window["student"] is not None and window["student"] != elem["student"]:
                await notify.dislike(elem["student"], id_teacher, window)
                continue
            if window["student"] == elem["student"]:
                continue
            elem["window"] = window
            student = sql.SQL("""
                SELECT id, nickname, name, grade, sphere, description, cnt_came, cnt_pass, cnt_cancel FROM students WHERE id = %s
                """)
            cursor.execute(student, (elem["student"],))
            row = cursor.fetchone()
            student = {"id": row[0], "nickname": row[1], "name": row[2], "grade": row[3], "sphere": row[4],
                       "description": row[5], "cnt_came": row[6], "cnt_pass": row[7], "cnt_cancel": row[8]}
            elem["student"] = student
            free_request.append(elem)

        return free_request

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


def check_exist_request(id: int) -> bool:
    connection = db_connection()
    cursor = connection.cursor()
    try:
        window = sql.SQL("""
                SELECT EXISTS (
  SELECT 1 
  FROM requests 
  WHERE id = %s
);
""")
        cursor.execute(window, (id,))
        row = cursor.fetchone()
        return row[0]

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


async def delete_one_dislike_requests(id_request: int):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        window_query = sql.SQL("""
                        SELECT id_student, id_window FROM requests WHERE id = %s
                        """)
        cursor.execute(window_query, (id_request,))
        row = cursor.fetchone()
        id_student = row[0]
        id_window = row[1]
        window_query = sql.SQL("""
                                   SELECT id, time, description, id_student, id_teacher FROM windows WHERE id = %s
                                   """)
        cursor.execute(window_query, (id_window,))

        row = cursor.fetchone()

        window = {"id": row[0], "time": row[1], "description": row[2], "student": row[3]}

        id_teacher = row[4]

        await notify.dislike(id_student, id_teacher, window)
        delete_query = sql.SQL("""DELETE from requests WHERE id = %s""")
        cursor.execute(delete_query, (id_request,))
        cursor.connection.commit()
        return True

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


async def delete_all_window_requests(id_window: int):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        window_query = sql.SQL("""
                                   SELECT id, time, description, id_student, id_teacher FROM windows WHERE id = %s
                                   """)
        cursor.execute(window_query, (id_window,))

        row = cursor.fetchone()

        window = {"id": row[0], "time": row[1], "description": row[2], "student": row[3]}

        id_teacher = row[4]
        window_query = sql.SQL("""
                        SELECT id_student FROM requests WHERE id_window = %s
                        """)
        cursor.execute(window_query, (id_window,))
        rows = cursor.fetchall()
        for row in rows:
            await notify.dislike(row[0], id_teacher, window)
        delete_query = sql.SQL("""DELETE from requests WHERE id_window = %s""")
        cursor.execute(delete_query, (id_window,))
        cnt_wind = get_cnt_windows(id_teacher)
        if cnt_wind == 1:
            update_query = sql.SQL("""
                                        UPDATE teachers
                                        SET cnt_window = %s, show = false
                                        WHERE id = %s
                                    """)
        else:
            update_query = sql.SQL("""
                                        UPDATE teachers
                                        SET cnt_window = %s, show = true
                                        WHERE id = %s
                                    """)
        cursor.execute(update_query, (
            cnt_wind - 1, id_teacher
        ))
        cursor.connection.commit()
        return True

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


async def like_requests(id_request: int):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        window_query = sql.SQL("""
                            SELECT id_student, id_window, id_teacher FROM requests WHERE id = %s
                            """)
        cursor.execute(window_query, (id_request,))
        row = cursor.fetchone()
        id_student = row[0]
        id_window = row[1]
        id_teacher = row[2]
        window_query = sql.SQL("""
                                    SELECT nickname FROM students WHERE id = %s
                                    """)
        cursor.execute(window_query, (id_student,))
        row = cursor.fetchone()
        nickname_student = row[0]
        window_query = sql.SQL("""
                                            SELECT nickname FROM teachers WHERE id = %s
                                            """)
        cursor.execute(window_query, (id_teacher,))
        row = cursor.fetchone()
        nickname_teacher = row[0]
        window_query = sql.SQL("""
                                       SELECT id, time, description, id_student, id_teacher FROM windows WHERE id = %s
                                       """)
        cursor.execute(window_query, (id_window,))

        row = cursor.fetchone()

        window = {"id": row[0], "time": row[1], "description": row[2], "student": row[3]}

        id_teacher = row[4]

        await notify.like(id_student, id_teacher, window)
        delete_query = sql.SQL("""DELETE from requests WHERE id = %s""")
        cursor.execute(delete_query, (id_request,))

        update_query = sql.SQL("""
                                            UPDATE windows
                                            SET id_student = %s
                                            WHERE id = %s
                                        """)
        cursor.execute(update_query, (id_student, id_window,))
        if get_free_cnt_windows(id_teacher) == 0:
            update_query = sql.SQL("""
                                                UPDATE teachers
                                                SET show = false
                                                WHERE id = %s
                                            """)
            cursor.execute(update_query, (id_teacher,))

        cursor.connection.commit()
        return True

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


def delete_time_student_requests(id_student: int, id_window: int):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        window_query = sql.SQL("""
                            SELECT time FROM windows WHERE id = %s
                            """)
        cursor.execute(window_query, (id_window,))
        row = cursor.fetchone()
        time = row[0]
        delta = timedelta(minutes=30)
        t1 = time - delta
        t2 = time + delta
        requests_query = sql.SQL("""
                                       SELECT id, id_window FROM requests WHERE id_student = %s
                                       """)
        cursor.execute(requests_query, (id_student,))

        rows = cursor.fetchall()

        windows = [{"id_request": row[0], "id_window": row[1]} for row in rows]
        for window in windows:
            window_query = sql.SQL("""
                                        SELECT time FROM windows WHERE id = %s
                                        """)
            cursor.execute(window_query, (window["id_window"],))
            row = cursor.fetchone()
            time = row[0]
            if t1 <= time <= t2:
                delete_query = sql.SQL("""DELETE from requests WHERE id = %s""")
                cursor.execute(delete_query, (window["id_request"],))
        cursor.connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


def get_all_requests():
    connection = db_connection()
    cursor = connection.cursor()
    try:
        request = sql.SQL("""
               SELECT id_teacher, COUNT(*) as total
                    FROM requests
                    GROUP BY id_teacher
               """)
        cursor.execute(request)

        rows = cursor.fetchall()

        request = [{"id_teacher": row[0], "cnt": row[1]} for row in rows]

        return request

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


def delete_windows_expired():
    connection = db_connection()
    cursor = connection.cursor()
    try:
        request = sql.SQL("""
                   DELETE FROM windows 
WHERE 
    time AT TIME ZONE 'Europe/Moscow' <  -- Конвертируем хранимое время в тип с зоной
    (NOW() AT TIME ZONE 'Europe/Moscow');
                   """)
        cursor.execute(request)

        cursor.connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()
