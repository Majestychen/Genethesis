import os
import re
import json
import shutil
import requests
import time
from datetime import datetime
from flask import Blueprint, render_template, url_for, redirect, flash, request, send_from_directory
from flask_login import current_user, login_required
from Genethesis import db, app
from Genethesis.articles.forms import newArticleForm, chapterContentForm, abstractForm
from Genethesis.models import Article, Chapter, subChapter, scSubChapter

articles = Blueprint('articles', __name__)

@app.template_filter('getHTML')
def get_html_form(text):
    if text == '':
        return '暂时还没有内容呢～'
    text = re.sub(r'{{bold&italic&underline:([^}}]+)}}', r'<strong><em><u>\1</u></em></strong>', text)
    text = re.sub(r'{{bold&italic:([^}}]+)}}', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'{{italic&underline:([^}}]+)}}', r'<em><u>\1</u></em>', text)
    text = re.sub(r'{{bold&underline:([^}}]+)}}', r'<strong><u>\1</u></strong>', text)
    text = re.sub(r'{{bold:([^}}]+)}}', r'<strong>\1</strong>', text)
    text = re.sub(r'{{italic:([^}}]+)}}', r'<em>\1</em>', text)
    text = re.sub(r'{{underline:([^}}]+)}}', r'<u>\1</u>', text)
    text = re.sub(r'{{footnoteAnchor:([^,]+), footnoteContent:([^}}]+)}}', r'<span class="text-primary">\1</span>', text)
    text = re.sub(r'{{ImageAnchor:([^}}]+)}}', '', text)
    return text

@app.template_filter('getRaw')
def get_raw_form(text):
    text = re.sub(r'{{bold&italic&underline:([^}}]+)}}', r'\1', text)
    text = re.sub(r'{{bold&italic:([^}}]+)}}', r'\1', text)
    text = re.sub(r'{{italic&underline:([^}}]+)}}', r'\1', text)
    text = re.sub(r'{{bold&underline:([^}}]+)}}', r'\1', text)
    text = re.sub(r'{{bold:([^}}]+)}}', r'\1', text)
    text = re.sub(r'{{italic:([^}}]+)}}', r'\1', text)
    text = re.sub(r'{{underline:([^}}]+)}}', r'\1', text)
    text = re.sub(r'{{footnoteAnchor:([^,]+), footnoteContent:([^}}]+)}}', r'\1', text)
    text = re.sub(r'{{ImageAnchor:([^}}]+)}}\n', '', text)
    return text

@app.template_filter('getRawCountWithClass')
def get_raw_count(text):
    if text == '':
        return 0
    text = get_raw_form(text)
    if re.match(r'[a-zA-Z]', text[0]):
        return str(len(text.split()))+'个单词'
    else:
        return str(len(text))+'个字'

@app.template_filter('getRawCount')
def get_raw_count(text):
    text = re.sub(r'{{bold&italic&underline:([^}}]+)}}', r'\1', text)
    text = re.sub(r'{{bold&italic:([^}}]+)}}', r'\1', text)
    text = re.sub(r'{{italic&underline:([^}}]+)}}', r'\1', text)
    text = re.sub(r'{{bold&underline:([^}}]+)}}', r'\1', text)
    text = re.sub(r'{{bold:([^}}]+)}}', r'\1', text)
    text = re.sub(r'{{italic:([^}}]+)}}', r'\1', text)
    text = re.sub(r'{{underline:([^}}]+)}}', r'\1', text)
    text = re.sub(r'{{footnoteAnchor:([^,]+), footnoteContent:([^}}]+)}}', r'\1', text)
    text = re.sub(r'{{ImageAnchor:([^}}]+)}}', '', text)
    if text == '':
        return 0
    if re.match(r'[a-zA-Z]', text[0]):
        return len(text.split())
    else:
        return len(text)

@app.template_filter('getWordCount')
def get_word_count(chapter):
    totalCount = 0
    totalCount = totalCount + get_raw_count(chapter.content)
    for subchapter in chapter.subChapters:
        totalCount = totalCount + get_raw_count(subchapter.content)
        for scsubchapter in subchapter.scSubChapters:
            totalCount = totalCount + get_raw_count(scsubchapter.content)
        if subchapter.tailContent:
            totalCount = totalCount + get_raw_count(subchapter.tailContent)
    if chapter.tailContent:
        totalCount = totalCount + get_raw_count(chapter.tailContent)
    return totalCount

