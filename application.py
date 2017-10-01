#!/usr/bin/python3
import os
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    g,
    abort,
    url_for,
    jsonify,
    flash,
    send_from_directory)
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from model import Base, Category, SubCategory, ItemCategory, Items, User
from werkzeug import secure_filename
import json
import requests
import time
import shutil
import random
import string
import httplib2
from flask import session as login_session
from flask import make_response


app = Flask(__name__)
# This is the path for image files.
app = Flask(app.name, static_url_path='/static')
# This is the path to the upload folder directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(
    ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['TEMPLATES_AUTO_RELOAD']

app.secret_key = 'super secret key'

engine = create_engine('sqlite:///items.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# For a given file, return whether it's an allowed type or not
# All creds to
# http://code.runnable.com/UiPcaBXaxGNYAAAL/how-to-upload-a-file-to-the-server-in-flask-for-python


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Move uploaded file to right directory
# add itemid in url.


def moveFile(filename, directory, itemid):
    path = os.path.join("/vagrant/catalog/uploads/", filename)
    target = os.path.join('/vagrant/catalog/static/images/' +
                          directory + '/' + str(itemid) + '/', filename)
    targetDir = '/vagrant/catalog/static/images/' + \
        directory + '/' + str(itemid) + '/'
    try:
        os.makedirs(targetDir)  # it creates the destination folder
    except BaseException:
        print targetDir + ' allready exist.'
    os.rename(path, target)


def createUser(login_session):
    newUser = User(
        username=login_session['email'],
        picture=login_session['picture'],
        name=login_session['name'],
        role="user")
    session.add(newUser)
    session.commit()
    return newUser


def getUserInfo(user_id):
    try:
        user = session.query(User).filter_by(id=user_id).one()
        return user
    except BaseException:
        return None


def getUserID(email):
    try:
        user = session.query(User).filter_by(username=email).one()
        return user.id
    except BaseException:
        return None

# set a random state key for Facebook login process / Javascript.
# state variable can be found in main.html sendTokenToServer Function .js


def setState():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return state

# Verify if user has correct user role
# User or Admin


def verify_access(role):
    try:
        id = getUserID(login_session['email'])
    except BaseException:
        id = None
    if id is not None:
        user = getUserInfo(id)
        if user.role == role:
            return True
        else:
            return False
    else:
        return False

# if has no data in login_sesionn then user is a public user.


def publicUser():
    try:
        login_session["email"]
        return False
    except BaseException:
        return True

# Facebook Login Endpoints


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = (
        'https://graph.facebook.com/oauth/access_token?grant_type=fb_exch' +
        'ange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
            app_id, app_secret, access_token
        )
    )
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print result

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token
        exchange we have to split the token first on commas and
        select the first index which gives us the key : value
        for the server access token then we split it on colons
        to pull out the actual token value and replace the remaining quotes
        with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = (
        'https://graph.facebook.com/v2.8/me?' +
        'access_token=%s&fields=name,id,email' % token
    )
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['name'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = (
        'https://graph.facebook.com/v2.8/me/picture' +
        '?access_token=%s&redirect=0&height=200&width=200' % token
    )
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    # Set user piture to session
    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    # Save new user_id to session.
    login_session['user_id'] = user_id
    flash("Now logged in as %s" % login_session['name'])
    return 'logged in'


@app.route('/fbdisconnect')
def fbdisconnect():
    try:
        facebook_id = login_session['facebook_id']
        # The access token must me included to successfully logout
        access_token = login_session['access_token']
        url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
            facebook_id, access_token)
        h = httplib2.Http()
        result = h.request(url, 'DELETE')[1]
        loggedOutUser = login_session['name']
        # Delete login_session properties, user will now be threated as not
        # logged in = public user again.
        del login_session['provider']
        del login_session['facebook_id']
        del login_session['name']
        del login_session['email']
        del login_session['picture']
        flash("logged out : " + loggedOutUser)
        return redirect(url_for('showCategory'))
    except BaseException:
        flash("error logging out user.. contact admin")
        return redirect(url_for('showCategory'))


# Endpoints category

