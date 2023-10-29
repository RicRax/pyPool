from os import walk
import logging
import psycopg2


def initDB(app):
    conn = psycopg2.connect(user="riccardo", database="pyPoll")

    conn.autocommit = True
    cursor = conn.cursor()

    # Create the users table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        sub VARCHAR(100) UNIQUE NOT NULL
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
        poll_id INT REFERENCES polls(poll_id),
        votes INT 
    )
    """
    )

    conn.commit()
    cursor.close()
    conn.close()


def checkIfUserExists(username, sub):
    conn = psycopg2.connect(user="riccardo", database="pyPoll")

    conn.autocommit = True
    cursor = conn.cursor()

    insert_query = "SELECT * FROM users WHERE username = %s AND sub = %s"
    cursor.execute(insert_query, (username, sub))

    user_exists = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    if user_exists is not None:
        return True
    else:
        return False


def addUser(username, sub):
    conn = psycopg2.connect(user="riccardo", database="pyPoll")

    conn.autocommit = True
    cursor = conn.cursor()

    insert_query = "INSERT INTO users (username,sub) VALUES (%s,%s)"
    cursor.execute(insert_query, (username, sub))

    conn.commit()
    cursor.close()
    conn.close()


def createPoll(title, description, choices, username):
    conn = psycopg2.connect(user="riccardo", database="pyPoll")

    print("creating table")

    conn.autocommit = True
    cursor = conn.cursor()

    select_user = "SELECT user_id FROM users WHERE username = %s"
    cursor.execute(select_user, (username,))
    user_id = cursor.fetchone()

    conn.commit()

    insert_query = "INSERT INTO polls (title, description,user_id) VALUES (%s, %s, %s) RETURNING poll_id"
    cursor.execute(insert_query, (title, description, user_id))
    conn.commit()

    poll_id = cursor.fetchone()

    for choice in choices:
        insert_query = (
            "INSERT INTO choices (poll_id, choice_text,votes) VALUES (%s, %s, 0) "
        )
        cursor.execute(insert_query, (poll_id, choice))
        conn.commit()

    cursor.close()
    conn.close()

    return


def selectPoll(pollID):
    conn = psycopg2.connect(user="riccardo", database="pyPoll")

    print("selecting table")

    conn.autocommit = True
    cursor = conn.cursor()

    insert_query = "SELECT * FROM polls WHERE poll_id = '%s'"
    cursor.execute(insert_query, (pollID,))

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


def getPollsOfUser(username):
    conn = psycopg2.connect(user="riccardo", database="pyPoll")

    print("selecting table")

    conn.autocommit = True
    cursor = conn.cursor()
    select_user = "SELECT user_id FROM users WHERE username = %s"
    cursor.execute(select_user, (username,))
    user_id = cursor.fetchone()

    conn.commit()

    select_polls = "SELECT title FROM polls WHERE user_id = %s"
    cursor.execute(select_polls, (user_id,))

    polls = cursor.fetchall()
    pollTitles = [{"title": title} for title in polls]

    conn.commit()
    cursor.close()
    conn.close()

    print(polls)

    return pollTitles


def getChoicesText(pollID):
    conn = psycopg2.connect(user="riccardo", database="pyPoll")

    conn.autocommit = True
    cursor = conn.cursor()

    insert_query = "SELECT choice_text FROM choices WHERE poll_id = '%s'"
    cursor.execute(insert_query, (pollID,))

    choices = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    print(choices)

    return choices


def getChoices(pollID):
    conn = psycopg2.connect(user="riccardo", database="pyPoll")

    conn.autocommit = True
    cursor = conn.cursor()

    insert_query = "SELECT * FROM choices WHERE poll_id = '%s'"
    cursor.execute(insert_query, (pollID,))

    choices = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    print(choices)

    return choices


def insertVote(pollID, choiceText):
    conn = psycopg2.connect(user="riccardo", database="pyPoll")

    print("insertingVote")

    conn.autocommit = True
    cursor = conn.cursor()

    update_query = "UPDATE choices SET votes = votes + 1 WHERE poll_id = %s AND choice_text = %s RETURNING votes"
    cursor.execute(update_query, (pollID, choiceText))

    votes = cursor.fetchone()
    # not sure if working properly

    conn.commit()
    cursor.close()
    conn.close()

    return votes
