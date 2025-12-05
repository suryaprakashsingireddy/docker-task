import psycopg2
import time

# Wait for PostgreSQL container to be ready
time.sleep(5)

try:
    conn = psycopg2.connect(
        host="my-postgres",
        database="mydb",
        user="user",
        password="pass"
    )
    print("Connected to PostgreSQL!")

    cur = conn.cursor()

    # 1. Create table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100)
        );
    """)
    conn.commit()

    # 2. Insert one row
    cur.execute("INSERT INTO students (name) VALUES ('surya bhai');")
    conn.commit()

    # 3. Read the row
    cur.execute("SELECT * FROM students;")
    rows = cur.fetchall()

    print("Data from DB:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()

except Exception as e:
    print("Error:", e)
