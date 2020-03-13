import psycopg2


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
    return psycopg2.connect(host="doris.devserver0.btn1.bwcom.net", database="brandwatch-crawler.db", user="brandwatch")


def insert_question(q):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO discord_chatbot_questions (question, user_submitted) VALUES (%s, true)", (q,))
    conn.commit()
    cur.close
