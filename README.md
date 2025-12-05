 Dockerized Python → PostgreSQL Example :

This repository demonstrates a simple Python app that connects to a PostgreSQL container on a custom Docker network. The app:

 connects to PostgreSQL
 creates a table
 inserts a row
 reads and prints rows

 `app.py` — simple Python script that connects to PostgreSQL, creates a `students` table, inserts rows, and prints them.
 `Dockerfile` — builds a small Python 3.10-slim image that runs `app.py` and installs `psycopg2-binary`.
 (optional) `docker-compose.yml` — quick compose file to run Postgres + the app together (provided below).
app.py (example)
python
import psycopg2
import time
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

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100)
        );
    """)
    conn.commit()

    cur.execute("INSERT INTO students (name) VALUES ('Aalla');")
    conn.commit()

    cur.execute("SELECT * FROM students;")
    rows = cur.fetchall()

    print("Data from DB:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()

except Exception as e:
    print("Error:", e)

Dockerfile (example)

dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY app.py .

RUN pip install psycopg2-binary

CMD ["python", "app.py"]

1. Create a custom docker network
docker network create mynetwork

If you get `Error response from daemon: network with name mynetwork already exists` — it's fine: the network already exists.

2. Run PostgreSQL container

Single-line (recommended in PowerShell):
docker run -d --name my-postgres --network mynetwork -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=mydb postgres
docker run -d `
  --name my-postgres `
  --network mynetwork `
  -e POSTGRES_USER=user `
  -e POSTGRES_PASSWORD=pass `
  -e POSTGRES_DB=mydb `
  postgres
3. Build the Python app image

From the folder that contains `Dockerfile` and `app.py`:
<img width="1237" height="529" alt="image" src="https://github.com/user-attachments/assets/15a7d42b-ca0b-47db-8b4e-c3682ce2d937" />


docker build -t my-python-app .
4. Run the app container on the same network


docker run --rm --network mynetwork my-python-app
<img width="1186" height="107" alt="image" src="https://github.com/user-attachments/assets/1aaab213-02bc-44fc-9d02-e378c300eda2" />

Expected output (example):

```
Connected to PostgreSQL!
Data from DB:
(1, 'Aalla')
Expected project workflow (quick)

1. `docker network create mynetwork` (once)
2. `docker run -d --name my-postgres --network mynetwork -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=mydb postgres`
3. `docker build -t my-python-app .`
4. `docker run --rm --network mynetwork my-python-app`

<img width="1139" height="145" alt="image" src="https://github.com/user-attachments/assets/008d4df4-fead-40d2-b77a-523177bad74b" />


-
