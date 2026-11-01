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
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            return cur.fetchall()


def run_command(sql, params=None):
    """Run INSERT/UPDATE/DELETE/DDL. The connection context manager commits on success."""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.rowcount


if __name__ == "__main__":
    tables = run_query("SELECT * FROM users")
    for t in tables:
        print(t["username"])