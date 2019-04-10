import os
from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import current_user, login_required
from Genethesis import app
from Genethesis.illustrations.forms import IllustrationUploadForm
from Genethesis.illustrations.utils import save_illustrations

illustrations = Blueprint('illustrations', __name__)

@illustrations.route('/illustrations')
@login_required
def main_list():
    form = IllustrationUploadForm()
    illustration_path = os.path.join(app.root_path, 'static/illustrations', str(current_user.id))
    illustrations = []
    count = 0
    for illustration in os.listdir(illustration_path):
        if illustration.endswith(".jpg") or illustration.endswith(".png") or illustration.endswith(".jpeg"):
            count = count + 1
            illustrations.append(illustration)
    return render_template('illustrations_list.html', section='插图管理', title='我的插图列表', form=form, illustrations=illustrations, count=count)

@illustrations.route('/illustrations/upload', methods=['POST'])
@login_required
def upload():
    form = IllustrationUploadForm()
    if form.validate_on_submit():
        files = form.illustrations.data
        for file in files:
            if file.filename.endswith(".jpg") or file.filename.endswith(".png") or file.filename.endswith(".jpeg"):
                pass
            else:
                flash('好像混进了一些不是图片的东西……', 'danger')
                return redirect(url_for('illustrations.main_list'))
        save_illustrations(files)
        return redirect(url_for('illustrations.main_list'))
    else:
        flash('上传就这样莫名其妙的失败了，联系程序猿吧……', 'warning')
        return redirect(url_for('illustrations.main_list'))

@illustrations.route('/illustrations/delete/<string:filename>', methods=['POST'])
@login_required
def delete(filename):
    illustration_path = os.path.join(app.root_path, 'static/illustrations', str(current_user.id), filename)
    os.remove(illustration_path)
    return 'success'
    
