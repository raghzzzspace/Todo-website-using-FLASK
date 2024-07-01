from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@server/db'


db=SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=True)
    date_created= db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return f'<Todo {self.sno} - {self.title}>'


@app.route('/',methods=['GET','POST']) 
def add_todo():
    #return 'Hello, World!'
    if request.method=='POST':
            title=request.form['title']
            desc =request.form['desc']
            todo=Todo(title=title,desc=desc)
            db.session.add(todo)
            db.session.commit()

    todos=Todo.query.all()
    return render_template('index.html',alltodo=todos)

@app.route('/update/<int:sno>',methods=['GET','POST']) 
def update(sno):
    if request.method=='POST':
         title=request.form['title']
         desc=request.form['desc']
         todo=Todo.query.filter_by(sno=sno).first()
         todo.title=title
         todo.desc=desc
         db.session.add(todo)
         db.session.commit()
         return redirect('/')

    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>') 
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return  redirect('/')





    


if __name__=="__main__":
    app.run(debug=True)  
    #app.run(debug=True,port=8000)