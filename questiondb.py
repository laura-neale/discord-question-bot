import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
HOST = os.getenv('DB_HOST')
DATABASE = os.getenv('DB_NAME')
USER = os.getenv('USER')

def select_question():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT question FROM discord_chatbot_questions ORDER BY last_asked NULLS FIRST, user_submitted DESC, random()")
    qs = cur.fetchone()
    question = qs[0]
    cur.execute("UPDATE discord_chatbot_questions SET last_asked = now() WHERE question = %s", (question,))
    conn.commit()
    cur.close
    return question


def connect_to_db():
    return psycopg2.connect(host=HOST, database=DATABASE, user=USER)


def insert_question(q):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM discord_chatbot_questions WHERE question=%s", (q,))
    count = cur.fetchone()
    if count > 0:
        cur.execute("UPDATE discord_chatbot_questions SET last_asked = null WHERE question=%s", (q,))
    else:
        cur.execute("INSERT INTO discord_chatbot_questions (question, user_submitted) VALUES (%s, true)", (q,))
    conn.commit()
    cur.close
