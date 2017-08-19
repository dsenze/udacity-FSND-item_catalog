import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, send_from_directory
# you need to install module in vagrant machine, pip install WTForms
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, SubCategory, ItemCategory, Items
from werkzeug import secure_filename
import shutil
import time

app = Flask(__name__)
# This is the path for image files.
app = Flask(app.name, static_url_path='/static')
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(
    ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

engine = create_engine('sqlite:///items.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# For a given file, return whether it's an allowed type or not
# All creds to http://code.runnable.com/UiPcaBXaxGNYAAAL/how-to-upload-a-file-to-the-server-in-flask-for-python


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def moveFile(filename, directory, itemid):
    path = os.path.join("/vagrant/catalog/uploads/", filename)
    target = os.path.join('/vagrant/catalog/static/images/' +
                          directory + '/' + str(itemid) + '/', filename)
    targetDir = '/vagrant/catalog/static/images/' + \
        directory + '/' + str(itemid) + '/'
    os.makedirs(targetDir)  # it creates the destination folder
    os.rename(path, target)
# WWWW


@app.route('/')
def showCategory():
    category = session.query(Category).all()
    return render_template(
        'public_category.html', category=category)


@app.route('/category/<int:categoryid>/edit/', methods=['GET', 'POST'])
def editCategory(categoryid):
    editedItem = session.query(Category).filter_by(id=categoryid).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['picture']:
            editedItem.picture = request.form['picture']
        time.sleep(5.5)
        session.add(editedItem)
        session.commit()
        return render_template('admin_category_edit.html', category=editedItem)
    else:
        return render_template('admin_category_edit.html', category=editedItem)


@app.route('/category/add/', methods=['GET', 'POST'])
def addCategory():
    if request.method == 'POST':
        # add new item with a dummy picture
        newItem = Category(
            name=request.form['name'],
            picture='dummy/category.png'
        )
        session.add(newItem)
        session.commit()
        file = request.files['file']
        # if user uploaded file, upload file and change url.
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            item = session.query(Category).filter_by(name=newItem.name).first()
            item.picture = 'category/' + str(item.id) + '/' + filename
            session.add(item)
            session.commit()
            moveFile(filename, 'category', item.id)
        return redirect(url_for('showCategory'))
    else:
        return render_template('admin_category_add.html')

@app.route('/category/<int:categoryid>/delete/', methods=['GET', 'POST'])
def deleteCategory(categoryid):
    itemToDelete = session.query(Category).filter_by(id=categoryid).one()
    if request.method =='POST':
        session.delete(itemToDelete)
        session.commit()
        try:
            file = '/vagrant/catalog/static/images/category/' + str(categoryid) + '/'
            shutil.rmtree(file)
        except Exception:
            print 'delete file error, file was not found ['+file+']'
        return redirect(url_for('showCategory'))
    else:
        return render_template('admin_category_delete.html', item=itemToDelete)


'''
    JSON for WWW Endpoints
'''


@app.route('/category/<int:categoryid>/JSON')
def categoryJSON(categoryid):
    category = session.query(Category).filter_by(id=categoryid).one()
    return jsonify(Category=category.serialize)


@app.route('/category/<int:categoryid>/subcategorys/JSON')
def returnSubCategorysJSON(categoryid):
    category = session.query(SubCategory).filter_by(
        categoryid=categoryid).all()
    return jsonify(Categorys=[i.serialize for i in category])

# Subcategory


@app.route('/allsubcategory/')
def showAllSubCategory():
    subcategory = session.query(SubCategory).all()
    return render_template(
        'public_all_subcategory.html', subcategory=subcategory.serialize)


@app.route('/subcategory/<int:subcategoryid>', methods=['GET'])
def showSubCategory(subcategoryid):
    subcategory = session.query(SubCategory).filter_by(
        categoryid=subcategoryid).all()
    categoryid = session.query(Category).from_statement(text("SELECT id FROM Category where id=:subcategoryid")).\
        params(subcategoryid=subcategoryid).first()
    category = session.query(Category).filter_by(id=categoryid.id).first()
    return render_template('public_subcategory.html', subcategory=subcategory, category=category)


@app.route('/subcategory/<int:subcategoryid>/edit/', methods=['GET', 'POST'])
def editSubCategory(subcategoryid):
    editedItem = session.query(SubCategory).filter_by(id=subcategoryid).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['picture']:
            editedItem.picture = request.form['picture']
        time.sleep(5.5)
        session.add(editedItem)
        session.commit()
        return render_template('admin_subcategory_edit.html', subcategory=editedItem)
    else:
        return render_template('admin_subcategory_edit.html', subcategory=editedItem)

@app.route('/subcategory/<int:subcategoryid>/delete/', methods=['GET', 'POST'])
def deleteSubCategory(subcategoryid):
    itemToDelete = session.query(Category).filter_by(id=subcategoryid).one()
    if request.method =='POST':
        session.delete(itemToDelete)
        session.commit()
        try:
            file = '/vagrant/catalog/static/images/subcategory/' + str(subcategoryid) + '/'
            shutil.rmtree(file)
        except Exception:
            print 'delete file error, file was not found ['+file+']'
        return redirect(url_for('showCategory'))
    else:
        return render_template('admin_subcategory_delete.html', item=itemToDelete)


'''
    JSON for subcategory Endpoints
'''
@app.route('/subcategory/add/', methods=['GET', 'POST'])
def addSubCategory():
    if request.method == 'POST':
        # add new item with a dummy picture
        newItem = SubCategory(
            name=request.form['name'],
            picture='dummy/subcategory.png',
            categoryid=request.form['category']
        )
        session.add(newItem)
        session.commit()
        file = request.files['file']
        # if user uploaded file, upload file and change url.
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            item = session.query(SubCategory).filter_by(name=newItem.name).first()
            item.picture = 'subcategory/' + str(item.id) + '/' + filename
            session.add(item)
            session.commit()
            moveFile(filename, 'subcategory', item.id)
        return redirect(url_for('showCategory'))
    else:
        category = session.query(Category).all()
        return render_template('admin_SubCategory_add.html',category=category)


@app.route('/subcategory/<int:subcategoryid>/JSON')
def subcategoryJSON(subcategoryid):
    subcategory = session.query(SubCategory).filter_by(id=subcategoryid).one()
    return jsonify(SubCategory=subcategory.serialize)


@app.route('/subcategory/<int:subcategoryid>/itemcategorys/JSON')
def returnItemCategorysJSON(subcategoryid):
    itemcategory = session.query(ItemCategory).filter_by(
        subcategoryid=subcategoryid).all()
    return jsonify(itemCategorys=[i.serialize for i in itemcategory])

# Item Category


@app.route('/allitemcategory/')
def showAllItemCategory():
    itemcategory = session.query(ItemCategory).all()
    return render_template(
        'public_all_itemcategory.html', itemcategory=itemcategory)


@app.route('/itemcategory/<int:itemcategoryid>', methods=['GET'])
def showItemCategory(itemcategoryid):
    itemcategory = session.query(
        ItemCategory).filter_by(id=itemcategoryid).all()
    itemcategoryid = session.query(
        ItemCategory).filter_by(id=itemcategoryid).first()
    subcategory = session.query(SubCategory).filter_by(
        id=itemcategoryid.id).first()
    category = session.query(Category).filter_by(id=subcategory.id).first()
    return render_template('public_itemcategory.html', subcategory=subcategory, category=category, itemcategory=itemcategory)

@app.route('/itemcategory/add/', methods=['GET', 'POST'])
def addItemCategory():
    if request.method == 'POST':
        # add new item with a dummy picture
        newItem = ItemCategory(
            name=request.form['name'],
            picture='dummy/itemcategory.png',
            subcategoryid=request.form['subcategory']
        )
        session.add(newItem)
        session.commit()
        file = request.files['file']
        # if user uploaded file, upload file and change url.
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            item = session.query(ItemCategory).filter_by(name=newItem.name).first()
            item.picture = 'itemcategory/' + str(item.id) + '/' + filename
            session.add(item)
            session.commit()
            moveFile(filename, 'itemcategory', item.id)
        return redirect(url_for('showCategory'))
    else:
        subcategory = session.query(SubCategory).all()
        return render_template('admin_ItemCategory_add.html',subcategory=subcategory)

@app.route('/itemcategory/<int:itemcategoryid>/edit/', methods=['GET', 'POST'])
def editItemCategory(itemcategoryid):
    editedItem = session.query(ItemCategory).filter_by(id=itemcategoryid).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['picture']:
            editedItem.picture = request.form['picture']
        time.sleep(5.5)
        session.add(editedItem)
        session.commit()
        return render_template('admin_itemcategory_edit.html', itemcategory=editedItem)
    else:
        return render_template('admin_itemcategory_edit.html', itemcategory=editedItem)

@app.route('/itemcategory/<int:itemcategoryid>/delete/', methods=['GET', 'POST'])
def deleteItemCategory(itemcategoryid):
    itemToDelete = session.query(ItemCategory).filter_by(id=itemcategoryid).one()
    if request.method =='POST':
        session.delete(itemToDelete)
        session.commit()
        try:
            file = '/vagrant/catalog/static/images/itemcategory/' + str(itemcategoryid) + '/'
            shutil.rmtree(file)
        except Exception:
            print 'delete file error, file was not found ['+file+']'
        return redirect(url_for('showCategory'))
    else:
        return render_template('admin_itemcategory_delete.html', item=itemToDelete)

'''
    JSON for itemcategory Endpoints
'''


@app.route('/itemcategory/<int:itemcategoryid>/JSON')
def itemcategoryJSON(itemcategoryid):
    itemcategory = session.query(
        ItemCategory).filter_by(id=itemcategoryid).one()
    return jsonify(ItemCategory=itemcategory.serialize)

# Items


@app.route('/items/<int:itemcategoryid>', methods=['GET'])
def showItems(itemcategoryid):
    items = session.query(Items).filter_by(itemcategoryid=itemcategoryid).all()
    itemcategory = session.query(ItemCategory).filter_by(
        id=itemcategoryid).first()
    subcategory = session.query(SubCategory).filter_by(
        id=itemcategoryid).first()
    category = session.query(Category).filter_by(id=subcategory.id).first()
    return render_template('public_items.html', subcategory=subcategory, category=category, itemcategory=itemcategory, items=items)


@app.route('/allitems/')
def showAllItems():
    items = session.query(Items).all()
    return render_template(
        'public_all_items.html', items=items)


@app.route('/item/<int:itemid>', methods=['GET'])
def showItem(itemid):
    item = session.query(Items).filter_by(id=itemid).first()
    print item.name
    itemcategory = session.query(ItemCategory).filter_by(id=item.id).first()
    subcategory = session.query(SubCategory).filter_by(
        id=itemcategory.id).first()
    category = session.query(Category).filter_by(id=subcategory.id).first()
    return render_template('item.html', subcategory=subcategory, category=category, itemcategory=itemcategory, item=item)

@app.route('/item/add/', methods=['GET', 'POST'])
def addItem():
    if request.method == 'POST':
        # add new item with a dummy picture
        print request.form['itemcategory']
        newItem = Items(
            name=request.form['name'],
            price=request.form['price'],
            description=request.form['description'],
            categoryid=request.form['category'],
            subcategoryid=request.form['subcategory'],
            picture='dummy/item.png',
            itemcategoryid=request.form['itemcategory']
        )
        session.add(newItem)
        session.commit()
        file = request.files['file']
        # if user uploaded file, upload file and change url.
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            item = session.query(ItemCategory).filter_by(name=newItem.name).first()
            item.picture = 'item/' + str(item.id) + '/' + filename
            session.add(item)
            session.commit()
            moveFile(filename, 'item', item.id)
        return redirect(url_for('showCategory'))
    else:
        category = session.query(Category).all()
        subcategory = session.query(SubCategory).all()
        itemcategory = session.query(ItemCategory).all()
        return render_template('user_Item_add.html',subcategory=subcategory,category=category,itemcategory=itemcategory)


@app.route('/item/<int:itemid>/edit/', methods=['GET', 'POST'])
def editItem(itemid):
    editedItem = session.query(
        Items).filter_by(id=itemid).one()
    category = session.query(Category).all()
    subcategory = session.query(SubCategory).all()
    itemcategory = session.query(ItemCategory).all()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['picture']:
            editedItem.picture = request.form['picture']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        # propertys allways contain a value. no if needed.
        editedItem.categoryid = request.form['category']
        editedItem.subcategoryid = request.form['subcategory']
        editedItem.itemcategoryid = request.form['itemcategory']
        time.sleep(5.5)
        session.add(editedItem)
        session.commit()
        return render_template('user_item_edit.html', item=editedItem, category=category, subcategory=subcategory, itemcategory=itemcategory)
    else:
        return render_template('user_item_edit.html', item=editedItem, category=category, subcategory=subcategory, itemcategory=itemcategory)

@app.route('/item/<int:itemid>/delete/', methods=['GET', 'POST'])
def deleteItem(itemid):
    itemToDelete = session.query(Items).filter_by(id=itemid).one()
    if request.method =='POST':
        session.delete(itemToDelete)
        session.commit()
        try:
            file = '/vagrant/catalog/static/images/item/' + str(itemid) + '/'
            shutil.rmtree(file)
        except Exception:
            print 'delete file error, file was not found ['+file+']'
        return redirect(url_for('showCategory'))
    else:
        return render_template('user_item_delete.html', item=itemToDelete)


'''
    JSON for item Endpoints
'''


@app.route('/item/<int:itemid>/JSON')
def itemJSON(itemid):
    item = session.query(Items).filter_by(id=itemid).one()
    return jsonify(Item=item.serialize)


@app.route('/item/<int:itemid>/category/name/JSON')
def itemFriendlyNameJSON(itemid):
    item = session.query(Items).filter_by(id=itemid).one()
    category = session.query(Category).filter_by(id=item.categoryid).one()
    subcategory = session.query(SubCategory).filter_by(
        id=item.subcategoryid).one()
    itemcategory = session.query(ItemCategory).filter_by(
        id=item.itemcategoryid).one()

    myobject = [{'categoryname': category.name, 'categoryid': category.id, 'subcategoryname': subcategory.name,
                 'subcategoryid': subcategory.id, 'itemcategoryname': itemcategory.name, 'itemcategoryid': itemcategory.id}]
    return jsonify(myobject)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
