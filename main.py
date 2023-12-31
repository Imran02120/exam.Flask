from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy  import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()



class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('get_posts.html', articles=articles)


@app.route('/posts/<int:id>')
def get_posts_detail(id):
    article=Article.query.get(id)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create-article', methods=["POST", "GET"])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        # with app.app_context():
        #     db.create_all()
        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return 'При добавлении статьи произошла ошибка'


    else:
        return render_template('/create-article.html')



if __name__ == '__main__':
    app.run(debug=True)