@app.route('/')
@app.route('/catalog')
def showCategory():
    category = session.query(Category).all()
    if verify_access("admin"):
        return render_template(
            'admin_category.html',
            category=category,
            picture=login_session['picture'],
            user=login_session['name'])
    if verify_access("user"):
        # present settings / admin admin url to upgrade permissions.
        # todo: fix option to go back from admin to user.
        return render_template(
            'admin_category_settings.html',
            category=category,
            picture=login_session['picture'],
            user=login_session['name'],
            userid=getUserID(
                login_session['email']))
    else:
        state = setState()
        return render_template(
            'public_category.html', category=category, STATE=state)


@app.route('/catalog/category/<int:categoryid>/edit/', methods=['GET', 'POST'])
def editCategory(categoryid):
    if publicUser() or verify_access("admin") is False:
        flash("log in with your FB Account or add admin priv under settings")
        return redirect('/catalog/accessdenied')
    else:
        editedItem = session.query(Category).filter_by(id=categoryid).one()
        if request.method == 'POST':
            file = request.files['file']
            if request.form['name']:
                editedItem.name = request.form['name']
            if file and allowed_file(file.filename):
                ''' if file was changed and are allowed filename
                 take file in request and save temporary in UPLOAD_FOLDER
                 then move file and place it in a new folder with editItems.ID
                 update db object with new file URL
                 we do this to keep track on every single picture
                 to each db object.
                '''
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                editedItem.picture = 'category/' + \
                    str(editedItem.id) + '/' + filename
                moveFile(filename, 'category', editedItem.id)
            session.add(editedItem)
            session.commit()
            flash("Updated " + editedItem.name + " Category..")
            return redirect(url_for('showCategory'))
        else:
            return render_template(
                'admin_category_edit.html',
                category=editedItem,
                picture=login_session['picture'])


@app.route('/catalog/add/', methods=['GET', 'POST'])
def addCategory():
    if publicUser() or verify_access("admin") is False:
        flash("log in with your FB Account or add admin priv under settings")
        return redirect('/catalog/accessdenied')
    else:
        if request.method == 'POST':
            # add new item with a dummy picture
            # if user selected not to add.
            newItem = Category(
                name=request.form['name'],
                picture='images/dummy/category.png'
            )
            session.add(newItem)
            session.commit()
            file = request.files['file']
            # if user uploaded file, upload file and change url.
            # update db object with new url info.
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                item = session.query(Category).filter_by(
                    name=newItem.name).first()
                item.picture = 'images/category/' + \
                    str(item.id) + '/' + filename
                session.add(item)
                session.commit()
                moveFile(filename, 'category', item.id)
            return redirect(url_for('showCategory'))
        else:
            return render_template(
                'admin_category_add.html',
                picture=login_session['picture'])


@app.route('/catalog/<int:categoryid>/delete/', methods=['GET', 'POST'])
def deleteCategory(categoryid):
    if publicUser() or verify_access("admin") is False:
        flash("log in with your FB Account or add admin priv under settings")
        return redirect('/catalog/accessdenied')
    else:
        itemToDelete = session.query(Category).filter_by(id=categoryid).one()
        if request.method == 'POST':
            session.delete(itemToDelete)
            session.commit()
            try:
                # delete picture if it exist.
                file = '/vagrant/catalog/static/images/category/' + \
                    str(categoryid) + '/'
                shutil.rmtree(file)
            except Exception:
                print 'delete file error, file was not found [' + file + ']'
            flash("deleted category: " + itemToDelete.name + " ...")
            return redirect(url_for('showCategory'))
        else:
            return render_template(
                'admin_category_delete.html',
                item=itemToDelete)
# Subcategory


@app.route('/catalog/subcategory/<int:subcategoryid>', methods=['GET'])
def showSubCategory(subcategoryid):
    subcategory = session.query(SubCategory).filter_by(
        categoryid=subcategoryid).all()
    categoryid = session.query(Category).from_statement(
        text("SELECT id FROM Category where id=:subcategoryid")). params(
        subcategoryid=subcategoryid).first()
    category = session.query(Category).filter_by(id=categoryid.id).first()
    if verify_access("admin"):
        return render_template(
            'admin_subcategory.html',
            subcategory=subcategory,
            category=category,
            picture=login_session['picture'])
    else:
        if verify_access("user"):
            return render_template(
                'user_subcategory.html',
                subcategory=subcategory,
                category=category,
                picture=login_session['picture'])
        else:  # Public User
            state = setState()
            return render_template(
                'public_subcategory.html',
                subcategory=subcategory,
                category=category,
                STATE=state)


