"""
Миграции
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


def migration_up():
    conn = db_connection()
    cur = conn.cursor()
    try:
        create = sql.SQL("""CREATE TABLE IF NOT EXISTS teachers
(
    id          bigint NOT NULL PRIMARY KEY,
    nickname varchar,
    name        varchar,
    grade       varchar,
    sphere      varchar,
    description varchar,
    show        bool default false,
    cnt_window int default 0,
    cnt_came int default 0,
    cnt_pass int default 0
);

CREATE TABLE IF NOT EXISTS students
(
    id          bigint NOT NULL PRIMARY KEY,
    nickname    varchar,
    name        varchar,
    grade       varchar,
    sphere      varchar,
    description varchar,
    cnt_came int default 0,
    cnt_pass int default 0,
    cnt_cancel int default 0
);

CREATE TABLE IF NOT EXISTS windows
(
    id serial not null primary key,
    id_teacher bigint not null,
    time timestamp,
    description varchar(23),
    id_student bigint default null
);
create table if not exists requests
(
    id serial not null primary key,
    id_window int,
    id_teacher int,
    id_student int
);


        """)

        cur.execute(create)  # Выполняем запрос на создание таблицы
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if conn:
            cur.close()
            conn.close()


def migration_down():
    conn = db_connection()
    cur = conn.cursor()
    try:
        drop = sql.SQL("""DROP TABLE IF EXISTS teachers, students, windows;""")

        cur.execute(drop)  # Выполняем запрос на создание таблицы
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if conn:
            cur.close()
            conn.close()


if __name__ == "__main__":
    migration_down()
    migration_up()
