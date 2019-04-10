from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, DecimalField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_login import current_user
from Genethesis.models import Article

class newArticleForm(FlaskForm):
    language = SelectField('语言', choices=[('zh', '中文'), ('es', '西班牙语')])
    title = StringField('标题', validators=[DataRequired(), Length(max=120, message='由于系统限制，目前最多支持120字符的论文标题……')])
    titleAlt = StringField('第二语言标题（可不填）', validators=[Length(max=120, message='由于系统限制，目前最多支持120字符的论文标题……')])
    tutor = StringField('导师', validators=[DataRequired(), Length(max=60, message='谁名字这么长啊，您的导师是龙妈吗？')])
    keywords = StringField('关键词', validators=[DataRequired(), Length(max=120, message='由于系统限制，目前最多支持关键词长度为120字符。')])
    keywordsAlt = StringField('第二语言关键词', validators=[Length(max=120, message='由于系统限制，目前最多支持关键词长度为120字符。')])
    
    marginTop = DecimalField('上方页边距 (cm)', places=1, render_kw={"placeholder": "2.0"})
    marginBottom = DecimalField('下方页边距 (cm)', places=1, render_kw={"placeholder": "2.0"})
    marginLeft = DecimalField('左侧页边距 (cm)', places=1, render_kw={"placeholder": "2.0"})
    marginRight = DecimalField('右侧页边距 (cm)', places=1, render_kw={"placeholder": "2.0"})
    sectionTitleFont = SelectField('大标题字体', choices=[('tnr', 'Times New Roman'), ('helvetica', 'Helvetica'), ('arial', 'Arial'), ('st', '宋体'), ('ht', '黑体'), ('fs', '仿宋')])
    sectionTitleFontAlt = SelectField('第二语言大标题字体', choices=[('tnr', 'Times New Roman'), ('helvetica', 'Helvetica'), ('arial', 'Arial'), ('st', '宋体'), ('ht', '黑体'), ('fs', '仿宋')])
    titleFont = SelectField('正文标题字体', choices=[('tnr', 'Times New Roman'), ('helvetica', 'Helvetica'), ('arial', 'Arial'), ('st', '宋体'), ('ht', '黑体'), ('fs', '仿宋')])
    bodyFont = SelectField('正文字体', choices=[('tnr', 'Times New Roman'), ('helvetica', 'Helvetica'), ('arial', 'Arial'), ('st', '宋体'), ('ht', '黑体'), ('fs', '仿宋')])
    abstractFont = SelectField('摘要字体', choices=[('tnr', 'Times New Roman'), ('helvetica', 'Helvetica'), ('arial', 'Arial'), ('st', '宋体'), ('ht', '黑体'), ('fs', '仿宋')])
    abstractFontAlt = SelectField('第二语言摘要字体', choices=[('tnr', 'Times New Roman'), ('helvetica', 'Helvetica'), ('arial', 'Arial'), ('st', '宋体'), ('ht', '黑体'), ('fs', '仿宋')])
    imageCommentFont = SelectField('图片说明字体', choices=[('tnr', 'Times New Roman'), ('helvetica', 'Helvetica'), ('arial', 'Arial'), ('st', '宋体'), ('ht', '黑体'), ('fs', '仿宋')])
    noteFont = SelectField('脚注字体', choices=[('tnr', 'Times New Roman'), ('helvetica', 'Helvetica'), ('arial', 'Arial'), ('st', '宋体'), ('ht', '黑体'), ('fs', '仿宋')])
    bibliographyFont = SelectField('参考文献字体', choices=[('tnr', 'Times New Roman'), ('helvetica', 'Helvetica'), ('arial', 'Arial'), ('st', '宋体'), ('ht', '黑体'), ('fs', '仿宋')])
    bibliographyFontAlt = SelectField('第二语言参考文献字体', choices=[('tnr', 'Times New Roman'), ('helvetica', 'Helvetica'), ('arial', 'Arial'), ('st', '宋体'), ('ht', '黑体'), ('fs', '仿宋')])
    tocFont = SelectField('目录字体', choices=[('tnr', 'Times New Roman'), ('helvetica', 'Helvetica'), ('arial', 'Arial'), ('st', '宋体'), ('ht', '黑体'), ('fs', '仿宋')])
    innerCoverFont = SelectField('内封面字体', choices=[('tnr', 'Times New Roman'), ('helvetica', 'Helvetica'), ('arial', 'Arial'), ('st', '宋体'), ('ht', '黑体'), ('fs', '仿宋')])
    innerCoverFontAlt = SelectField('第二语言内封面字体', choices=[('tnr', 'Times New Roman'), ('helvetica', 'Helvetica'), ('arial', 'Arial'), ('st', '宋体'), ('ht', '黑体'), ('fs', '仿宋')])

    sectionTitleFontSize = DecimalField('大标题字号', places=0, render_kw={"placeholder": "16"})
    title1FontSize = DecimalField('章节标题字号', places=0, render_kw={"placeholder": "12"})
    title2FontSize = DecimalField('子章节标题字号', places=0, render_kw={"placeholder": "12"})
    title3FontSize = DecimalField('次级子章节标题字号', places=0, render_kw={"placeholder": "12"})
    bodyFontSize = DecimalField('正文字号', places=0, render_kw={"placeholder": "12"})
    abstractFontSize = DecimalField('摘要字号', places=0, render_kw={"placeholder": "12"})
    imageCommentFontSize = DecimalField('图片说明字号', places=0, render_kw={"placeholder": "12"})
    noteFontSize = DecimalField('脚注字号', places=0, render_kw={"placeholder": "9"})
    bibliographyFontSize = DecimalField('参考文献字号', places=0, render_kw={"placeholder": "10.5"})
    toc1FontSize = DecimalField('一级目录字号', places=0, render_kw={"placeholder": "12"})
    toc2FontSize = DecimalField('二级目录字号', places=0, render_kw={"placeholder": "12"})
    toc3FontSize = DecimalField('三级目录字号', places=0, render_kw={"placeholder": "12"})
    innerCoverFontSize = DecimalField('内封面字号', places=0, render_kw={"placeholder": "22"})

    sectionTitleLineSpacing = DecimalField('大标题行距 (倍数)', places=2, render_kw={"placeholder": "2"})
    title1LineSpacing = DecimalField('章节标题行距 (倍数)', places=2, render_kw={"placeholder": "1.5"})
    title2LineSpacing = DecimalField('子章节标题行距 (倍数)', places=2, render_kw={"placeholder": "1.5"})
    title3LineSpacing = DecimalField('次级子章节标题行距 (倍数)', places=2, render_kw={"placeholder": "1.5"})
    tocLineSpacing = DecimalField('目录行距 (倍数)', places=2, render_kw={"placeholder": "1.5"})
    bodyLineSpacing = DecimalField('正文行距 (倍数)', places=2, render_kw={"placeholder": "1.5"})
    abstractLineSpacing = DecimalField('摘要行距 (倍数)', places=2, render_kw={"placeholder": "1.5"})
    bibliographyLineSpacing = DecimalField('参考文献行距 (倍数)', places=2, render_kw={"placeholder": "1"})
    innerCoverLineSpacing = DecimalField('内封面行距 (倍数)', places=2, render_kw={"placeholder": "1.5"})
    
    title1AfterSpacing = DecimalField('章节标题段后距 (倍数)', places=2, render_kw={"placeholder": "0"})
    title2AfterSpacing = DecimalField('子章节标题段后距 (倍数)', places=2, render_kw={"placeholder": "0"})
    title3AfterSpacing = DecimalField('次级子章节标题段后距 (倍数)', places=2, render_kw={"placeholder": "0"})
    bodyAfterSpacing = DecimalField('正文段后距 (倍数)', places=2, render_kw={"placeholder": "0"})
    abstractAfterSpacing = DecimalField('摘要段后距 (倍数)', places=2, render_kw={"placeholder": "0"})
    bibliographyAfterSpacing = DecimalField('参考文献段后距 (倍数)', places=2, render_kw={"placeholder": "1"})
    toc1BeforeSpacing = DecimalField('一级目录段前距 (倍数)', places=2, render_kw={"placeholder": "0.75"})
    toc2BeforeSpacing = DecimalField('二级目录段前距 (倍数)', places=2, render_kw={"placeholder": "0"})
 
    title1Indent = DecimalField('章节标题缩进（字符）', places=0, render_kw={"placeholder": "0"})
    title2Indent = DecimalField('子章节标题缩进（字符）', places=0, render_kw={"placeholder": "0"})
    title3Indent = DecimalField('次级子章节标题缩进（字符）', places=0, render_kw={"placeholder": "0"})
    toc1Indent = DecimalField('一级目录缩进（字符）', places=0, render_kw={"placeholder": "0"})
    toc2Indent = DecimalField('二级目录缩进（字符）', places=0, render_kw={"placeholder": "2"})
    toc3Indent = DecimalField('三级目录缩进（字符）', places=0, render_kw={"placeholder": "4"})
    bodyFirstIndent = DecimalField('正文首行缩进（字符）', places=0, render_kw={"placeholder": "2"})
    abstractFirstIndent = DecimalField('摘要首行缩进（字符）', places=0, render_kw={"placeholder": "2"})
    bodyLeftIndent = DecimalField('正文左侧缩进（字符）', places=0, render_kw={"placeholder": "0"})
    abstractLeftIndent = DecimalField('摘要左侧缩进（字符）', places=0, render_kw={"placeholder": "0"})
    
    submit = SubmitField('新建论文')

    def validate_marginTop(self, marginTop):
        if marginTop.data > 5 or marginTop.data <= 0:
            raise ValidationError('上方页边距必须在0～5厘米之间。')
    def validate_marginBottom(self, marginBottom):
        if marginBottom.data > 5 or marginBottom.data <= 0:
            raise ValidationError('下方页边距必须在0～5厘米之间。')
    def validate_marginLeft(self, marginLeft):
        if marginLeft.data > 5 or marginLeft.data <= 0:
            raise ValidationError('左侧页边距必须在0～5厘米之间。')
    def validate_marginRight(self, marginRight):
        if marginRight.data > 5 or marginRight.data <= 0:
            raise ValidationError('右侧页边距必须在0～5厘米之间。')
    def validate_lineSpacing(self, lineSpacing):
        if lineSpacing.data > 2 or lineSpacing.data < 1:
            raise ValidationError('暂时仅支持1-2倍行距。')

class chapterContentForm(FlaskForm):
    title = StringField('章节标题', validators=[DataRequired(message='喂，虽然能编辑你也别不填啊……')])
    content = TextAreaField('章节内容', render_kw={"rows": "10"})
    tailContent = TextAreaField('章节尾部内容', render_kw={"rows": "10"})
    submit = SubmitField('确认修改')

class abstractForm(FlaskForm):
    abstract1 = TextAreaField('摘要1', render_kw={"rows": "10", "placeholder": "摘要1"})
    abstract2 = TextAreaField('摘要2', render_kw={"rows": "10", "placeholder": "摘要2"})
    toggle = BooleanField('双语摘要')
    submit = SubmitField('确认修改')