@app.route(
    '/catalog/subcategory/<int:subcategoryid>/edit/',
    methods=[
        'GET',
        'POST'])
def editSubCategory(subcategoryid):
    if publicUser() or verify_access("admin") is False:
        flash("log in with your FB Account or add admin priv under settings")
        return redirect('/catalog/accessdenied')
    else:
        editedItem = session.query(
            SubCategory).filter_by(id=subcategoryid).one()
        if request.method == 'POST':
            ''' if file was changed and are allowed filename
                 take file in request and save temporary in UPLOAD_FOLDER
                 then move file and place it in a new folder with editItems.ID
                 update db object with new file URL
                 we do this to keep track on every single picture to
                 each db object.
                '''
            file = request.files['file']
            if request.form['name']:
                editedItem.name = request.form['name']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                editedItem.picture = 'images/subcategory/' + \
                    str(editedItem.id) + '/' + filename
                moveFile(filename, 'category', editedItem.id)
            session.add(editedItem)
            session.commit()
            flash("Updated " + editedItem.name + " Category..")
            return redirect(
                url_for(
                    'showSubCategory',
                    subcategoryid=editedItem.categoryid))
        else:
            return render_template(
                'admin_subcategory_edit.html',
                subcategory=editedItem)


@app.route(
    '/catalog/subcategory/<int:subcategoryid>/delete/',
    methods=[
        'GET',
        'POST'])
def deleteSubCategory(subcategoryid):
    if publicUser() or verify_access("admin") is False:
        flash("log in with your FB Account or add admin priv under settings")
        return redirect('/catalog/accessdenied')
    else:
        itemToDelete = session.query(
            SubCategory).filter_by(id=subcategoryid).one()
        category = session.query(Category).filter_by(
            id=itemToDelete.categoryid).one()
        if request.method == 'POST':
            session.delete(itemToDelete)
            session.commit()
            try:
                # delete picture if it exist.
                file = '/vagrant/catalog/static/images/subcategory/' + \
                    str(subcategoryid) + '/'
                shutil.rmtree(file)
            except Exception:
                print 'delete file error, file was not found [' + file + ']'
            flash("deleted " + itemToDelete.name + " from " + category.name)
            return redirect(
                url_for(
                    'showSubCategory',
                    subcategoryid=category.id))
        else:
            return render_template(
                'admin_subcategory_delete.html',
                item=itemToDelete)


@app.route(
    '/catalog/subcategory/<int:categoryid>/add/',
    methods=[
        'GET',
        'POST'])
def addSubCategory(categoryid):
    if publicUser() or verify_access("admin") is False:
        flash("log in with your FB Account or add admin priv under settings")
        return redirect('/catalog/accessdenied')
    else:
        if request.method == 'POST':
            # add new item with a dummy picture
            newItem = SubCategory(
                name=request.form['name'],
                picture='images/dummy/subcategory.png',
                categoryid=categoryid
            )
            session.add(newItem)
            session.commit()
            file = request.files['file']
            # if user uploaded file, upload file and change url.
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                item = session.query(SubCategory).filter_by(
                    name=newItem.name).first()
                item.picture = 'images/subcategory/' + \
                    str(item.id) + '/' + filename
                session.add(item)
                session.commit()
                moveFile(filename, 'subcategory', item.id)
            return redirect(
                url_for(
                    'showSubCategory',
                    subcategoryid=categoryid))
        else:
            category = session.query(Category).filter_by(id=categoryid).first()
            return render_template(
                'admin_SubCategory_add.html',
                category=category,
                picture=login_session['picture'])


# Item Category endpoints

