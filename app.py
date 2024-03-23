from flask import Flask, render_template, request, redirect, url_for,  flash
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///toplanti.db'
db = SQLAlchemy(app)

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    participants = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

    sample_meetings = [
        {"topic": "Backend Toplantısı", "date": datetime.datetime.strptime("2024-09-08", "%Y-%m-%d").date(), "start_time": datetime.datetime.strptime("09:00", "%H:%M").time(), "end_time": datetime.datetime.strptime("12:00", "%H:%M").time(), "participants": "Rümeysa, Ayşe, Seda"},
        {"topic": "Frontend Toplantısı", "date": datetime.datetime.strptime("2024-07-18", "%Y-%m-%d").date(), "start_time": datetime.datetime.strptime("14:00", "%H:%M").time(), "end_time": datetime.datetime.strptime("16:00", "%H:%M").time(), "participants": "Berkant, Talha, Ali"},
        {"topic": "Pazarlama Toplantısı", "date": datetime.datetime.strptime("2024-03-24", "%Y-%m-%d").date(), "start_time": datetime.datetime.strptime("15:00", "%H:%M").time(), "end_time": datetime.datetime.strptime("12:00", "%H:%M").time(), "participants": "Rümeysa, Ayşe, Seda"},
        {"topic": "Genel Toplantı", "date": datetime.datetime.strptime("2024-01-29", "%Y-%m-%d").date(), "start_time": datetime.datetime.strptime("11:00", "%H:%M").time(), "end_time": datetime.datetime.strptime("16:00", "%H:%M").time(), "participants": "Berkant, Talha, Ali"},
         ]

    for meeting_data in sample_meetings:
        meeting = Meeting(**meeting_data)
        db.session.add(meeting)

    # Değişiklikleri kaydet
    db.session.commit()


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    meeting = Meeting.query.get(id)
    if meeting:
        db.session.delete(meeting)
        db.session.commit()
       
  
    
    return redirect(url_for('home'))

@app.route("/")
def home():
    meetings = Meeting.query.order_by(Meeting.id).all()
    return render_template('index.html',meetings=meetings)

@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        date_string = request.form['date']
        topic = request.form['topic']
        participants = request.form['participants']  # Değiştirildi
        start_time_str = request.form['start_time']
        end_time_str = request.form['end_time']
        start_time = datetime.datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.datetime.strptime(end_time_str, '%H:%M').time()

        date = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()

        meeting = Meeting(topic=topic, date=date, start_time=start_time, end_time=end_time, participants=participants)
        db.session.add(meeting)
        db.session.commit()
    
        return redirect(url_for('index'))

    else:
        return render_template('index.html')



@app.route('/form_edit/<int:id>', methods=['GET','POST'])
def form_edit(id):
    meeting = Meeting.query.get_or_404(id)

    if request.method == 'POST':
        date_string = request.form['date']
        topic = request.form['topic']
        participants = request.form['participants']  # Değiştirildi
        start_time_str = request.form['start_time']
        end_time_str = request.form['end_time']
        start_time = datetime.datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.datetime.strptime(end_time_str, '%H:%M').time()

        date = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()

       
        meeting.topic = topic
        meeting.date = date
        meeting.start_time = start_time
        meeting.end_time = end_time
        meeting.participants = participants

        db.session.commit()
    
        return redirect(url_for('home'))

    else:
        return render_template('index.html', meeting=meeting)


if __name__ == '__main__':
    app.run(debug=True)
