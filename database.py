import sqlite3 as sql

from config import DB_NAME


async def create_db() -> None:
    with sql.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
      CREATE TABLE users (
        id      INTEGER PRIMARY KEY,
        chat_id INTEGER NOT NULL UNIQUE
      )"""
        )

        cursor.execute(
            """
      CREATE TABLE intervals (
        id   INTEGER PRIMARY KEY,
        name TEXT    NOT NULL UNIQUE
      )"""
        )

        cursor.execute(
            """
      CREATE TABLE tracking_pairs (
        id              INTEGER PRIMARY KEY,
        user_id         INTEGER NOT NULL,
        pair_name       TEXT    NOT NULL,
        exchange_name   TEXT    NOT NULL,
        growth_rate     REAL    NOT NULL DEFAULT 8,
        correction_rate REAL    NOT NULL DEFAULT 5,
        candle_count    INTEGER NOT NULL DEFAULT 20,
        interval_id     INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (user_id)     REFERENCES users(id)     ON DELETE CASCADE,
        FOREIGN KEY (interval_id) REFERENCES intervals(id) ON DELETE RESTRICT
      )"""
        )
        connection.commit()


async def get_intervals() -> list[sql.Row]:
    with sql.connect(DB_NAME) as connection:
        connection.row_factory = sql.Row
        cursor = connection.cursor()
        cursor.execute(
            """
      SELECT id, name 
        FROM intervals
    """
        )
        result = cursor.fetchall()
        return result


async def get_user_pair(pair_id: str) -> sql.Row:
    with sql.connect(DB_NAME) as connection:
        connection.row_factory = sql.Row
        cursor = connection.cursor()
        cursor.execute(
            f"""
      SELECT t.*, 
             u.chat_id, 
             i.name AS interval_name
        FROM tracking_pairs AS t 
            JOIN intervals AS i 
            ON i.id = t.interval_id

            JOIN users AS u 
            ON u.id = t.user_id
      WHERE t.id = {pair_id}
    """
        )
        result = cursor.fetchone()
        return result


async def get_user_pairs(chat_id: str) -> list[sql.Row]:
    with sql.connect(DB_NAME) as connection:
        connection.row_factory = sql.Row
        cursor = connection.cursor()
        cursor.execute(
            f"""
      SELECT t.id, t.pair_name, t.exchange_name
        FROM tracking_pairs AS t 
              JOIN users AS u 
              ON u.id = t.user_id
        WHERE u.chat_id = {chat_id}
    """
        )
        user_pairs = cursor.fetchall()
        return user_pairs


async def get_all_pairs() -> list[sql.Row]:
    with sql.connect(DB_NAME) as connection:
        connection.row_factory = sql.Row
        cursor = connection.cursor()
        cursor.execute(
            f"""
      SELECT t.*, 
             u.chat_id, 
             i.name AS interval_name
        FROM tracking_pairs AS t 
             JOIN intervals AS i 
             ON i.id = t.interval_id

             JOIN users AS u 
             ON u.id = t.user_id
    """
        )
        result = cursor.fetchall()
        return result


async def get_user(chat_id: str) -> sql.Row:
    with sql.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
      SELECT chat_id 
        FROM users
        WHERE chat_id = {chat_id}
    """
        )
        result = cursor.fetchone()
        return result


async def add_user(chat_id: str) -> None:
    with sql.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
      INSERT INTO users (chat_id)
      VALUES ({chat_id})
    """
        )
        connection.commit()


async def add_tracking_pair(chat_id: str, pair_name: str, exchange_name: str) -> None:
    with sql.connect(DB_NAME) as connection:
        connection.row_factory = sql.Row
        cursor = connection.cursor()
        cursor.execute(
            f"""
      SELECT id 
        FROM users
      WHERE chat_id = {chat_id}
    """
        )
        user_id = cursor.fetchone()["id"]
        cursor.execute(
            f"""
      INSERT INTO tracking_pairs (user_id, pair_name, exchange_name)
      VALUES({user_id}, "{pair_name}", "{exchange_name}")
    """
        )
        connection.commit()


async def update_growth_rate(pair_id: str, new_value: float) -> None:
    with sql.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
      UPDATE tracking_pairs
        SET growth_rate = "{new_value}"
      WHERE id = {pair_id}
    """
        )
        connection.commit()


async def update_correction_rate(pair_id: str, new_value: float) -> None:
    with sql.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
      UPDATE tracking_pairs
        SET correction_rate = "{new_value}"
      WHERE id = {pair_id}
    """
        )
        connection.commit()


async def update_candle_count(pair_id: str, new_value: int) -> None:
    with sql.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
      UPDATE tracking_pairs
        SET candle_count = "{new_value}"
      WHERE id = {pair_id}
    """
        )
        connection.commit()


async def update_interval(pair_id: str, new_value: int) -> None:
    with sql.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
      UPDATE tracking_pairs
        SET interval_id = "{new_value}"
      WHERE id = {pair_id}
    """
        )
        connection.commit()


async def delete_pair(pair_id: str) -> None:
    with sql.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
      DELETE FROM tracking_pairs
        WHERE id = {pair_id}
    """
        )
        connection.commit()


async def delete_user(user_id: str) -> None:
    with sql.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
      DELETE FROM users
        WHERE id = {user_id}
    """
        )
        connection.commit()


async def count_user_pairs(chat_id: str) -> None:
    with sql.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
      SELECT COUNT(u.chat_id), 
             u.chat_id
        FROM tracking_pairs AS t 
             JOIN users AS u 
             ON u.id = t.user_id
             WHERE u.chat_id = {chat_id}
    """
        )
        result = cursor.fetchone()
        return result
