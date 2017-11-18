import datetime
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Length
from flask_mongoengine import MongoEngine
from flask_bootstrap import Bootstrap

app = Flask(__name__)
db = MongoEngine(app)
bootstrap = Bootstrap(app)

app.config["MONGODB_SETTINGS"] = { "db":"nishi" }
app.config['SECRET_KEY'] = "ok"
app.debug = True

class Memo(db.EmbeddedDocument):
    tag = db.StringField(max_length=20)
    body = db.StringField(max_length=150)

class Post(db.Document):
    title = db.StringField(max_length=100, required=True)
    content = db.StringField(max_length=200, required=True)
    memo = db.EmbeddedDocumentField(Memo)
    created_at = db.DateTimeField(default=datetime.datetime.now)

# PostForm = model_form(Post)

class PostForm(FlaskForm):
    title = StringField('Title',validators=[Required(), Length(1,80)])
    content = TextAreaField('Content',validators=[Required(), Length(1,180)])
    submit = SubmitField('Submit')

class MemoForm(FlaskForm):
    tag = StringField("Tag", validators=[Length(1,20)])
    body = TextAreaField("Memo", validators=[Length(1,150)])
    submit = SubmitField('Submit')

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

@app.route('/edit-memo/<string:_id>', methods=['GET', 'POST'])
def edit_memo(_id):
    form = MemoForm()
    post = Post.objects.get(id=_id)
    if form.validate_on_submit():
        post.memo.tag = form.tag.data
        post.memo.body = form.body.data
        post.save()
        return redirect(url_for("index"))
    form.tag.data = post.memo.tag
    form.body.data = post.memo.body 
    return render_template('edit_memo.html', form=form, post=post)

@app.route('/create-memo/<string:_id>', methods=['GET', 'POST'])
def create_memo(_id):
    form = MemoForm()
    post = Post.objects.get(id=_id)
    if form.validate_on_submit():
        new_memo = Memo()
        new_memo.tag = form.tag.data
        new_memo.body = form.body.data
        post.memo = new_memo
        post.save()
        return redirect(url_for("index"))
    return render_template('edit_memo.html', form=form, post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555)