@app.route('/catalog/itemcategory/<int:itemcategoryid>', methods=['GET'])
def showItemCategory(itemcategoryid):
    itemcategory = session.query(ItemCategory).filter_by(
        subcategoryid=itemcategoryid).all()
    subcategory = session.query(SubCategory).filter_by(
        id=itemcategoryid).first()
    category = session.query(Category).filter_by(
        id=subcategory.categoryid).first()
    # Bugfix if there are no itemcategory.
    if itemcategory == []:
        if verify_access("admin"):
            return render_template(
                'admin_itemcategory_noitems.html',
                subcategory=subcategory,
                category=category,
                picture=login_session['picture'])
        else:
            state = setState()
            return render_template(
                'public_itemcategory.html',
                subcategory=subcategory,
                category=category,
                STATE=state)
    else:
        itemcategoryid = session.query(
            ItemCategory).filter_by(id=itemcategoryid).first()
        if verify_access("admin"):
            return render_template(
                'admin_itemcategory.html',
                subcategory=subcategory,
                category=category,
                itemcategory=itemcategory,
                picture=login_session['picture'])
        else:
            if verify_access("user"):
                return render_template(
                    'user_itemcategory.html',
                    subcategory=subcategory,
                    category=category,
                    itemcategory=itemcategory,
                    picture=login_session['picture'])
            else:
                state = setState()
                return render_template(
                    'public_itemcategory.html',
                    subcategory=subcategory,
                    category=category,
                    itemcategory=itemcategory,
                    STATE=state)


@app.route(
    '/catalog/itemcategory/<int:categoryid>/<int:subcategoryid>/add/',
    methods=[
        'GET',
        'POST'])
def addItemCategory(categoryid, subcategoryid):
    if publicUser() or verify_access("admin") is False:
        flash("log in with your FB Account or add admin priv under settings")
        return redirect('/catalog/accessdenied')
    else:
        if request.method == 'POST':
            # add new item with a dummy picture
            newItem = ItemCategory(
                name=request.form['name'],
                picture='images/dummy/itemcategory.png',
                subcategoryid=subcategoryid
            )
            session.add(newItem)
            session.commit()
            file = request.files['file']
            # if user uploaded file, upload file and change url.
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                item = session.query(ItemCategory).filter_by(
                    name=newItem.name).first()
                item.picture = 'images/itemcategory/' + \
                    str(item.id) + '/' + filename
                session.add(item)
                session.commit()
                moveFile(filename, 'itemcategory', item.id)
            flash("created " + newItem.name)
            return redirect(
                url_for(
                    'showItemCategory',
                    itemcategoryid=subcategoryid))
        else:
            category = session.query(Category).filter_by(id=categoryid).first()
            subcategory = session.query(SubCategory).filter_by(
                id=subcategoryid).first()
            itemcategory = session.query(ItemCategory).all()
            return render_template(
                'admin_ItemCategory_add.html',
                category=category,
                subcategory=subcategory,
                itemcategory=itemcategory,
                picture=login_session['picture'])


@app.route(
    '/catalog/itemcategory/<int:itemcategoryid>/edit/',
    methods=[
        'GET',
        'POST'])
def editItemCategory(itemcategoryid):
    if publicUser() or verify_access("admin") is False:
        flash("log in with your FB Account or add admin priv under settings")
        return redirect('/catalog/accessdenied')
    else:
        editedItem = session.query(ItemCategory).filter_by(
            id=itemcategoryid).one()
        if request.method == 'POST':
            ''' if file was changed and are allowed filename
                 take file in request and save temporary in UPLOAD_FOLDER
                 then move file and place it in a new folder with editItems.ID
                 update db object with new file URL
                 we do this to keep track on every single picture to
                 each db object.
                '''
            file = request.files['file']
            if request.form['name']:
                editedItem.name = request.form['name']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                editedItem.picture = 'images/category/' + \
                    str(editedItem.id) + '/' + filename
                moveFile(filename, 'category', editedItem.id)
            session.add(editedItem)
            session.commit()
            flash("Updated " + editedItem.name + " ItemCategory..")
            return redirect(
                url_for(
                    'showItemCategory',
                    itemcategoryid=editedItem.subcategoryid))
        else:
            subcategory = session.query(SubCategory).filter_by(
                id=editedItem.subcategoryid).one()
            category = session.query(Category).filter_by(
                id=subcategory.categoryid).one()
            return render_template(
                'admin_itemcategory_edit.html',
                item=editedItem,
                category=category,
                subcategory=subcategory)


