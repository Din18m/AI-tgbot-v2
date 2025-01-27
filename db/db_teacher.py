from datetime import datetime

import psycopg2
from psycopg2 import sql

import config
import teacher.model

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

        window = [{"time": row[0], "description": row[1], "id": row[2], "student":row[3]} for row in rows]

        return window

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


def delete_window(id: int):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        window = sql.SQL("""
            SELECT id_teacher FROM windows WHERE id = %s
            """)
        cursor.execute(window, (id,))

        id_teacher = cursor.fetchone()[0]

        insert_query = sql.SQL("""delete FROM windows WHERE id = %s """)
        cursor.execute(insert_query, (id,))
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
