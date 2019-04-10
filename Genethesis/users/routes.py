import os
from flask import Blueprint, render_template, url_for, redirect, flash, request, jsonify
from Genethesis import db, bcrypt, app
from Genethesis.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, UserAvatarForm, UserSignatureForm, PasswordChangeForm
from Genethesis.models import User
from flask_login import login_user, logout_user, login_required, current_user
from Genethesis.users.utils import save_avatar, delete_avatar, save_signature, delete_signature

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'欢迎回来, {form.username.data}.', category='success')
            return redirect(next_page) if next_page else redirect(url_for('users.profile'))
        else:
            form.password.errors.append('密码输错啦，重来重来！')
    return render_template('login.html', form=form, title='Login')

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        illustrationDic = os.path.join(app.root_path, 'static/illustrations', str(user.id))
        articleDic = os.path.join(app.root_path, 'static/articles', str(user.id))
        if not os.path.exists(illustrationDic):
            os.makedirs(illustrationDic)
        if not os.path.exists(articleDic):
            os.makedirs(articleDic)
        flash(f'账户 {form.username.data} 已经创建，请登录。', category='success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form, title='用户注册')

@users.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f"登出成功，祝您一天愉快！", category='success')
    return redirect(url_for('users.login'))

@users.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    pw_change_form = PasswordChangeForm()
    avatar_form = UserAvatarForm()
    sig_form = UserSignatureForm()
    if form.validate_on_submit():  
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.firstName = form.firstName.data
        current_user.lastName = form.lastName.data
        current_user.university = form.university.data
        current_user.faculty = form.faculty.data
        current_user.grade = form.grade.data
        current_user.selfIntro = form.selfIntro.data
        db.session.commit()
        flash('信息更新成功！', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.firstName.data = current_user.firstName
        form.lastName.data = current_user.lastName
        form.university.data = current_user.university
        form.faculty.data = current_user.faculty
        form.grade.data = current_user.grade
        form.selfIntro.data = current_user.selfIntro
        
    avatar_file = url_for('static', filename='avatars/' + current_user.avatar)
    return render_template('profile.html', section='用户信息', title='用户信息', avatar_file=avatar_file, form=form, pw_change_form=pw_change_form, avatar_form=avatar_form, sig_form=sig_form)

@users.route("/password_change", methods=['POST'])
@login_required
def password_change():
    form = PasswordChangeForm()
    if not bcrypt.check_password_hash(current_user.password, form.oldPw.data):
        flash('旧密码不正确，如果忘记密码，请联系程序猿重置。', 'danger')
        return redirect(url_for('users.profile'))
    if not form.validate_on_submit():
        flash(str(list(form.errors.values())[0])[2:-2], 'danger')
        return redirect(url_for('users.profile'))
    hashed_password = bcrypt.generate_password_hash(form.newPw.data).decode('utf-8')
    user = User.query.get(current_user.id)
    user.password = hashed_password
    db.session.commit()
    flash('密码修改成功，下次登陆请使用新密码。', 'success')
    return redirect(url_for('users.profile'))


@users.route("/profile/avatar_change", methods=['POST'])
@login_required
def avatar_change():
    avatar_form = UserAvatarForm()
    if avatar_form.validate_on_submit():
        if current_user.avatar != 'default.jpg':
            delete_avatar(current_user.avatar)
        avatar_file = save_avatar(avatar_form.avatar.data)
        current_user.avatar = avatar_file
        db.session.commit()
        flash(f'头像修改成功！', 'success')
        return redirect(url_for('users.profile'))
    else:
        flash(f'这怕不是个图片吧，试试PNG或者JPG。', 'danger')
        return redirect(url_for('users.profile'))

@users.route("/profile/signature_change", methods=['POST'])
@login_required
def signature_change():
    sig_form = UserSignatureForm()
    if sig_form.validate_on_submit():
        if current_user.signature:
            delete_signature(current_user.signature)
        signature_file = save_signature(sig_form.signature.data)
        current_user.signature = signature_file
        db.session.commit()
        flash(f'签名修改成功！', 'success')
        return redirect(url_for('users.profile'))
    else:
        flash(f'这怕不是个图片吧，试试PNG或者JPG。', 'danger')
        return redirect(url_for('users.profile'))