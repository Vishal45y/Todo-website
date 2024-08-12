from flask import Flask,render_template,request,redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db=SQLAlchemy(app)
class Todo(db.Model):
    Sno=db.Column(db.Integer,primary_key=True)
    Title=db.Column(db.String(200),nullable=False)
    Desc=db.Column(db.String(200),nullable=False)
    Date_created=db.Column(db.DateTime,default=datetime.utcnow)    # very imp D and T are both caps
    def __repr__(self) -> str:                 # Whenever I will print this database what I want to get should be given here..
        return f"{self.Sno}-{self.Title}"
@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method =='POST':
        title=request.form['title']            #title is the key that is (name attribute  of the input) which i used in app.py
        desc=request.form['desc']
        todo=Todo(Title=title,Desc=desc)      #todo is the instance here
        db.session.add(todo)
        db.session.commit()
    alltodo=Todo.query.all()       # collect all todos
    return render_template('index.htm' , alltodo=alltodo)    #alltodo is available in index.htm now
@app.route('/about')
def about():    
    return render_template('about.htm')
@app.route('/contact')
def contact():
    return render_template('contact.htm')
@app.route('/delete/<int:Sno>')
def delete(Sno):
    todo1=Todo.query.filter_by(Sno=Sno).first()
    db.session.delete(todo1)
    db.session.commit()
    return redirect('/')
@app.route('/update/<int:Sno>',methods=['GET','POST'])
def update(Sno):
    if request.method=='POST':
        title=request.form['title']            #title is the name of the input which i used in app.py
        desc=request.form['desc']
        todo=Todo.query.filter_by(Sno=Sno).first()
        todo.Title=title
        todo.Desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")    
    todo=Todo.query.filter_by(Sno=Sno).first()
    return render_template('update.htm',todo=todo)   #Now todo is available in update.htm
if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=8000)
