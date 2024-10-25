from clickhouse_driver import Client
import os

class ClickHouseClient:
    def __init__(self):
        self.host = os.getenv("CLICKHOUSE_HOST")
        self.user = os.getenv("CLICKHOUSE_USER")
        self.password = os.getenv("CLICKHOUSE_PASSWD")
        self.client = Client(host=self.host, user=self.user, password=self.password)

    def insert_data(self, table_name, data):
        """
        Insert data into the specified ClickHouse table.
        
        :param table_name: Name of the table where data will be inserted.
        :param data: List of tuples, where each tuple represents a row of data.
        """
        query = f"INSERT INTO {table_name} VALUES"
        self.client.execute(query, data)

    def query_data(self, query):
        """
        Query data from ClickHouse.
        
        :param query: SQL query string.
        :return: Query result.
        """
        result = self.client.execute(query)
        return result

