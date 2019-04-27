# -----------------------------------------------+
# FLASK MAIN SERVER                              +
# -----------------------------------------------+

# IMPORT ----------------------------------------+
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from pytz import timezone

# INIT ------------------------------------------+
app = Flask(__name__)
app.config['secret_key'] = "This_Is_Development_Key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///email_database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ENDPOINTS -------------------------------------+
@app.route('/')
@app.route('/index')
def index():
    cli_emails = ClientEmail.query.all()
    return render_template('index.html', data=cli_emails)

@app.route('/api', methods=['GET','POST','PUT','DELETE'])
def api():
    if request.method == 'GET':
        cli_emails = ClientEmail.query.all()
        myarr = []
        for email in cli_emails:
            myarr.append({'event_id': email.event_id, 'email_subject': email.email_subject, 'email_content': email.email_content, 'timestamp': email.timestamp})
        return jsonify({'data': myarr})

@app.route('/save_emails', methods=['POST'])
def save_email():
    eventid     = request.form.get('event_id', type=int),
    emailsubj   = request.form.get('email_subject')
    emailcont   = request.form.get('email_content')
    currenttime = dt.now(tz=timezone('Asia/Singapore')).strftime("%d %b %Y %H:%M")

    #if all("" not in var for var in [emailsubj, emailcont]): # Check if all values is filled
    client_email = ClientEmail(
        event_id= eventid[0], 
        email_subject= emailsubj, 
        email_content= emailcont, 
        timestamp= currenttime
    )
    db.session.add(client_email)
    db.session.commit()
    return "Data successfully inserted!"

@app.route('/time')
def time():
    mytime = mdl.getTime()
    return jsonify({'time': mytime})

# MODEL -----------------------------------------+
class ClientEmail(db.Model):
    event_id        = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    email_subject   = db.Column(db.String(30), nullable=False)
    email_content   = db.Column(db.String(50), nullable=False)
    timestamp       = db.Column(db.String(15), nullable=False)

# RUN -------------------------------------------+
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=81, debug=True)
# END -------------------------------------------+
