from datetime import datetime
from Genethesis import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    signature = db.Column(db.String(20), nullable=True)
    firstName = db.Column(db.String(60), nullable=True)
    lastName = db.Column(db.String(60), nullable=True)
    university = db.Column(db.String(120), nullable=True, default='某知名大学')
    faculty = db.Column(db.String(120), nullable=True, default='某杰出院系')
    grade = db.Column(db.String(120), nullable=True, default='某年级')
    selfIntro = db.Column(db.Text, nullable=True, default='随便写点什么？程序员只是想测试一下textfield。')
    timeCreated = db.Column(db.DateTime, nullable=False, default=datetime.now)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    articles = db.relationship('Article', backref='author', cascade="all,delete", lazy=True)

    def __repr__(self):
        if self.admin == True:
            return f"Admin user('{self.username}', with email '{self.email}', with image '{self.avatar}')"
        return f"User('{self.username}', with email '{self.email}', with image '{self.avatar}')"

    def completedArticles(self):
        completedArticles = []
        for article in self.articles:
            if article.status == True:
                completedArticles.append(article)
        return completedArticles

    def incompletedArticles(self):
        incompletedArticles = []
        for article in self.articles:
            if article.status == False:
                incompletedArticles.append(article)
        return incompletedArticles

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    language = db.Column(db.String(20), unique=False, nullable=False)
    status = db.Column(db.Boolean(), nullable=False, default=False)
    title = db.Column(db.String(120), unique=False, nullable=False)
    titleAlt = db.Column(db.String(120), unique=False, nullable=False)
    tutor = db.Column(db.String(60), unique=False, nullable=False)
    abstract1 = db.Column(db.Text, nullable=False)
    abstract2Toggle = db.Column(db.Boolean, nullable=False, default=True)
    abstract2 = db.Column(db.Text, nullable=True)
    introduction = db.Column(db.Text, unique=False, nullable=True)
    keywords = db.Column(db.String(120), unique=False, nullable=True)
    keywordsAlt = db.Column(db.String(120), unique=False, nullable=True)
    bibliography = db.Column(db.Text, unique=False, nullable=False)
    gratitude = db.Column(db.Text, unique=False, nullable=False)
    marginLeft = db.Column(db.Float(asdecimal=True), nullable=False, default=2)
    marginRight = db.Column(db.Float(asdecimal=True), nullable=False, default=2)
    marginTop = db.Column(db.Float(asdecimal=True), nullable=False, default=2)
    marginBottom = db.Column(db.Float(asdecimal=True), nullable=False, default=2)
    # Fonts
    sectionTitleFont = db.Column(db.String(30), nullable=False, default='tnr')
    sectionTitleFontAlt = db.Column(db.String(30), nullable=False, default='ht')
    titleFont = db.Column(db.String(30), nullable=False, default='tnr')
    bodyFont = db.Column(db.String(30), nullable=False, default='tnr')
    abstractFont = db.Column(db.String(30), nullable=False, default='tnr')
    abstractFontAlt = db.Column(db.String(30), nullable=False, default='st')
    imageCommentFont = db.Column(db.String(30), nullable=False, default='tnr')
    noteFont = db.Column(db.String(30), nullable=False, default='tnr')
    bibliographyFont = db.Column(db.String(30), nullable=False, default='tnr')
    bibliographyFontAlt = db.Column(db.String(30), nullable=False, default='st')
    tocFont = db.Column(db.String(30), nullable=False, default='tnr')
    innerCoverFont = db.Column(db.String(30), nullable=False, default='tnr')
    innerCoverFontAlt = db.Column(db.String(30), nullable=False, default='tnr')
    # Font Sizes
    sectionTitleFontSize = db.Column(db.Float(asdecimal=True), nullable=False, default=16)
    title1FontSize = db.Column(db.Float(asdecimal=True), nullable=False, default=12)
    title2FontSize = db.Column(db.Float(asdecimal=True), nullable=False, default=12)
    title3FontSize = db.Column(db.Float(asdecimal=True), nullable=False, default=12)
    bodyFontSize = db.Column(db.Float(asdecimal=True), nullable=False, default=12)
    abstractFontSize = db.Column(db.Float(asdecimal=True), nullable=False, default=12)
    imageCommentFontSize = db.Column(db.Float(asdecimal=True), nullable=False, default=12)
    noteFontSize = db.Column(db.Float(asdecimal=True), nullable=False, default=9)
    bibliographyFontSize = db.Column(db.Float(asdecimal=True), nullable=False, default=10.5)
    toc1FontSize = db.Column(db.Float(asdecimal=True), nullable=False, default=12)
    toc2FontSize = db.Column(db.Float(asdecimal=True), nullable=False, default=12)
    toc3FontSize = db.Column(db.Float(asdecimal=True), nullable=False, default=12)
    innerCoverFontSize = db.Column(db.Float(asdecimal=True), nullable=False, default=22)
    # Line Spacings
    sectionTitleLineSpacing = db.Column(db.Float(asdecimal=True), nullable=False, default=2)
    title1LineSpacing = db.Column(db.Float(asdecimal=True), nullable=False, default=1.5)
    title2LineSpacing = db.Column(db.Float(asdecimal=True), nullable=False, default=1.5)
    title3LineSpacing = db.Column(db.Float(asdecimal=True), nullable=False, default=1.5)
    tocLineSpacing = db.Column(db.Float(asdecimal=True), nullable=False, default=1.5)
    bodyLineSpacing = db.Column(db.Float(asdecimal=True), nullable=False, default=1.5)
    abstractLineSpacing = db.Column(db.Float(asdecimal=True), nullable=False, default=1.5)
    imageCommentLineSpacing = db.Column(db.Float(asdecimal=True), nullable=False, default=1)
    noteLineSpacing = db.Column(db.Float(asdecimal=True), nullable=False, default=1)
    bibliographyLineSpacing = db.Column(db.Float(asdecimal=True), nullable=False, default=1)
    innerCoverLineSpacing = db.Column(db.Float(asdecimal=True), nullable=False, default=1.5)
    # After and Before Spacings
    title1AfterSpacing = db.Column(db.Float(asdecimal=True), nullable=False, default=0)
    title2AfterSpacing = db.Column(db.Float(asdecimal=True), nullable=False, default=0)
    title3AfterSpacing = db.Column(db.Float(asdecimal=True), nullable=False, default=0)
    bodyAfterSpacing = db.Column(db.Float(asdecimal=True), nullable=False, default=0)
    abstractAfterSpacing = db.Column(db.Float(asdecimal=True), nullable=False, default=0)
    bibliographyAfterSpacing = db.Column(db.Float(asdecimal=True), nullable=False, default=1)
    toc1BeforeSpacing = db.Column(db.Float(asdecimal=True), nullable=False, default=0.75)
    toc2BeforeSpacing = db.Column(db.Float(asdecimal=True), nullable=False, default=0)
    # Indents
    title1Indent = db.Column(db.Float(asdecimal=True), nullable=False, default=0)
    title2Indent = db.Column(db.Float(asdecimal=True), nullable=False, default=0)
    title3Indent = db.Column(db.Float(asdecimal=True), nullable=False, default=0)
    toc1Indent = db.Column(db.Float(asdecimal=True), nullable=False, default=0)
    toc2Indent = db.Column(db.Float(asdecimal=True), nullable=False, default=2)
    toc3Indent = db.Column(db.Float(asdecimal=True), nullable=False, default=4)
    bodyFirstIndent = db.Column(db.Float(asdecimal=True), nullable=False, default=2)
    abstractFirstIndent = db.Column(db.Float(asdecimal=True), nullable=False, default=2)
    bodyLeftIndent = db.Column(db.Float(asdecimal=True), nullable=False, default=0)
    abstractLeftIndent = db.Column(db.Float(asdecimal=True), nullable=False, default=0)
    timeCreated = db.Column(db.DateTime, nullable=False, default=datetime.now)
    timeEdited = db.Column(db.DateTime, nullable=False, default=datetime.now)
    chapters = db.relationship('Chapter', backref='mainArticle', cascade="all,delete", lazy=True)

    #def __repr__(self):
        #return f"标题{self.title}，来自用户{self.author.username}"

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    articleID = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    chapterNumber = db.Column(db.Integer, unique=False, nullable=False)
    title = db.Column(db.String(120), unique=False, nullable=False)
    content = db.Column(db.Text, nullable=True)
    tailContent = db.Column(db.Text, nullable=True)
    subChapters = db.relationship('subChapter', backref='mainChapter', cascade="all,delete", lazy=True)
    timeEdited = db.Column(db.DateTime, nullable=False, default=datetime.now)

    #def __repr__(self):
        #return f"标题{self.title}，是标题为{self.mainArticle.title}的论文的第{self.chapterNumber}章节。"

class subChapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapterID = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    subChapterNumber = db.Column(db.Integer, unique=False, nullable=False)
    title = db.Column(db.String(120), unique=False, nullable=False)
    content = db.Column(db.Text, nullable=True)
    tailContent = db.Column(db.Text, nullable=True)
    scSubChapters = db.relationship('scSubChapter', backref='mainSubChapter', cascade="all,delete", lazy=True)
    timeEdited = db.Column(db.DateTime, nullable=False, default=datetime.now)

    #def __repr__(self):
        #return f"标题{self.title}，是标题为{self.mainChapter.mainArticle.title}的论文的第{self.mainChapter.chapterNumber}章节的第{self.subChapterNumber}子章节。"

class scSubChapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subChapterID = db.Column(db.Integer, db.ForeignKey('sub_chapter.id'), nullable=False)
    scSubChapterNumber = db.Column(db.Integer, unique=False, nullable=False)
    title = db.Column(db.String(120), unique=False, nullable=False)
    content = db.Column(db.Text, nullable=False)
    timeEdited = db.Column(db.DateTime, nullable=False, default=datetime.now)

    #def __repr__(self):
        #return f"标题{self.title}，是标题为{self.mainSubChapter.mainChapter.mainArticle.title}的论文的第{self.mainSubChapter.mainChapter.chapterNumber}章节的第{self.mainSubChapter.subChapterNumber}子章节的{self.scSubChapterNumber}次级章节。"