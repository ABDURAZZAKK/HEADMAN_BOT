import os
from typing import Dict, List, Tuple

import sqlite3

conn = sqlite3.connect(os.path.join("db", "df.db"))
conn.execute("PRAGMA foreign_keys = 1")
cursor = conn.cursor()




def insert(table: str, column_values: Dict):
    columns = ", ".join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ', '.join( '?' * len(column_values.keys()))  
    cursor.executemany(
        f"INSERT INTO {table}"
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def update_schedule(table: str, key, val, whom: int):
    cursor.execute(
        f"""UPDATE {table}
        SET {key} = '{val}'
        WHERE id LIKE {whom}"""
        )
    conn.commit()

def update_active_group(table: str,  whom: int, column_values: Dict):
    columns = "".join(column_values.keys())
    values = [tuple(column_values.values())]
    cursor.executemany(
        f"""UPDATE {table}
        SET {columns} = ?
        WHERE id LIKE {whom}"""
        ,values)
    conn.commit()
    

def delete_many_to_many(table: str, whom: int, group_name: str) -> None:
    whom = int(whom)
    cursor.execute(f"""delete from {table} where member_id={whom} and 
                    group_name='{group_name}' """)
    conn.commit()


def delete(table: str, row_id: int) -> None:
    row_id = int(row_id)
    cursor.execute(f"delete from {table} where id={row_id}")
    conn.commit()


def get_cursor():
    return cursor


def _init_db():
    """Инициализирует БД"""
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()
    

def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='groups'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()

check_db_exists()
