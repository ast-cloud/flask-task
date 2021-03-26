from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)


class task(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(200), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"



@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        tsk=task(title=title, desc=desc)
        db.session.add(tsk)
        db.session.commit()
    alltasks=task.query.all()
    return render_template('index.html',alltasks=alltasks)
    
@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        tsk=task.query.filter_by(sno=sno).first()
        tsk.title=title
        tsk.desc=desc
        db.session.add(tsk)
        db.session.commit()
        return redirect("/")

    tsk=task.query.filter_by(sno=sno).first()

    return render_template('update.html',tsk=tsk)

@app.route('/delete/<int:sno>')
def delete(sno):
    tsk=task.query.filter_by(sno=sno).first()
    db.session.delete(tsk)
    db.session.commit()
    return redirect('/')

@app.route('/api/data')
def data():
    alltasks=task.query.all()
    dict={}
    for i,t in enumerate(alltasks):
        dict[i]={
            "title":t.title,
            "desc":t.desc,
            "datetime":t.date_created
        }
    return jsonify(dict)

if __name__=="__main__":
    app.run(debug=True, port=8000)