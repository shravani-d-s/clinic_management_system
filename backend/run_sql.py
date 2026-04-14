import os
import sys
import oracledb

def run_sql_file(filename):
    # DSN connection same as database.py
    # using load_dotenv if available
    from dotenv import load_dotenv
    load_dotenv()
    
    conn = oracledb.connect(
        user=os.getenv("DB_USER", "system"),
        password=os.getenv("DB_PASSWORD", "oracle"),
        dsn=oracledb.makedsn(os.getenv("DB_HOST", "127.0.0.1"), os.getenv("DB_PORT", "1521"), service_name=os.getenv("DB_SERVICE", "XE"))
    )
    cursor = conn.cursor()
    
    with open(filename, 'r') as f:
        sql = f.read()
    
    # Split by / that are alone on a line for PL/SQL blocks or triggers
    statements = []
    current_statement = []
    
    lines = sql.split('\n')
    for line in lines:
        stripped = line.strip()
        if stripped == '/' and current_statement:
            statements.append('\n'.join(current_statement))
            current_statement = []
        elif stripped == 'EXIT;':
            pass
        elif stripped.startswith('--'):
            pass
        else:
            if stripped:
                current_statement.append(line)
                
        # If it's a simple statement ending with ; but not inside a PL/SQL block
        if stripped.endswith(';') and not any(kw in '\n'.join(current_statement).upper() for kw in ['BEGIN', 'DECLARE', 'CREATE OR REPLACE TRIGGER']):
            stmt = '\n'.join(current_statement).rstrip(';')
            statements.append(stmt)
            current_statement = []

    # Final flush
    if current_statement:
        stmt = '\n'.join(current_statement).rstrip(';')
        if stmt.strip():
            statements.append(stmt)

    success = 0
    fail = 0
    for stmt in statements:
        if not stmt.strip(): continue
        try:
            cursor.execute(stmt)
            success += 1
        except Exception as e:
            print(f"Error executing:\n{stmt[:100]}...\n{e}\n")
            fail += 1

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Ran {filename}: {success} succeeded, {fail} failed.")

if __name__ == '__main__':
    run_sql_file(sys.argv[1])
