from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500))
    ingredients = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Task %r % self.id>'
@app.route('/',methods=['GET','POST'] )
def index():
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        rating = float(request.form['rating'])
        description = request.form['description']


        nowy_przepis = Todo(name=name,ingredients=ingredients,description=description,rating=rating)
        try:
            db.session.add(nowy_przepis)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "problem z dodaniem przepisu!"
    else:
        przepisy = Todo.query.order_by(Todo.name).all()# wyswietlenie wszystkich przepisów
        return render_template('index.html',przepisy = przepisy)



@app.route('/delete/<int:id>')
def delete(id):
    try:

        to_delete = Todo.query.get_or_404(id)
        db.session.delete(to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "problem z usunięciem przepisu!"

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    to_update = Todo.query.get_or_404(id)
    if request.method == 'POST':
        try:
            to_update.name = request.form['name']
            to_update.ingredients = request.form['ingredients']
            to_update.rating = request.form['rating']
            to_update.description = request.form['description']
            db.session.commit()
            return redirect('/')
        except:
            return "problem z modyfikacją przepisu!"
    else:
        return render_template('update.html',recipe = to_update)


if __name__ == "__main__":
    with app.app_context():  # Fix: ensures db.create_all() runs with context
        db.create_all()
    app.run(debug=True)
