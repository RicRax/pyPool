from os import walk
import psycopg2


def initDB():
    conn = psycopg2.connect(user="riccardo", database="pyPoll")

    conn.autocommit = True
    cursor = conn.cursor()

    # Create the users table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY
    )
    """
    )

    # Create the polls table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS polls (
        poll_id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        created_at TIMESTAMP,
        user_id INT REFERENCES users(user_id)
    )
    """
    )

    # Create the choices table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS choices (
        choice_id SERIAL PRIMARY KEY,
        choice_text TEXT NOT NULL,
        poll_id INT REFERENCES polls(poll_id)
    )
    """
    )

    # Create the responses table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS responses (
        response_id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(user_id),
        choice_id INT REFERENCES choices(choice_id),
        chosen_choices INT[]
    )
    """
    )

    conn.commit()
    cursor.close()
    conn.close()


def createPoll(title, description):
    conn = psycopg2.connect(user="riccardo", database="pyPoll")

    print("creating table")

    conn.autocommit = True
    cursor = conn.cursor()

    insert_query = (
        "INSERT INTO polls (title, description) VALUES (%s, %s) RETURNING title"
    )
    cursor.execute(insert_query, (title, description))

    title = cursor.fetchone()
    print(title)
    # not sure if working properly

    conn.commit()
    cursor.close()
    conn.close()

    return


def selectPoll(pollID):
    conn = psycopg2.connect(user="riccardo", database="pyPoll")

    print("selecting table")

    conn.autocommit = True
    cursor = conn.cursor()

    insert_query = "SELECT * FROM polls WHERE poll_id = %s"
    cursor.execute(insert_query, pollID)

    poll = cursor.fetchone()
    if poll:
        # Process the data as needed
        poll_id, title, description, created_at, user_id = poll
        result = {
            "poll_id": poll_id,
            "title": title,
            "description": description,
            "created_at": created_at,
            "user_id": user_id,
        }
    else:
        return "Poll not found."

    conn.commit()
    cursor.close()
    conn.close()

    print(result)

    return result
