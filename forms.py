from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Length


class PostForm(FlaskForm):
    title = StringField('タイトル',validators=[Required(), Length(1,80)])
    content = TextAreaField('本文',validators=[Required(), Length(1,180)])
    submit = SubmitField('保存')

class MemoForm(FlaskForm):
    tag = StringField("タグ", validators=[Length(1,20)])
    body = TextAreaField("メモ", validators=[Length(1,150)])
    submit = SubmitField('保存')

