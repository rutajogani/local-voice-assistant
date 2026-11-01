import os
from typing import Any, List, Optional

from local_voice_assistant.agent_tools_instructions.query_db import (
    get_table_schema,
    list_tables,
    run_command,
    run_query,
)

NOTES_FILE = "notes.txt"

def save_note(note:  str) -> str:
    with open(NOTES_FILE, "a", encoding="utf-8")as file:
        file.write(f"- {note}\n")
    return "Note saved"

def read_notes() -> str:
    if not os.path.exists(NOTES_FILE):
        return "No notes saved yet!"
    with open(NOTES_FILE, encoding="utf-8")as file:
        return file.read()

def select_query(sql: str, params: Optional[List[Any]] = None) -> List[dict]:
    """Run a read-only SELECT query on the PostgreSQL database and return the rows.
    
    Use this to look up data, for example users. The `users` table has a
    `username` column. Never use this for INSERT, UPDATE, or DELETE.

    Args:
        sql: A SELECT statement. Use %s placeholders for values.
        params: Values for the %s placeholders, in order.
    """
    rows = run_query(sql)
    return [dict(r) for r in rows]

def query_command(sql: str, params: Optional[List[Any]] = None) -> int:
    """Run an INSERT, UPDATE, or DELETE statement on the PostgreSQL database.
   
    Use this only when the user explicitly asks to add, change, or remove data.

    Args:
        sql: An INSERT, UPDATE, or DELETE statement. Use %s placeholders for values.
        params: Values for the %s placeholders, in order.

    Returns:
        The number of rows affected.
    """
    return run_command(sql, params)

def get_schema_of_table(table_name: str) -> List[dict]:
    """Get the columns of a table: name, data type, nullable, and default.

    Always call this before writing a SQL query for a table, so you use the
    correct column names.

    Args:
        table_name: The exact name of the table, for example "users".
    """
    rows = get_table_schema(table_name)
    if not rows:
        return [{"error": f"Table '{table_name}' not found. Call tables_list to see available tables."}]
    return [dict(r) for r in rows]


def tables_list() -> List[str]:
    """List all tables in the PostgreSQL database.

    Use this first when you don't know which tables exist.
    """
    return list_tables()

def tools():
    tools = [save_note, read_notes, select_query, query_command, get_schema_of_table, tables_list]

    return tools

