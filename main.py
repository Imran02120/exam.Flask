from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())


@app.route('/home')
@app.route('/')
def index():
    return  render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)





@app.route("/create-article", methods=["POST", "GET"])
def create_article():
    if request.method =="POST":
        title = request.form["title"]
        intro = request.form["intro"]
        text = request.form["text"]

        # with app.app_context():
        #     db.create_al





        print(title)
        print(intro)
        print(text)
        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect("/posts")
        except Exception as e:
            print(e)
            return "При добавении статьи произшла неизвестная ошибка"



    else:
        return render_template("create_article.html")

@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    print(article)
    return render_template('post_detail.html', article = article)



@app.route('/posts/delete/<int:id>')
def posts_delete(id):
    article = Article.query.get(id)


    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/posts")
    except Exception as e:
        print(e)
        return "При удалении призошла ошибка"



@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return f'Имя:  {name}, ID:{id}'



if __name__ == '__main__':
    app.run(debug=True)

