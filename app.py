from flask import Flask,render_template,request,redirect,url_for,session,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
import paho.mqtt.client as mqtt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

mqttc=mqtt.Client()
mqttc.connect("broker.emqx.io",1883,60)
mqttc.loop_start()

loginmanager= LoginManager()
loginmanager.init_app(app)
loginmanager.login_view="login"

@loginmanager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table = db.Column(db.String(200), nullable=False)
    meal = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '%r' % self.id

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False,unique=True)
    password = db.Column(db.String(80), nullable=False)

class LoginForm(FlaskForm):
    username =  StringField(validators=[InputRequired(),Length(
        min = 4, max=20)], render_kw={"placeholder":"username"})
    password =  PasswordField(validators=[InputRequired(),Length(
        min = 4, max=20)], render_kw={"placeholder":"password"})
    
    submit = SubmitField("Login")




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




@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            password = User.query.filter_by(password=form.password.data).first()
            if password:
                login_user(user)
                return redirect(url_for('adminpage'))
            else:
                return "<h1>Wrong password</h1>"
        else:
            return "<h1>Wrong username</h1>"

    return render_template('login.html',form = form)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))




@app.route('/adminpage')
@login_required
def adminpage():
    TableNum = Todo.query.order_by(Todo.date_created).all()
    return render_template('adminpage.html', TableNum=TableNum)
    
    
    
@app.route('/mqttstart/<id>/<table>')
@login_required
def mqttstart(id,table):
    id = Todo.query.get_or_404(id)
    if table == "1":
        mqttc.publish("flaskmqtt","1")
    if table == "2":
        mqttc.publish("flaskmqtt","2")
    if table == "3":
        mqttc.publish("flaskmqtt","3")
    if table == "4":
        mqttc.publish("flaskmqtt","4")
    flash(f"Order have been sent to the bot. Order id:{id}")
    return  redirect(url_for('adminpage'))



@app.route('/mqttfinished/<int:id>')
@login_required
def mqttfinished(id):
    order_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(order_to_delete)
        db.session.commit()
        return redirect(url_for('adminpage'))
    except:
        return 'There was a problem deleting that order'





if __name__ == '__main__':
    app.run(debug=True)