@app.route(
    '/catalog/itemcategory/<int:itemcategoryid>/delete/',
    methods=[
        'GET',
        'POST'])
def deleteItemCategory(itemcategoryid):
    if publicUser() or verify_access("admin") is False:
        flash("log in with your FB Account or add admin priv under settings")
        return redirect('/catalog/accessdenied')
    else:
        itemToDelete = session.query(
            ItemCategory).filter_by(id=itemcategoryid).one()
        subcategory = session.query(SubCategory).filter_by(
            id=itemToDelete.subcategoryid).one()
        if request.method == 'POST':
            session.delete(itemToDelete)
            session.commit()
            try:
                # delete picture if it exist.
                file = '/vagrant/catalog/static/images/itemcategory/' + \
                    str(itemcategoryid) + '/'
                shutil.rmtree(file)
            except Exception:
                print 'delete file error, file was not found [' + file + ']'
            flash("deleted " + itemToDelete.name + " from " + subcategory.name)
            return redirect(
                url_for(
                    'showItemCategory',
                    itemcategoryid=subcategory.id))
        else:
            category = session.query(Category).filter_by(
                id=subcategory.categoryid).one()
            print category.name
            return render_template(
                'admin_itemcategory_delete.html',
                item=itemToDelete,
                subcategory=subcategory,
                category=category)

# Item Endpoints


@app.route('/catalog/item/<int:itemid>', methods=['GET'])
def showItem(itemid):
    item = session.query(Items).filter_by(id=itemid).first()
    itemcategory = session.query(ItemCategory).filter_by(
        id=item.subcategoryid).first()
    subcategory = session.query(SubCategory).filter_by(
        id=item.subcategoryid).first()
    category = session.query(Category).filter_by(id=item.categoryid).first()
    try:
        userid = getUserID(login_session["email"])
    except BaseException:
        userid = None

    user = getUserInfo(item.owner)
    try:
        owner = user.name
    except BaseException:
        owner = "No owner"
    if userid:
        if item.owner == userid:
            return render_template(
                'user_item.html',
                subcategory=subcategory,
                category=category,
                itemcategory=itemcategory,
                item=item,
                picture=login_session["picture"],
                owner=owner)
        else:
            # Render a new template if user is logged in but not have access
            state = setState()
            return render_template(
                'public_item_1.html',
                subcategory=subcategory,
                category=category,
                itemcategory=itemcategory,
                item=item,
                STATE=state,
                owner=owner,
                picture=login_session["picture"])
    else:
        state = setState()
        return render_template(
            'public_item.html',
            subcategory=subcategory,
            category=category,
            itemcategory=itemcategory,
            item=item,
            STATE=state,
            owner=owner)


@app.route(
    '/catalog/item/<int:categoryid>/<int:subcategoryid>' +
    '/<int:itemcategoryid>/add/',
    methods=[
        'GET',
        'POST'])
def addItem(categoryid, subcategoryid, itemcategoryid):
    publicuser = publicUser()
    if publicuser:
        flash("log in with your FB Account or add admin priv under settings")
        return redirect('/catalog/accessdenied')
    else:
        if request.method == 'POST':
            # add new item with a dummy picture
            # add current user as owner
            userid = getUserID(login_session["email"])
            newItem = Items(
                name=request.form['name'],
                price=request.form['price'],
                description=request.form['description'],
                categoryid=categoryid,
                subcategoryid=subcategoryid,
                picture='images/dummy/item.png',
                itemcategoryid=itemcategoryid,
                owner=userid
            )
            session.add(newItem)
            session.commit()

            # if user uploaded file, upload file and change url.
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                item = session.query(Items).filter_by(id=newItem.id).first()
                item.picture = 'images/item/' + str(item.id) + '/' + filename
                session.add(item)
                session.commit()
                moveFile(filename, 'item', item.id)
            flash("created " + newItem.name)
            return redirect(
                url_for(
                    'showItems',
                    itemcategoryid=itemcategoryid))
        else:
            category = session.query(Category).filter_by(id=categoryid).first()
            subcategory = session.query(SubCategory).filter_by(
                id=subcategoryid).first()
            itemcategory = session.query(ItemCategory).filter_by(
                id=itemcategoryid).first()
            return render_template(
                'user_Item_add.html',
                subcategoryid=subcategoryid,
                categoryid=categoryid,
                itemcategoryid=itemcategoryid,
                category=category,
                subcategory=subcategory,
                itemcategory=itemcategory,
                picture=login_session["picture"])


