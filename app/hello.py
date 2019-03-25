sys.path.append('/home/amt597/RoadsideAssist')
from myapp import app as application

from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
return "Roadside Assistance Application"

if __name__ == "__main__":
app.run()
