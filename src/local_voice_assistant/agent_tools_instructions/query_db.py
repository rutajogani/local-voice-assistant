import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "appdb",
    "user": "postgres",
    "password": "postgres",
}


def run_query(sql, params=None):
    """Run a SELECT query and return rows as a list of dicts."""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory = RealDictCursor) as cur:
            cur.execute(sql, params)
            return cur.fetchall()


def run_command(sql, params=None):
    """Run INSERT/UPDATE/DELETE/DDL. The connection context manager commits on success."""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.rowcount

def get_table_schema(table_name, schema="public"):
    """Return column info (name, type, nullable, default) for a table."""
    sql = """
        SELECT
            column_name,
            data_type,
            is_nullable,
            column_default
        FROM information_schema.columns
        WHERE table_schema = %s
          AND table_name = %s
        ORDER BY ordinal_position
    """
    return run_query(sql, (schema, table_name))


def list_tables(schema="public"):
    """Return the names of all tables in a schema."""
    sql = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s
          AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """
    return [row["table_name"] for row in run_query(sql, (schema,))]

if __name__ == "__main__":
    tables = run_query("SELECT * FROM users")
    for t in tables:
        print(t["username"])