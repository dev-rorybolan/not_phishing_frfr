from flask import Flask, request, render_template, redirect, url_for
import psycopg2
from psycopg2 import errors


conn = psycopg2.connect(
    host="aws-0-eu-central-1.pooler.supabase.com",
    port=5432,
database="postgres",
user="postgres.pwlkomkrtuddlqagjcrl",
    password="MorphoKnight101"
)
def hashall():
    pass
print("connected")
cursor = conn.cursor()
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")
@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

    return render_template("download.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            cursor.execute(
                "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
                (email, password)
            )
            conn.commit()
            return render_template("signup.html")
        except errors.UniqueViolation:
            conn.rollback()
            return "That email is already registered. Try logging in.", 400
        except Exception as e:
            conn.rollback()
            return f"An error occurred: {str(e)}", 500
    return render_template("signup.html")
@app.route('/admin/details')
def admin_details():
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    users_html = '<ul class="list-disc list-inside text-indigo-700 font-semibold">'
    for row in rows:
        email = row[0]
        password = row[1]
        users_html += f'<li>{email} | {password}</li>'
    users_html += '</ul>'

    return render_template("users.html", users_html=users_html)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969, debug=True)
