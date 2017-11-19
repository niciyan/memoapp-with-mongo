from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Length


class PostForm(FlaskForm):
    title = StringField('Title',validators=[Required(), Length(1,80)])
    content = TextAreaField('Content',validators=[Required(), Length(1,180)])
    submit = SubmitField('Submit')

class MemoForm(FlaskForm):
    tag = StringField("Tag", validators=[Length(1,20)])
    body = TextAreaField("Memo", validators=[Length(1,150)])
    submit = SubmitField('Submit')

