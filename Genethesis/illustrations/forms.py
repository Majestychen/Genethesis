from flask_wtf import FlaskForm
from wtforms import MultipleFileField
from flask_wtf.file import FileAllowed

class IllustrationUploadForm(FlaskForm):
    illustrations = MultipleFileField('上传插图', validators=[FileAllowed(['jpg', 'png', 'jpeg'], message='好像混入了一些不是图片的东西……')])