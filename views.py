from flask import Flask, request, render_template, flash, redirect, url_for, Blueprint
from models import Memo, Post
from forms import MemoForm, PostForm
from flask_mongoengine import DoesNotExist


main = Blueprint('main', __name__)

@main.route('/')
def index():
    page = request.args.get("page", default=1, type=int)
    posts = Post.objects.order_by("-created_at").paginate(page=page, per_page=10).items
    return render_template('index.html', posts=posts)

@main.route('/add', methods=["GET", "POST"])
def add():
    form = PostForm()
    if form.validate_on_submit():
        Post(title=form.title.data, content=form.content.data).save()
        flash('post added!')
        return redirect(url_for(".index"))
    return render_template('add.html', form=form)

@main.route('/delete')
def delete():
    # id come from url param
    _id = request.args.get('id',type=str)
    try:
        post = Post.objects.get(id=_id)
    except DoesNotExist:
        flash('the post alredy not exist.')
        return redirect(url_for(".index"))
    post.delete()
    # post = Post(id).delete()
    flash("the post deleted")
    return redirect(url_for(".index"))

@main.route('/edit-memo/<string:_id>', methods=['GET', 'POST'])
def edit_memo(_id):
    form = MemoForm()
    post = Post.objects.get(id=_id)
    if form.validate_on_submit():
        post.memo.tag = form.tag.data
        post.memo.body = form.body.data
        post.save()
        return redirect(url_for(".index"))
    form.tag.data = post.memo.tag
    form.body.data = post.memo.body 
    return render_template('edit_memo.html', form=form, post=post)

@main.route('/create-memo/<string:_id>', methods=['GET', 'POST'])
def create_memo(_id):
    form = MemoForm()
    post = Post.objects.get(id=_id)
    if form.validate_on_submit():
        new_memo = Memo()
        new_memo.tag = form.tag.data
        new_memo.body = form.body.data
        post.memo = new_memo
        post.save()
        return redirect(url_for(".index"))
    return render_template('edit_memo.html', form=form, post=post)

