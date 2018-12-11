from flask import Flask, request, render_template, redirect, url_for
import json
import subprocess
import yaml
import time
import socket

app = Flask(__name__)

# Method to return the newly created jupyter container details  
def create_jupyter_container(ssh_password):
    python3_command = "python script.py "+ssh_password  # launch your python2 script using bash

    process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()     
    new_container_data = json.loads(output.decode("utf-8"))
    return new_container_data


# Method to append new container details in json file
def insert_new_container_data_for_an_user(user_name, new_container_data):
    old_data = ''
    
    # Append new container data
    with open('user_data.json') as json_file: 
        old_data = json.load(json_file)
        if user_name in old_data:
            current_data = old_data[user_name]['containers']
        else:
            current_data = []
        current_data.append(new_container_data)
        old_data[user_name]['containers'] = current_data
    
    # Dump updated data in the json file
    with open('user_data.json', 'w') as outfile:
        json.dump(old_data,outfile)

    print("New data inserted")

@app.route('/')
def home_page():
    # Home page with link to login page
    return render_template('home.html')

@app.route('/user/<username>', methods=['GET', 'POST'])
def show_user_profile(username):
    # show the user profile for that user
    
    if request.method == 'POST':
        user_name = request.form['uname']
        ssh_password = request.form['ssh_pass']
        # Create a new Container for this user
        new_container_data = create_jupyter_container(ssh_password)
        new_container_data['sshPassword'] = ssh_password
        # Insert new container details of the user in json file
        insert_new_container_data_for_an_user(username, new_container_data)
    
    # Retrieve all container details from jsom file
    with open('user_data.json') as json_file: 
        data = json.load(json_file)
        user_data = data[username]['containers']

  
    # Return to user details page
    return render_template('user.html', user_name = username, user_data = user_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['uname']
        password = request.form['passwd']

        # User credential validation
        with open('user_data.json') as json_file: 
            data = json.load(json_file)
            # If username not found then display appropriate message
            errmsg = ''
            if user_name not in data:
                return render_template('login.html', errmsg = 'Username not Found!!')
            elif data[user_name]['password'] != password:
                return render_template('login.html', errmsg = 'Incorrect password, Please try again.')

        # If valid username, redirect to user page
        return redirect(url_for('show_user_profile',username = user_name))
    else:
        return render_template('login.html')

if __name__ == '__main__':
   app.run(host= '0.0.0.0',port = 1000, debug = True)
