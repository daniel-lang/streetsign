# -*- coding: utf-8 -*-
"""  Concertino Digital Signage Project
     (C) Copyright 2013 Daniel Fairhead

    Concertino is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Concertino is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Concertino.  If not, see <http://www.gnu.org/licenses/>.

    ---------------------------------
    Views for Working with users and passwords.

"""


from flask import render_template, url_for, request, session, redirect, \
                  flash, json, g
import app.user_session as user_session
import app.post_types as post_types
from os import makedirs, remove, stat
from app import app
from app.models import DB, User, Group, Feed, Post, Screen, \
                       writeable_feeds, by_id


@app.route('/login', methods=['POST'])
def login():
    # TODO: is using the request.endpoint the best way to do this?
    #       would it be better to use an absolute URL?  I dunno if this
    #       is better against XSS?

    return_to = request.form.get('from','index')
    try:
        user_session.login(request.form['username'], request.form['password'])
    except:
        flash('Invalid username or password! Sorry!')

    return redirect(request.referrer)

@app.route('/logout', methods=['POST'])
def logout():
    return_to = request.form.get('from','index')

    # delete the session from the database:
    try:
        user_session.logout()
    except:
        flash('error logging out. That is odd')

    # return to where we were.
    return redirect(request.referrer)

##################################################################
# User Management:

@app.route('/users')
def users():
    return render_template('users.html', users=User.select())

@app.route('/users/<int:userid>', methods=['GET','POST'])
def user(userid):
    try:
        current_user = user_session.get_user()
    except user_session.NotLoggedIn as e:
        flash("Sorry, you're not logged in!")
        return redirect(url_for('index'))

    user = User.get(id=userid)

    if request.method == 'POST':
        if current_user != user and not current_user.is_admin:
            flash('Sorry! You cannot edit this user!')
            return render_template('user.html',
                    user=user)


    return render_template('user.html',
            posts=Post.select().where(Post.author==user)\
                      .order_by(Post.write_date.desc()).limit(10),
            user=user)


@app.route('/groups')
def groups():
    return render_template('groups.html', groups=Group.select())

