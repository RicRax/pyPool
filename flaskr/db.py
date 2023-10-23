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

    # Commit the changes
    conn.commit()
    # Close the connection
    cursor.close()
    conn.close()
