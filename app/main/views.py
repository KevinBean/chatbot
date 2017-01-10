# -*- coding=utf-8 -*-
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response,session
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm,\
    CommentForm,EditProjectForm,WebChatbotForm
from .. import db
from ..models import Permission, Role, User, Post, Comment
from ..decorators import admin_required, permission_required
from attract import *
import os
import pypandoc
import aiml
from wordscut import jiebacut


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,
                           show_followed=show_followed, pagination=pagination)


@main.route('/project', methods=['GET', 'POST'])
def project():

    form = EditProjectForm()
    form.MaxCurrent_Value.data = u'1150'
    if form.validate_on_submit():

        dictpath = u'/Users/bianbin/PycharmProjects/chatbot/dict/dict.txt'  # 训练数据越多越准确
        info = {
                u'系统载流量提资': 'systemRef',
                u'系统载流量(A)': 'systemRefValue',
                u'电压等级': '110'
                }
        # 存储文件
        SystemRef = form.SystemRef_File.data
        #filename = current_app.config['UPLOAD_FOLDER'] + '/SystemRef.txt'
        filename = 'doc/互提资料单.txt'
        outputfile = open(filename,'wb')
        outputfile.write(SystemRef.encode('utf-8'))
        outputfile.close()

        # pypandoc.convert_text(SystemRef,'txt','string',outputfile= filename)
        # form.SystemRef_File.dataraw_data.save(current_app.config['UPLOAD_FOLDER'] + filename)
        systemReftoinfo(filename, dictpath, info)
        form.MaxCurrent_Value.data = info[u'系统载流量(A)']
        form.Voltage_Value.data = info[u'电压等级']
        form.MaxCurrent_Detail.data = info[u'系统载流量提资']
        # form.Voltage_Value.data = filename
    return render_template('project.html', form=form)

@main.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    # 1. 创建Kernel()和 并学习AIML 规则库文件
    global kernel  # kernel作为全局变量，方便调用
    kernel = aiml.Kernel()
    kernel.learn("std-startup.xml")
    kernel.respond("load aiml b")
    #2.用户界面
    form = WebChatbotForm()
    try:
        form.Chatroom.data = session['chatroom']
    except:
        pass
    else:
        pass

    if form.Chatroom.data == '':
        #初始欢迎信息
        msgcontent = unicode('iRobot' + ':', 'utf-8') + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
        msgcontent += u'您好,请问有什么可以帮您:)' + '\n '
        form.Chatroom.data += msgcontent
    # 处理输入信息
    if form.validate_on_submit():
        # 1. 读取输入数据，并分词
        raw_msg = form.Input.data
        msg = jiebacut(raw_msg)
        print msg
        # 2. 在聊天内容上方加一行 显示发送人及发送时间，以及输入信息内容
        msgcontent = current_user.username + ':' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
        msgcontent += raw_msg + '\n '
        form.Chatroom.data += msgcontent
        # 3. 获取ＡＩＭＬ的响应bot_response
        bot_response = kernel.respond(form.Input.data)  # bot_response() 信息回复
        # 新的分类处理，根据响应信息内容分类处理
        # msg=>可执行＼无参数的函数调用语句bot_response，如'quit'=>'execexit()'，可以简化这里的ifelse语句，但相应的增加了commands.aiml
        # 文件的维护量 可以用exec(bot_response.replace('exec',''))来执行调用
        # 4. 如果是含exec-的可执行响应，则用exec（）进行执行，调用对应特殊响应函数完成功能。msg与调用函数的对应关系在commands.aiml中定义，调用的函数体在本文件中。
        if 'exec-' in bot_response:
            exec (bot_response.replace('exec-', ''))
            pass  # 清除信息发送框，因为下面处理中有些函数要调用信息发送框中内容，因此放在处理函数之后再清除
        # 5. 如果是文本响应，则直接展示响应信息
        elif bot_response:
            msgcontent = unicode('iRobot' + ':', 'utf-8') + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
            msgcontent += bot_response + '\n '
            form.Chatroom.data += msgcontent
            session['chatroom'] =form.Chatroom.data
    return render_template('chatbot.html', form=form)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts,
                           pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))
