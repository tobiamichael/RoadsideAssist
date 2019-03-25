
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from app.forms import DocumentForm
from app.models import Document
from app.plagiarism.ExampleSynchronous import checkPlagiarism
from googletrans import Translator
from app.translate import translateToSpanish
import html



@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('userpage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('userpage')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if current_user.is_authenticated:
        return redirect(url_for('userpage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('create.html', title='Create', form=form)


@app.route('/userpage', methods=['GET', 'POST'])
@login_required
def userpage():
	
	# docs list
    docs = []
    userDocs = current_user.documents.all()
    for index, d in enumerate(userDocs):
        docs.append("document%s" % str(index+1) + ".txt")

    documentContent = []
    for d in userDocs:
        documentContent.append(" ".join(d.text.split()))

    print(documentContent)
    form = DocumentForm()
    if form.validate_on_submit():
        document = Document(text=form.document.data, author=current_user)
        db.session.add(document)
        db.session.commit()
        flash('Document submitted!')
		# process document most recently submitted in database
        text = document.text
        urls = checkPlagiarism(text)
        print(urls)
        # if checking in spanish as well
        if form.spanish.data:
            translation = translateToSpanish(text)
            urlsSpanish = checkPlagiarism(translation)
            print(urlsSpanish)
            #add to url list
            for url in urlsSpanish:
                urls.append(url)
        # use javascript to display urls
        return render_template('userpage_results.html', docs=docs, documentContent=documentContent, urls=urls)
    return render_template('userpage.html', form=form, docs=docs, documentContent=documentContent)


@app.route('/logout')
def logout():
	user = current_user
	user.authenticated = False
	db.session.add(user)
	db.session.commit()
	logout_user()
	return redirect(url_for('login'))
