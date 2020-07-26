from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from myapp import app, db
from myapp.models import Nickname, Article, Comment
from datetime import datetime


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        nick = request.form['nick']
        txt = request.form['addtxt']
        nickname = Nickname.query.filter_by(name=nick).first()
        if not nick or not txt or len(nick)>20 or len(txt)>140:
            flash('暱稱或文章輸入錯誤!')
            return redirect(url_for('index'))
        if nickname:
            addtxt = Article(txt=txt)
            nickname.article.append(addtxt)
            db.session.add(nickname)    
        else:
            nickname = Nickname(name=nick)
            addtxt = Article(txt=txt)
            nickname.article.append(addtxt)
            db.session.add(nickname)
        db.session.commit()
        flash('文章貼上了喔!')
        return redirect(url_for('index'))
    txt = Article.query.order_by(Article.nowtime.desc()).all()
    return render_template('index.html', txts=txt, current_time=datetime.utcnow())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        admin = request.form['admin']
        password = request.form['password']

        if not admin or not password:
            flash('請輸入帳號或密碼...')
            return redirect(url_for('login'))

        nick = Nickname.query.first()
        if admin == nick.admin and nick.validate_password(password):
            login_user(nick)
            flash('oh my king!!!')
            return redirect(url_for('index'))

        flash('who are you?')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("don's go!!!")
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_name = request.form['search']
        if not search_name:
            flash('請輸入暱稱...')
            return redirect(url_for('search'))
        nickname = Nickname.query.filter_by(name=search_name).first()
        if not nickname:
            flash('暱稱不存在...')
            return redirect(url_for('search'))
        nick_txt = nickname.article
        flash('ok...')
        return render_template('search.html', nick_txt=nick_txt)
    else:
        return render_template('search.html')

@app.route('/comment/<int:txt_id>' , methods=['GET', 'POST'])
def comment(txt_id):
    txt = Article.query.get_or_404(txt_id)
    if request.method == 'POST':
        com_name = request.form['nick']
        com_txt = request.form['com_txt']
        if not com_name or not com_txt:
            flash('請輸入暱稱或內容...')
            return redirect(url_for('comment'))
        if len(com_txt) > 100:
            flash('內容請勿超過100個字元...')
            return redirect(url_for('comment'))
        nickname = Nickname.query.filter_by(name=com_name).first()
        if not nickname:
            flash('暱稱不存在...')
            return redirect(url_for('commit'))
        else:
            com_txt = Comment(com_txt=com_txt)
            nickname.n_comment.append(com_txt)
            txt.a_comment.append(com_txt)
            db.session.add(nickname)
            db.session.add(txt)
        db.session.commit()
        flash('回覆成功...')
        return redirect(url_for('comment', txt_id=txt_id))
    com_addtxt = txt.a_comment
    return render_template('comment.html', com_txts=com_addtxt, current_time=datetime.utcnow())    