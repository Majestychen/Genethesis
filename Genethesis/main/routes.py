from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/index")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('articles.main_list'))
    return redirect('/login')

@main.route("/about")
def about():
    return render_template('about.html', section='关于作者', title='关于作者')

@main.route("/important")
def important():
    return render_template('important.html', section='用户须知', title='用户须知')

@main.route("/help/articles")
def help_articles():
    return render_template('help_articles.html', section='支持文档', title='论文添加与编辑 - Genethesis')

@main.route("/help/illustrations")
def help_illustrations():
    return render_template('help_illustrations.html', section='支持文档', title='插图管理功能使用 - Genethesis')

@main.route("/help/export")
def help_export():
    return render_template('help_export.html', section='支持文档', title='论文格式与导出 - Genethesis')