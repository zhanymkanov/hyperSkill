from typing import List, Generator

from clickhouse_driver import Client

DEFAULT_TABLE_NAME = "analytics.facts_events"


class Clickhouse:
    def __init__(self, table_name=DEFAULT_TABLE_NAME):
        self.client = Client(host="clickhouse")
        self.table_name = table_name

        self._init_tables()

    def _init_tables(self):
        create_query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name}
        (
            time              DateTime,
            user_id           UInt64,
            join_date         Date,
            registration_date Date NULL,
            name              String,
            email             String,
            is_guest          UInt8,
            step_id           UInt64,
            action_id         UInt8
        ) ENGINE MergeTree()
            PARTITION BY toYYYYMM(time)
            ORDER BY (time, user_id, step_id)
            SETTINGS index_granularity = 8192;
        """

        self.client.execute(create_query)

    def insert_data(self, records):
        insert_query = f"""
        INSERT INTO {self.table_name} 
        (
            time,
            user_id,
            join_date,
            registration_date,
            name,
            email,
            is_guest,
            step_id,
            action_id
        )
        VALUES 
        """
        self.client.execute(insert_query, records)
