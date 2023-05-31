from flask import Flask, render_template
import psycopg2

### Make the flask app
app = Flask(__name__)

### Functions
def debug(s):
    """Prints a message to the screen (not web browser) 
    if FLASK_DEBUG is set."""
    if app.config['DEBUG']:
        print(s)

def get_db():
    return psycopg2.connect(
    host="localhost",
    database="SemiKhadam",
    user="postgres",
    password="admin"
    )

### Routes
@app.route("/browse", methods=['get', 'post'])
def browse():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('select id, date, title, content from entries order by date')
    rowlist = cursor.fetchall()
    print(rowlist);
    return render_template('browse.html', entries=rowlist)

@app.route("/populate", methods=['get', 'post'])
def populate_db():
    conn = get_db()
    cur = conn.cursor()
    with app.open_resource("populate.sql") as file: # open the file
        alltext = file.read() # read all the text
        cur.execute(alltext) # execute all the SQL in the file
    conn.commit()
    print("Populated DB with sample data.")
    return render_template("create_data.html")

@app.route("/create", methods=['get', 'post'])
def init_db():
    """Clear existing data and create new tables."""
    conn = get_db()
    cur = conn.cursor()
    with app.open_resource("schema.sql") as file: # open the file
        alltext = file.read() # read all the text
        cur.execute(alltext) # execute all the SQL in the file
    conn.commit()
    print("Initialized the database.")
    return render_template("con_db.html")

@app.route("/")
def main():
    name = "Semi"
    surname = "Al_Khadam"
    group = "KID-21"
    return render_template("index.html", name=name, surname=surname, group_and_id=group)

### Start flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5433, debug=True)
