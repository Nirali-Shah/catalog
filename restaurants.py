# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 13:11:56 2018

@author: Tarang
"""

# Step1: import files 
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Step 1 : create instance of a class with name of running application
app = Flask(__name__)

#Step 3 : create database_setup.py and lotofmenus.py and run it from shell
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# Step 4: Create HTML pages templates
# Step 5: Change the return statement to render_template

# Step 2 : Create Routing for each webpage# JSON for restaurants
@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurant = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurant])

#Add Json Menu Here
#making an API Endpoint (Get Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant.id).all()
    return jsonify(MenuItems=[i.serialize for i in items])
# ADD JSON API ENDPOINT HERE

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)
# ADD JSON API ENDPOINT HERE

# decorator in python - if ignored gives 404 error
@app.route('/') 
def restaurantsHome():
    return "List all Restaurants."
    
@app.route('/restaurants')
def restaurants():
    #return "List Restaurants."
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/new', methods = ['GET','POST'])
def newRestaurant():
    #return "Create new Restaurant."
    if request.method == 'POST': 
        newRestaurant = Restaurant(name=request.form['restaurantName']) 
        session.add(newRestaurant) 
        session.commit() 
        return redirect(url_for('restaurants')) 
    else: 
        return render_template('newRestaurant.html') 


@app.route('/restaurants/<int:restaurant_id>/edit', methods = ['GET','POST'])
def editRestaurant(restaurant_id):
    #return "Edit Restaurant."
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['editRestaurant']:
            editedRestaurant.name = request.form['editRestaurant']
        session.add(editedRestaurant)
        session.commit()
        return redirect(url_for('restaurants'))
    else:
        return render_template('editRestaurant.html', restaurant_id=restaurant_id, restaurant=editedRestaurant)
    
@app.route('/restaurants/<int:restaurant_id>/delete', methods = ['GET','POST'])
def deleteRestaurant(restaurant_id):
    #return "Delete Restaurant."
    deletedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deletedRestaurant)
        session.commit()
        return redirect(url_for('restaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, restaurant=deletedRestaurant)
    
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    #return "Show Restaurant Menu."
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)

    return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/restaurants/<int:restaurant_id>/new', methods = ['GET','POST'])
def newMenuItem(restaurant_id):
    #return "Create Menu Item."
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['itemName'], description=request.form['description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        #flash("New Menu Item Created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenu.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    #return "Edit Menu Item."
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
         if request.form['itemName']:
            editedItem.name = request.form['itemName']
         if request.form['description']:
            editedItem.description = request.form['description']
         if request.form['price']:
            editedItem.price = request.form['price']
         if request.form['course']:
            editedItem.course = request.form['course']
         session.add(editedItem)
         session.commit()
         #flash("Menu Item Edited!")
         return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editMenu.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    #return "Delete Menu Item."  
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        #flash("Menu Item Deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenu.html', item = itemToDelete, restaurant=restaurant)
        
# Step 1 : gets a name variable set to __main__ 
if __name__ == '__main__':    
    
# secret_key is used for flashing messages
    app.secret_key = 'super_secret_key'
# server reloads itself each time it notices a code change
    app.debug = True 
    app.run(host = '0.0.0.0', port = 5000)
