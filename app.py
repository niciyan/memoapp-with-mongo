import datetime
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length
from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
from flask_bootstrap import Bootstrap

app = Flask(__name__)
db = MongoEngine(app)
bootstrap = Bootstrap(app)

app.config["MONGODB_SETTINGS"] = { "db":"nishi" }
app.config['SECRET_KEY'] = "ok"
app.debug = True

class Post(db.Document):
    title = db.StringField(max_length=100, required=True)
    content = db.StringField(max_length=200, required=True)
    tags = db.ListField(db.StringField(max_length=10), mix_entries=1)
    created_at = db.DateTimeField(default=datetime.datetime.now)

# PostForm = model_form(Post)

class PostForm(FlaskForm):
    title = StringField('Title',validators=[Required(), Length(1,80)])
    content = StringField('Content',validators=[Required(), Length(1,180)])
    submit = SubmitField('submit')

@app.route('/')
def index():
    page = request.args.get("page", default=1, type=int)
    posts = Post.objects.order_by("-created_at").paginate(page=page, per_page=10).items
    return render_template('index.html', posts=posts)

@app.route('/add', methods=["GET", "POST"])
def add():
    form = PostForm()
    if form.validate_on_submit():
        Post(title=form.title.data, content=form.content.data).save()
        flash('post added!')
        return redirect(url_for("index"))
    return render_template('add.html', form=form)

@app.route('/delete')
def delete():
    # id come from url param
    _id = request.args.get('id',type=str)
    post = Post.objects.get(id=_id)
    post.delete()
    # post = Post(id).delete()
    flash("the post deleted")
    return redirect(url_for("index"))



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555)
