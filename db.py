"""Database handling."""

import psycopg2
from psycopg2.extras import execute_values
from psycopg2.extras import Json
from psycopg2.extensions import register_adapter

register_adapter(dict, Json)


def insert_ifaces(db_config, ifaces):
    """Insert all provided ifaces to database."""
    conn = psycopg2.connect(**db_config)
    columns = ifaces[0].keys()
    cursor = conn.cursor()
    insert_query = "INSERT INTO interface ({}) VALUES %s".format(",".join(columns))
    values = [[value for value in iface.values()] for iface in ifaces]
    execute_values(cursor, insert_query, values)
    conn.commit()
