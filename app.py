from flask import Flask,render_template,request,redirect,url_for,session,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time

app = Flask(__name__)
app.secret_key = 'super secret key'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:andynoodles@localhost/flaskdb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table = db.Column(db.String(200), nullable=False)
    meal = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id





@app.route('/',methods=['POST','GET'])
def home():
    if request.method == 'POST':
        nm = request.form['table']
        meal = request.form['food']
        TableNum = Todo(table=nm,meal=meal)

        try:
            db.session.add(TableNum)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding TableNum'

    else:
        return render_template('index.html')



@app.route('/adminpage')
def admin():
    TableNum = Todo.query.order_by(Todo.date_created).all()
    return render_template('adminpage.html', TableNum=TableNum)
    
@app.route('/mqttstart/<int:id>')
def mqttstart(id):
    return  '<h1>mqttstart</h1>'
            
@app.route('/mqttfinished/<int:id>')
def mqttfinished(id):
    order_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(order_to_delete)
        db.session.commit()
        return redirect('/adminpage')
    except:
        return 'There was a problem deleting that order'


if __name__ == '__main__':
    app.run(debug=True)