@app.route('/catalog/item/<int:itemid>/edit/', methods=['GET', 'POST'])
def editItem(itemid):
    if publicUser():
        flash("log in with your FB Account or add admin priv under settings")
        return redirect('/catalog/accessdenied')
    else:
        editedItem = session.query(
            Items).filter_by(id=itemid).one()
        itemcategory = session.query(ItemCategory).filter_by(
            id=editedItem.itemcategoryid).first()
        category = session.query(Category).filter_by(
            id=editedItem.categoryid).first()
        subcategory = session.query(SubCategory).filter_by(
            id=editedItem.subcategoryid).first()

        if request.method == 'POST':
            if request.form['name']:
                editedItem.name = request.form['name']
            if request.form['description']:
                editedItem.description = request.form['description']
            if request.form['price']:
                editedItem.price = request.form['price']
            ''' if file was changed and are allowed filename
                 take file in request and save temporary in
                 UPLOAD_FOLDER
                 then move file and place it in a new folder with editItems.ID
                 update db object with new file URL
                 we do this to keep track on every single picture to
                 each db object.
            '''
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                item = session.query(Items).filter_by(id=editedItem.id).first()
                item.picture = 'images/item/' + str(item.id) + '/' + filename
                session.add(item)
                session.commit()
                moveFile(filename, 'item', item.id)
            session.add(editedItem)
            session.commit()
            flash("updated " + editedItem.name)
            return redirect(
                url_for(
                    'showItems',
                    itemcategoryid=itemcategory.id))
        else:
            try:
                userid = getUserID(login_session["email"])
            except BaseException:
                userid = None
            if userid is not None and editedItem.owner == userid:
                return render_template(
                    'user_item_edit.html',
                    item=editedItem,
                    category=category,
                    subcategory=subcategory,
                    itemcategory=itemcategory)
            else:
                return redirect(url_for('showItem', itemid=editedItem.id))


@app.route('/catalog/item/<int:itemid>/delete/', methods=['GET', 'POST'])
def deleteItem(itemid):
    try:
        itemToDelete = session.query(Items).filter_by(id=itemid).one()
        userid = getUserID(login_session["email"])
    except BaseException:
        userid = None

    if publicUser() or itemToDelete.owner is not userid:
        flash("log in with your FB Account or add admin priv under settings")
        return redirect('/catalog/accessdenied')
    else:
        itemcategory = session.query(ItemCategory).filter_by(
            id=itemToDelete.itemcategoryid).first()
        category = session.query(Category).filter_by(
            id=itemToDelete.categoryid).first()
        subcategory = session.query(SubCategory).filter_by(
            id=itemToDelete.subcategoryid).first()
        if request.method == 'POST':
            session.delete(itemToDelete)
            session.commit()
            try:
                # delete picture if it exist.
                file = '/vagrant/catalog/static/images/item/' + \
                    str(itemid) + '/'
                shutil.rmtree(file)
            except Exception:
                print 'delete file error, file was not found [' + file + ']'
            flask("deleted " + itemToDelete.name)
            return redirect(
                url_for(
                    'showItems',
                    itemcategoryid=itemcategory.id))
        else:
            return render_template(
                'user_item_delete.html',
                item=itemToDelete,
                category=category,
                subcategory=subcategory,
                itemcategory=itemcategory)


# Other endpoints

@app.route('/catalog/settings/admin', methods=['POST', 'GET'])
def settings():
    if publicUser():
        flash("log in with your FB Account or add admin priv under settings")
        return redirect('/catalog/accessdenied')
    else:
        if request.method == 'POST':
            if getUserID(login_session["email"]):
                if request.form['admin'] == 'on':
                    item = session.query(User).filter_by(
                        username=login_session["email"]).first()
                    item.role = "admin"
                    session.add(item)
                    session.commit()
                    name = login_session['name']
                    flash(name + " = admin!")
                    return redirect('/catalog')
                else:
                    flash("error adding user to administrator")
                    return redirect('/catalog')
        else:
            name = login_session['name']
            picture = login_session['picture']
            return render_template('settings.html', name=name, picture=picture)


