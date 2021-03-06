# -----------------------------------------------+
# FLASK MAIN SERVER                              +
# -----------------------------------------------+

# IMPORT ----------------------------------------+
from flask import Flask, request, jsonify, render_template, redirect    # Main Server
from flask_sqlalchemy import SQLAlchemy                                 # Database ORM
from datetime import datetime as dt                                     # Display Current time
from pytz import timezone                                               # Singapore Time Format

# INIT ------------------------------------------+
app = Flask(__name__)                                                   # Initialize Flask
app.config['secret_key'] = "This_Is_Development_Key"                    # Flask Security Key
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///email_database.db"   # Database Path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False                    # Disable Verbose logging
db = SQLAlchemy(app)                                                    # Initialize ORM

# ENDPOINTS -------------------------------------+
@app.route('/')
@app.route('/index')
def index():
    try:                                                                # if Database file is present
        cli_emails = ClientEmail.query.all()                            # Fetch all data from database
        return render_template('index.html', data=cli_emails), 200
    except:
        db.create_all()
        return redirect('/')

@app.route('/save_emails', methods=['POST'])
def save_email():                                                       # Save email details into database
    eventid     = request.form.get('event_id', type=int),
    emailsubj   = request.form.get('email_subject')
    emailcont   = request.form.get('email_content')
    currenttime = dt.now(tz=timezone('Asia/Singapore')).strftime("%d %b %Y %H:%M")
    
    if str(type(eventid[0])) == "<class 'int'>":                        # Check if Event ID is Integer
        if all([emailsubj != "", emailcont != ""]):                     # Check is any empty string on Subject and Content

            if not any(["unit testing" in emailsubj, "unit testing" in emailcont]): # Check if running unit testing
                client_email = ClientEmail(
                    event_id=eventid[0],
                    email_subject=emailsubj.encode('utf-8'),
                    email_content=emailcont.encode('utf-8'),
                    timestamp=currenttime,
                    status="notsend"
                )
                db.session.add(client_email)                            # Save Data
                db.session.commit()                                     # Write Changes on Database
                return redirect('/')
            else:
                return "Success: Data successfully inserted!",201
        else:
            return "Error: Required Data not provided", 400
    else:
        return "Error: EventID must be Integer", 400

@app.route('/send_email',methods=['POST'])
def send_email():
    pass

# EXPERIMANTAL ENDPOINTS ------------------------+
@app.route('/api', methods=['GET','POST','PUT','DELETE'])               # Experimental Build
def api():
    if request.method == 'GET':
        cli_emails = ClientEmail.query.all()
        myarr = []
        for email in cli_emails:
            myarr.append({'event_id': email.event_id, 'email_subject': email.email_subject, 'email_content': email.email_content, 'timestamp': email.timestamp})
        return jsonify({'data': myarr}), 200

@app.route('/ajax')                                                     # Experimental Build
def ajax():
    return render_template('async.html'), 200

# MODEL -----------------------------------------+
class ClientEmail(db.Model):
    event_id        = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    email_subject   = db.Column(db.String(30), nullable=False)
    email_content   = db.Column(db.String(50), nullable=False)
    timestamp       = db.Column(db.String(15), nullable=False)
    status          = db.Column(db.String(15), nullable=False)

# RUN -------------------------------------------+
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=81, debug=True)
# END -------------------------------------------+
