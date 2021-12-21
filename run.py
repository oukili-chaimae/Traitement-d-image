import projet
from projet import app

from flask_mysqldb import MySQL
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "projet"

mysql = MySQL(app)

if __name__ == "__main__":
        app.run(debug=True)