@app.template_filter('getLineCount')
def get_line_count(text):
    if text == '':
        return 0
    return len(text.split('\n'))

@articles.route('/articles')
@login_required
def main_list():
    articles = Article.query.filter_by(userID=current_user.id)
    return render_template('articles_list.html', section='我的论文', title='我的论文列表', articles=articles)

@articles.route('/articles/new', methods=['GET', 'POST'])
@login_required
def new():
    form = newArticleForm()
    if form.validate_on_submit():
        if Article.query.filter_by(userID=current_user.id, title=form.title.data).count() == 0:
            article = Article(userID=current_user.id, language=form.language.data, \
            title=form.title.data, titleAlt=form.titleAlt.data, \
            tutor=form.tutor.data, keywords=form.keywords.data, \
            keywordsAlt=form.keywordsAlt.data,
            sectionTitleFont=form.sectionTitleFont.data, \
            sectionTitleFontAlt=form.sectionTitleFontAlt.data, \
            titleFont=form.titleFont.data, \
            bodyFont=form.bodyFont.data, \
            abstractFont=form.abstractFont.data, \
            abstractFontAlt=form.abstractFontAlt.data, \
            imageCommentFont=form.imageCommentFont.data, \
            noteFont=form.noteFont.data, \
            bibliographyFont=form.bibliographyFont.data, \
            bibliographyFontAlt=form.bibliographyFontAlt.data, \
            tocFont=form.tocFont.data, \
            innerCoverFont=form.innerCoverFont.data, \
            innerCoverFontAlt=form.innerCoverFontAlt.data, \
            sectionTitleFontSize=form.sectionTitleFontSize.data, \
            title1FontSize=form.title1FontSize.data, \
            title2FontSize=form.title2FontSize.data, \
            title3FontSize=form.title3FontSize.data, \
            bodyFontSize=form.bodyFontSize.data, \
            abstractFontSize=form.abstractFontSize.data, \
            imageCommentFontSize=form.imageCommentFontSize.data, \
            noteFontSize=form.noteFontSize.data, \
            bibliographyFontSize=form.bibliographyFontSize.data, \
            toc1FontSize=form.toc1FontSize.data, \
            toc2FontSize=form.toc2FontSize.data, \
            toc3FontSize=form.toc3FontSize.data, \
            innerCoverFontSize=form.innerCoverFontSize.data, \
            sectionTitleLineSpacing=form.sectionTitleLineSpacing.data, \
            title1LineSpacing=form.title1LineSpacing.data, \
            title2LineSpacing=form.title2LineSpacing.data, \
            title3LineSpacing=form.title3LineSpacing.data, \
            tocLineSpacing=form.tocLineSpacing.data, \
            bodyLineSpacing=form.bodyLineSpacing.data, \
            abstractLineSpacing=form.abstractLineSpacing.data, \
            bibliographyLineSpacing=form.bibliographyLineSpacing.data, \
            innerCoverLineSpacing=form.innerCoverLineSpacing.data, \
            title1AfterSpacing=form.title1AfterSpacing.data, \
            title2AfterSpacing=form.title2AfterSpacing.data, \
            title3AfterSpacing=form.title3AfterSpacing.data, \
            bodyAfterSpacing=form.bodyAfterSpacing.data, \
            abstractAfterSpacing=form.abstractAfterSpacing.data, \
            bibliographyAfterSpacing=form.bibliographyAfterSpacing.data, \
            toc1BeforeSpacing=form.toc1BeforeSpacing.data, \
            toc2BeforeSpacing=form.toc2BeforeSpacing.data, \
            title1Indent=form.title1Indent.data, \
            title2Indent=form.title2Indent.data, \
            title3Indent=form.title3Indent.data, \
            toc1Indent=form.toc1Indent.data, \
            toc2Indent=form.toc2Indent.data, \
            toc3Indent=form.toc3Indent.data, \
            bodyFirstIndent=form.bodyFirstIndent.data, \
            abstractFirstIndent=form.abstractFirstIndent.data, \
            bodyLeftIndent=form.bodyLeftIndent.data, \
            abstractLeftIndent=form.abstractLeftIndent.data, \
            marginTop=form.marginTop.data, marginBottom=form.marginBottom.data, \
            marginLeft=form.marginLeft.data, marginRight=form.marginRight.data, \
            abstract1='', abstract2Toggle=True, abstract2='', \
            introduction='', bibliography='', gratitude='')
            db.session.add(article)
            db.session.commit()
            articleEntry = Article.query.filter_by(userID=current_user.id, title=article.title).first()
            articleDic = os.path.join(app.root_path, 'static/articles', str(current_user.id), str(articleEntry.id))
            if not os.path.exists(articleDic):
                os.mkdir(articleDic)
            flash(f'您的论文 {form.title.data} 已经成功添加。', 'success')
            return redirect(url_for('articles.main_list'))
        else:
            form.title.errors.append('您已经有一篇同名的论文了。')
    elif request.method == 'GET':
        form.marginTop.data = 2
        form.marginBottom.data = 2.5
        form.marginLeft.data = 3
        form.marginRight.data = 2.5
        form.sectionTitleFont.data = 'ht'
        form.sectionTitleFontAlt.data = 'tnr'
        form.titleFont.data = 'st'

        form.bodyFont.data = 'st'
        form.abstractFont.data = 'st'
        form.abstractFontAlt.data = 'tnr'
        form.imageCommentFont.data = 'ht'
        form.noteFont.data = 'st'
        form.bibliographyFont.data = 'st'
        form.bibliographyFontAlt.data = 'tnr'
        form.tocFont.data = 'st'
        form.innerCoverFont.data = 'st'
        form.innerCoverFontAlt.data = 'tnr'

        form.sectionTitleFontSize.data = 16
        form.title1FontSize.data = 12
        form.title2FontSize.data = 12
        form.title3FontSize.data = 12
        form.bodyFontSize.data = 12
        form.abstractFontSize.data = 12
        form.imageCommentFontSize.data = 12
        form.noteFontSize.data = 9
        form.bibliographyFontSize.data = 10.5
        form.toc1FontSize.data = 12
        form.toc2FontSize.data = 12
        form.toc3FontSize.data = 12
        form.innerCoverFontSize.data = 22

        form.sectionTitleLineSpacing.data = 2
        form.title1LineSpacing.data = 1.5
        form.title2LineSpacing.data = 1.5
        form.title3LineSpacing.data = 1.5
        form.tocLineSpacing.data = 1.5
        form.bodyLineSpacing.data = 1.5
        form.abstractLineSpacing.data = 1.5
        form.bibliographyLineSpacing.data = 1
        form.innerCoverLineSpacing.data = 1.5

        form.title1AfterSpacing.data = 0
        form.title2AfterSpacing.data = 0
        form.title3AfterSpacing.data = 0
        form.bodyAfterSpacing.data = 0
        form.abstractAfterSpacing.data = 0
        form.bibliographyAfterSpacing.data = 1
        form.toc1BeforeSpacing.data = 0.75
        form.toc2BeforeSpacing.data = 0

        form.title1Indent.data = 0
        form.title2Indent.data = 0
        form.title3Indent.data = 0
        form.toc1Indent.data = 0
        form.toc2Indent.data = 2
        form.toc3Indent.data = 4
        form.bodyFirstIndent.data = 2
        form.abstractFirstIndent.data = 2
        form.bodyLeftIndent.data = 0
        form.abstractLeftIndent.data = 0

    return render_template('articles_edit_settings.html', section='我的论文', title='新建论文', form=form)

