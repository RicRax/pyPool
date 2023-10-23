import psycopg2


def initDB():
    conn = psycopg2.connect(user="riccardo", database="pyPoll")

    conn.autocommit = True
    cursor = conn.cursor()

    # Close the connection
    cursor.close()
    conn.close()