@app.route('/catalog/<int:userid>/myitems/')
def userItems(userid):
    if publicUser():
        flash("log in with your FBAccount or add admin priv under settings")
        return redirect('/catalog/accessdenied')
    else:
        items = session.query(Items).filter_by(owner=userid).all()
        return render_template(
            'userid_items.html', items=items)


@app.route('/catalog/accessdenied', methods=['GET'])
def accessdenied():
    return render_template('public_access_denied.html')


@app.route('/catalog/items/<int:itemcategoryid>', methods=['GET'])
def showItems(itemcategoryid):

    itemcategory = session.query(ItemCategory).filter_by(
        id=itemcategoryid).first()
    subcategory = session.query(SubCategory).filter_by(
        id=itemcategory.subcategoryid).first()
    category = session.query(Category).filter_by(
        id=subcategory.categoryid).first()
    items = session.query(Items).filter_by(itemcategoryid=itemcategoryid).all()
    if verify_access("admin"):
        return render_template(
            'admin_items.html',
            subcategory=subcategory,
            category=category,
            itemcategory=itemcategory,
            items=items,
            picture=login_session['picture'])
    if verify_access("user"):
        return render_template(
            'user_items.html',
            subcategory=subcategory,
            category=category,
            itemcategory=itemcategory,
            items=items,
            picture=login_session['picture'])
    else:
        state = setState()
        return render_template(
            'public_items.html',
            subcategory=subcategory,
            category=category,
            itemcategory=itemcategory,
            items=items,
            STATE=state)


''' API V1.0 '''
'''
    JSON for item Endpoints
'''


@app.route('/catalog/api/v1.0/item/<int:itemid>/JSON')
def itemJSON(itemid):
    item = session.query(Items).filter_by(id=itemid).one()
    return jsonify(Item=item.serialize)


'''
    JSON for itemcategory Endpoints
'''


@app.route('/catalog/api/v1.0/itemcategory/<int:itemcategoryid>/JSON')
def itemcategoryJSON(itemcategoryid):
    itemcategory = session.query(
        ItemCategory).filter_by(id=itemcategoryid).one()
    return jsonify(ItemCategory=itemcategory.serialize)


@app.route('/catalog/api/v1.0/itemcategory/<int:itemcategoryid>/items/JSON')
def returnItemsJSON(itemcategoryid):
    itemcategory = session.query(Items).filter_by(
        itemcategoryid=itemcategoryid).all()
    return jsonify(ItemCategorys=[i.serialize for i in itemcategory])


'''
    JSON for category Endpoints
'''


@app.route('/catalog/api/v1.0/category/<int:categoryid>/JSON')
def categoryJSON(categoryid):
    print request.headers.get('email')
    category = session.query(Category).filter_by(id=categoryid).one()
    return jsonify(Category=category.serialize)


@app.route('/catalog/api/v1.0/category/<int:categoryid>/subcategorys/JSON')
def returnSubCategorysJSON(categoryid):
    category = session.query(SubCategory).filter_by(
        categoryid=categoryid).all()
    return jsonify(Categorys=[i.serialize for i in category])


'''
    JSON for subcategory Endpoints
'''


@app.route('/catalog/api/v1.0/subcategory/<int:subcategoryid>/JSON')
def subcategoryJSON(subcategoryid):
    subcategory = session.query(SubCategory).filter_by(id=subcategoryid).one()
    return jsonify(SubCategory=subcategory.serialize)


@app.route(
    '/catalog/api/v1.0/subcategory/<int:subcategoryid>/itemcategorys/JSON'
)
def returnItemCategorysJSON(subcategoryid):
    itemcategory = session.query(ItemCategory).filter_by(
        subcategoryid=subcategoryid).all()
    return jsonify(itemCategorys=[i.serialize for i in itemcategory])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