@articles.route('/articles/edit_settings/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_settings(article_id):
    form = newArticleForm()
    article = Article.query.get_or_404(article_id)
    if form.validate_on_submit():
        if Article.query.filter_by(userID=current_user.id, title=form.title.data).count() == 0 or Article.query.filter_by(userID=current_user.id, title=form.title.data).first().id == article_id:
            article.title = form.title.data
            article.titleAlt = form.titleAlt.data
            article.tutor = form.tutor.data
            article.language = form.language.data
            article.keywords = form.keywords.data
            article.keywordsAlt = form.keywordsAlt.data
            article.sectionTitleFont = form.sectionTitleFont.data
            article.sectionTitleFontAlt = form.sectionTitleFontAlt.data
            article.titleFont = form.titleFont.data
            article.bodyFont = form.bodyFont.data
            article.abstractFont = form.abstractFont.data
            article.abstractFontAlt = form.abstractFontAlt.data
            article.imageCommentFont = form.imageCommentFont.data
            article.noteFont = form.noteFont.data
            article.bibliographyFont = form.bibliographyFont.data
            article.bibliographyFontAlt = form.bibliographyFontAlt.data
            article.tocFont = form.tocFont.data
            article.innerCoverFont = form.innerCoverFont.data
            article.innerCoverFontAlt = form.innerCoverFontAlt.data
            article.sectionTitleFontSize = form.sectionTitleFontSize.data
            article.title1FontSize = form.title1FontSize.data
            article.title2FontSize = form.title2FontSize.data
            article.title3FontSize = form.title3FontSize.data
            article.bodyFontSize = form.bodyFontSize.data
            article.abstractFontSize = form.abstractFontSize.data
            article.imageCommentFontSize = form.imageCommentFontSize.data
            article.noteFontSize = form.noteFontSize.data
            article.bibliographyFontSize = form.bibliographyFontSize.data
            article.toc1FontSize = form.toc1FontSize.data
            article.toc2FontSize = form.toc2FontSize.data
            article.toc3FontSize = form.toc3FontSize.data
            article.innerCoverFontSize = form.innerCoverFontSize.data
            article.sectionTitleLineSpacing = form.sectionTitleLineSpacing.data
            article.title1LineSpacing = form.title1LineSpacing.data
            article.title2LineSpacing = form.title2LineSpacing.data
            article.title3LineSpacing = form.title3LineSpacing.data
            article.tocLineSpacing = form.tocLineSpacing.data
            article.bodyLineSpacing = form.bodyLineSpacing.data
            article.abstractLineSpacing = form.abstractLineSpacing.data
            article.bibliographyLineSpacing = form.bibliographyLineSpacing.data
            article.innerCoverLineSpacing = form.innerCoverLineSpacing.data
            article.title1AfterSpacing = form.title1AfterSpacing.data
            article.title2AfterSpacing = form.title2AfterSpacing.data
            article.title3AfterSpacing = form.title3AfterSpacing.data
            article.bodyAfterSpacing = form.bodyAfterSpacing.data
            article.abstractAfterSpacing = form.abstractAfterSpacing.data
            article.bibliographyAfterSpacing = form.bibliographyAfterSpacing.data
            article.toc1BeforeSpacing = form.toc1BeforeSpacing.data
            article.toc2BeforeSpacing = form.toc2BeforeSpacing.data
            article.title1Indent = form.title1Indent.data
            article.title2Indent = form.title2Indent.data
            article.title3Indent = form.title3Indent.data
            article.toc1Indent = form.toc1Indent.data
            article.toc2Indent = form.toc2Indent.data
            article.toc3Indent = form.toc3Indent.data
            article.bodyFirstIndent = form.bodyFirstIndent.data
            article.abstractFirstIndent = form.abstractFirstIndent.data
            article.bodyLeftIndent = form.bodyLeftIndent.data
            article.abstractLeftIndent = form.abstractLeftIndent.data
            article.marginTop = form.marginTop.data
            article.marginBottom = form.marginBottom.data
            article.marginLeft = form.marginLeft.data
            article.marginRight = form.marginRight.data
            article.timeEdited = datetime.now()
            db.session.commit()
            flash(f'您的论文 {form.title.data} 的设置已经成功更新。', 'success')
            return redirect(url_for('articles.main_list'))
        else:
            form.title.errors.append('您已经有一篇同名的论文了。')
    elif request.method == 'GET':
        form.title.data = article.title
        form.titleAlt.data = article.titleAlt
        form.tutor.data = article.tutor
        form.language.data = article.language
        form.keywords.data = article.keywords
        form.keywordsAlt.data = article.keywordsAlt
        form.sectionTitleFont.data = article.sectionTitleFont
        form.sectionTitleFontAlt.data = article.sectionTitleFontAlt
        form.titleFont.data = article.titleFont
        form.bodyFont.data = article.bodyFont
        form.abstractFont.data = article.abstractFont
        form.abstractFontAlt.data = article.abstractFontAlt
        form.imageCommentFont.data = article.imageCommentFont
        form.noteFont.data = article.noteFont
        form.bibliographyFont.data = article.bibliographyFont
        form.bibliographyFontAlt.data = article.bibliographyFontAlt
        form.tocFont.data = article.tocFont
        form.innerCoverFont.data = article.innerCoverFont
        form.innerCoverFontAlt.data = article.innerCoverFontAlt
        form.sectionTitleFontSize.data = article.sectionTitleFontSize
        form.title1FontSize.data = article.title1FontSize
        form.title2FontSize.data = article.title2FontSize
        form.title3FontSize.data = article.title3FontSize
        form.bodyFontSize.data = article.bodyFontSize
        form.abstractFontSize.data = article.abstractFontSize
        form.imageCommentFontSize.data = article.imageCommentFontSize
        form.noteFontSize.data = article.noteFontSize
        form.bibliographyFontSize.data = article.bibliographyFontSize
        form.toc1FontSize.data = article.toc1FontSize
        form.toc2FontSize.data = article.toc2FontSize
        form.toc3FontSize.data = article.toc3FontSize
        form.innerCoverFontSize.data = article.innerCoverFontSize
        form.sectionTitleLineSpacing.data = article.sectionTitleLineSpacing
        form.title1LineSpacing.data = article.title1LineSpacing
        form.title2LineSpacing.data = article.title2LineSpacing
        form.title3LineSpacing.data = article.title3LineSpacing
        form.tocLineSpacing.data = article.tocLineSpacing
        form.bodyLineSpacing.data = article.bodyLineSpacing
        form.abstractLineSpacing.data = article.abstractLineSpacing
        form.bibliographyLineSpacing.data = article.bibliographyLineSpacing
        form.innerCoverLineSpacing.data = article.innerCoverLineSpacing
        form.title1AfterSpacing.data = article.title1AfterSpacing
        form.title2AfterSpacing.data = article.title2AfterSpacing
        form.title3AfterSpacing.data = article.title3AfterSpacing
        form.bodyAfterSpacing.data = article.bodyAfterSpacing
        form.abstractAfterSpacing.data = article.abstractAfterSpacing
        form.bibliographyAfterSpacing.data = article.bibliographyAfterSpacing
        form.toc1BeforeSpacing.data = article.toc1BeforeSpacing
        form.toc2BeforeSpacing.data = article.toc2BeforeSpacing
        form.title1Indent.data = article.title1Indent
        form.title2Indent.data = article.title2Indent
        form.title3Indent.data = article.title3Indent
        form.toc1Indent.data = article.toc1Indent
        form.toc2Indent.data = article.toc2Indent
        form.toc3Indent.data = article.toc3Indent
        form.bodyFirstIndent.data = article.bodyFirstIndent
        form.abstractFirstIndent.data = article.abstractFirstIndent
        form.bodyLeftIndent.data = article.bodyLeftIndent
        form.abstractLeftIndent.data = article.abstractLeftIndent
        form.marginTop.data = article.marginTop
        form.marginBottom.data = article.marginBottom
        form.marginLeft.data = article.marginLeft
        form.marginRight.data = article.marginRight
    return render_template('articles_edit_settings.html', section='我的论文', title='论文设置', form=form)

@articles.route('/articles/<int:article_id>')
@login_required
def single_article(article_id):
    article = Article.query.get_or_404(article_id)
    if article.status == True:
        flash(f'这篇论文已经完成了，无法再更改了哦～后悔了的话请打自己一巴掌然后点按论文下载按钮左侧的棒槌按钮。', 'danger')
        return redirect(url_for('articles.main_list'))
    order_file = os.path.join(app.root_path, 'static/articles', str(current_user.id), str(article_id), 'order.json')
    if not os.path.exists(order_file):
        return redirect(url_for('articles.inicialize', article_id=article_id))
    return render_template('articles_cards.html', section='我的论文', title=article.title, article=article)

@articles.route('/articles/inicialize/<int:article_id>', methods=['GET', 'POST'])
@login_required
def inicialize(article_id):
    article = Article.query.get_or_404(article_id)
    articleDic = os.path.join(app.root_path, 'static/articles', str(current_user.id), str(article_id))
    orderFile = os.path.join(app.root_path, 'static/articles', str(current_user.id), str(article_id), 'order.json')
    if request.method == 'POST':
        init = request.get_json()
        open(orderFile, 'a').close()
        with open(orderFile, 'w') as output:  
            json.dump(init, output)

        for chapter in init['chapters']:
            newChapter = Chapter(articleID=article_id, chapterNumber=chapter['chapterNumber'], title=chapter['title'], content='', tailContent='')
            db.session.add(newChapter)
        db.session.commit()

        for chapter in init['chapters']:
            for subchapter in chapter['subChapters']:
                mainChapter = Chapter.query.filter_by(articleID=article_id, chapterNumber=subchapter['chapterNumber']).first()
                newSubchapter = subChapter(chapterID=mainChapter.id, subChapterNumber=subchapter['subChapterNumber'], title=subchapter['title'], content='', tailContent='')
                db.session.add(newSubchapter)
        db.session.commit()

        for chapter in init['chapters']:
            for subchapter in chapter['subChapters']:
                for scsubchapter in subchapter['scSubChapters']:
                    mainChapter = Chapter.query.filter_by(articleID=article_id, chapterNumber=scsubchapter['chapterNumber']).first()
                    mainSubchapter = subChapter.query.filter_by(chapterID=mainChapter.id, subChapterNumber=scsubchapter['subChapterNumber']).first()
                    newScsubchapter = scSubChapter(subChapterID=mainSubchapter.id, scSubChapterNumber=scsubchapter['scSubChapterNumber'], title=scsubchapter['title'], content='')
                    db.session.add(newScsubchapter)
        db.session.commit()

        flash(f'您的论文大纲已经完成初始化，可以开始卡片式撰写了。', 'success')
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    if os.path.exists(orderFile):
        flash('该论文大纲已经确认，如果内测阶段尚未开放卡片增减功能，请新建论文。', 'danger')
        return redirect(url_for('articles.main_list'))
    if not os.path.exists(articleDic):
        os.mkdir(articleDic)
    return render_template('articles_inicialize.html', section='我的论文', title='论文大纲设置', article_id=article_id)

@articles.route('/articles/<int:article_id>/chapters/new', methods=['POST'])
@login_required
def add_chapter(article_id):
    chapter = Chapter(articleID=article_id, chapterNumber=request.get_json()['chapterNumber'], title=request.get_json()['chapterTitle'], content='')
    db.session.add(chapter)
    db.session.commit()
    return 'success'

@articles.route('/articles/<int:article_id>/chapters/<int:chapter_number>/subchapters/new', methods=['POST'])
@login_required
def add_subchapter(article_id, chapter_number):
    chapter = Chapter.query.filter_by(articleID=article_id, chapterNumber=chapter_number).first()
    subchapter = subChapter(chapterID=chapter.id, subChapterNumber=request.get_json()['subChapterNumber'], title=request.get_json()['subChapterTitle'], content='')
    db.session.add(subchapter)
    db.session.commit()
    return 'success'

@articles.route('/articles/<int:article_id>/chapters/<int:chapter_number>/subchapters/<int:subchapter_number>/scsubchapters/new', methods=['POST'])
@login_required
def add_scsubchapter(article_id, chapter_number, subchapter_number):
    chapter = Chapter.query.filter_by(articleID=article_id, chapterNumber=chapter_number).first()
    subchapter = subChapter.query.filter_by(chapterID=chapter.id, subChapterNumber=subchapter_number).first()
    scsubchapter = scSubChapter(subChapterID=subchapter.id, scSubChapterNumber=request.get_json()['scSubChapterNumber'], title=request.get_json()['scSubChapterTitle'], content='')
    db.session.add(scsubchapter)
    db.session.commit()
    return 'success'

@articles.route('/articles/<int:article_id>/index')
@login_required
def view_index(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('articles_view_index.html', section='我的论文', title='论文目录浏览（开发用）', article=article)

@articles.route('/chapters/<int:chapter_id>', methods=['GET', 'POST'])
@login_required
def edit_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    form = chapterContentForm()
    if form.validate_on_submit():
        chapter.title = form.title.data
        chapter.content = ''.join(L + '\n' for L in form.content.data.split('\r\n') if L)[:-1]
        chapter.tailContent = ''.join(L + '\n' for L in form.tailContent.data.split('\r\n') if L)[:-1]
        db.session.commit()
        flash('章节内容修改成功。', 'success')
        return redirect(url_for('articles.single_article', article_id=chapter.mainArticle.id))
    elif request.method == 'GET':
        form.title.data = chapter.title
        if chapter.content != 'Null':
            form.content.data = chapter.content
        if chapter.tailContent != 'Null':
            form.tailContent.data = chapter.tailContent
    return render_template('articles_edit_chapter.html', section='我的论文', title=chapter.title, object=chapter, article=chapter.mainArticle, form=form)

@articles.route('/subchapters/<int:subchapter_id>', methods=['GET', 'POST'])
@login_required
def edit_subchapter(subchapter_id):
    subchapter = subChapter.query.get_or_404(subchapter_id)
    form = chapterContentForm()
    if form.validate_on_submit():
        subchapter.title = form.title.data
        subchapter.content = ''.join(L + '\n' for L in form.content.data.split('\r\n') if L)[:-1]
        subchapter.tailContent = ''.join(L + '\n' for L in form.tailContent.data.split('\r\n') if L)[:-1]
        db.session.commit()
        flash('子章节内容修改成功。', 'success')
        return redirect(url_for('articles.single_article', article_id=subchapter.mainChapter.mainArticle.id))
    elif request.method == 'GET':
        form.title.data = subchapter.title
        if subchapter.content != 'Null':
            form.content.data = subchapter.content
        if subchapter.tailContent != 'Null':
            form.tailContent.data = subchapter.tailContent
    return render_template('articles_edit_chapter.html', section='我的论文', title=subchapter.title, article=subchapter.mainChapter.mainArticle, object=subchapter, form=form)

@articles.route('/scsubchapters/<int:scsubchapter_id>', methods=['GET', 'POST'])
@login_required
def edit_scsubchapter(scsubchapter_id):
    scsubchapter = scSubChapter.query.get_or_404(scsubchapter_id)
    form = chapterContentForm()
    if form.validate_on_submit():
        scsubchapter.title = form.title.data
        scsubchapter.content = ''.join(L + '\n' for L in form.content.data.split('\r\n') if L)[:-1]
        db.session.commit()
        flash('次级子章节内容修改成功。', 'success')
        return redirect(url_for('articles.single_article', article_id=scsubchapter.mainSubChapter.mainChapter.mainArticle.id))
    elif request.method == 'GET':
        form.title.data = scsubchapter.title
        if scsubchapter.content != 'Null':
            form.content.data = scsubchapter.content
    return render_template('articles_edit_chapter.html', section='我的论文', title=scsubchapter.title, article=scsubchapter.mainSubChapter.mainChapter.mainArticle, object=scsubchapter, form=form)

@articles.route('/articles/<int:article_id>/abstract', methods=['GET', 'POST'])
@login_required
def edit_abstract(article_id):
    article = Article.query.get_or_404(article_id)
    form = abstractForm()
    if form.validate_on_submit():
        article.abstract1 = ''.join(L + '\n' for L in form.abstract1.data.split('\r\n') if L)[:-1]
        article.abstract2Toggle = form.toggle.data
        if article.abstract2Toggle:
            article.abstract2 = ''.join(L + '\n' for L in form.abstract2.data.split('\r\n') if L)[:-1]
        else:
            article.abstract2 = 'Null'
        db.session.commit()
        flash('摘要修改成功。', 'success')
        return redirect(url_for('articles.single_article', article_id=article.id))
    elif request.method == 'GET':
        form.toggle.data = article.abstract2Toggle
        if article.abstract1 != 'Null':
            form.abstract1.data = article.abstract1
        if article.abstract2 != 'Null':
            form.abstract2.data = article.abstract2
    return render_template('articles_edit_abstract.html', section='我的论文', title='摘要' + article.title, article=article, form=form)


@articles.route('/articles/<int:article_id>/introduction', methods=['GET', 'POST'])
@login_required
def edit_introduction(article_id):
    article = Article.query.get_or_404(article_id)
    form = chapterContentForm()
    if form.validate_on_submit():
        article.introduction = ''.join(L + '\n' for L in form.content.data.split('\r\n') if L)[:-1]
        db.session.commit()
        flash('引入修改成功。', 'success')
        return redirect(url_for('articles.single_article', article_id=article.id))
    elif request.method == 'GET':
        if article.introduction != 'Null':
            form.content.data = article.introduction
    return render_template('articles_edit_chapter.html', section='我的论文', title='引入' + article.title, object={'title': '引入', 'titleInput': False}, article=article, form=form)

@articles.route('/articles/<int:article_id>/bibliography', methods=['GET', 'POST'])
@login_required
def edit_bibliography(article_id):
    article = Article.query.get_or_404(article_id)
    form = chapterContentForm()
    if form.validate_on_submit():
        article.bibliography = ''.join(L + '\n' for L in form.content.data.split('\r\n') if L)[:-1]
        db.session.commit()
        flash('参考书目修改成功。', 'success')
        return redirect(url_for('articles.single_article', article_id=article.id))
    elif request.method == 'GET':
        if article.bibliography != 'Null':
            form.content.data = article.bibliography
    return render_template('articles_edit_bibliography.html', section='我的论文', title='参考文献' + article.title, article=article, form=form)

@articles.route('/articles/<int:article_id>/gratitude', methods=['GET', 'POST'])
@login_required
def edit_gratitude(article_id):
    article = Article.query.get_or_404(article_id)
    form = chapterContentForm()
    if form.validate_on_submit():
        article.gratitude = ''.join(L + '\n' for L in form.content.data.split('\r\n') if L)[:-1]
        db.session.commit()
        flash('致谢辞修改成功。', 'success')
        return redirect(url_for('articles.single_article', article_id=article.id))
    elif request.method == 'GET':
        if article.gratitude != 'Null':
            form.content.data = article.gratitude
    return render_template('articles_edit_chapter.html', section='我的论文', title='致谢' + article.title, object={'title': '致谢辞', 'titleInput': False}, article=article, form=form)


@articles.route('/articles/finalize/<int:article_id>')
@login_required
def finalize(article_id):
    article = Article.query.get_or_404(article_id)
    orderFile = os.path.join(app.root_path, 'static/articles', str(current_user.id), str(article_id), 'order.json')
    if not os.path.exists(orderFile):
        flash('真的吗，一个字都还没写就完成了？', 'warning')
        return redirect(url_for('articles.main_list'))
    fn = os.path.join(app.root_path, 'static/articles', str(current_user.id), str(article_id), 'thesis.docx')
    if os.path.exists(fn):
        os.remove(fn)
    r = requests.get('http://localhost:3000/test/docx/'+str(article.id))
    while not os.path.exists(fn):
        time.sleep(1)
    article.status = True
    db.session.commit()
    flash(f'您的论文 {article.title} 已经确认完成，可以下载最终稿。', 'success')
    return redirect(url_for('articles.main_list'))

@articles.route('/articles/revitalize/<int:article_id>')
@login_required
def revitalize(article_id):
    article = Article.query.get_or_404(article_id)
    article.status = False
    db.session.commit()
    flash(f'您的论文 {article.title} 又可以编辑了，是不是很神奇。', 'success')
    return redirect(url_for('articles.main_list'))

@articles.route('/articles/<int:article_id>/delete')
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    path = os.path.join(app.root_path, 'static/articles', str(current_user.id), str(article_id))
    shutil.rmtree(path)
    flash(f'您的论文 {article.title} 的所有信息已经删除，感谢您的使用。', 'success')
    return redirect(url_for('articles.main_list'))


@articles.route('/articles/<int:article_id>/download', methods=['GET','POST'])
@login_required
def download(article_id):
    article = Article.query.get_or_404(article_id)
    if request.method == 'POST':
        fn = os.path.join(app.root_path, 'static/articles', str(current_user.id), str(article_id), 'thesis.docx')
        if os.path.exists(fn):
            os.remove(fn)
        r = requests.get('http://localhost:3000/test/docx/'+str(article.id))
        while not os.path.exists(fn):
            time.sleep(2)
        return 'success'
    elif request.method == 'GET':
        path = os.path.join(app.root_path, 'static/articles', str(current_user.id), str(article_id))
        return send_from_directory(directory=path, filename='thesis.docx', as_attachment=True, attachment_filename='preview.docx')