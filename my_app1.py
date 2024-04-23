import flask_sqlalchemy
from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, func
import re
app=Flask(__name__)



app.app_context()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.db'
db = SQLAlchemy(app)

class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    author_name = db.Column(db.String(80))
    theme = db.Column(db.String(100))
    blog_data = db.Column(db.Text)
    date = db.Column(db.String(10))


    def __init__(self, author_name, theme, blog_data, date):
        self.author_name = author_name
        self.theme = theme
        self.blog_data = blog_data
        self.date = date
    def __repr__(self):
        return '<User %r>' % self.username


with app.app_context():
    db.create_all()
    blog=Blogs("Муравьёва Светлана", "Съехал в кювет и скрылся",'''Вечером 30 октября житель Тверской области, 1979 года рождения, находясь за рулём автомашины "Рено", на повороте на село Сутка не справился с управлением и совершил съезд в кювет, где транспортное средство опрокинулось. Ни сам водитель, ни его пассажир – брейтовец, 1982 года рождения, – не пострадали, а вот техника получила серьёзные механические повреждения.
По факту ДТП вынесено определение об отказе в возбуждении дела об административном правонарушении. Виновник аварии с места происшествия скрылся, но впоследствии был разыскан сотрудниками ГИБДД. Кроме того, в момент её совершения мужчина находился в состоянии алкогольного опьянения. В отношении него составлены два административных протокола; материалы направлены на рассмотрение в судебный участок № 1 Брейтовского судебного района. За управление транспортным средством в состоянии опьянения водителю грозит лишение права управления техникой на срок от 1,5 до 2 лет и штраф в сумме 30000 рублей; за оставление места ДТП, участником которого он стал, – лишение права управления техникой на срок от 1 до 1,5 лет либо административный арест до 15 суток.''', "16.11.2023")
    # db.session.add(blog)
    # db.session.commit()
    db.session.close()
     
@app.route("/")
def main():
    blogs = Blogs.query.order_by(-Blogs.id).all()
    return render_template('main.html',blogs=blogs)


@app.route("/showtext")
def showtext( text=blog.blog_data):
    content=request.args.get('text')
    mytext = re.split(r'\n\s*\n', content)
    text=mytext[0]
    return render_template('showtext.html',text=text)

@app.route('/add_blog', methods=['POST'])
def add_blog():
    name=request.form['author_name']
    theme=request.form['theme']
    text=request.form['blog_data']
    date=request.form['date']
    blog=Blogs(name,theme,text,date)
    db.session.add(blog)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True) 

   
