from flask import Flask, render_template, request 
import sqlite3 
import requests
import pandas as pd
  
app = Flask(__name__, template_folder='templates') 
  
@app.route('/') 
def index(): 
    return render_template('index.html') 

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/twitter_data') 
def twitter_data(): 
    connect = sqlite3.connect('database.db') 
    cursor = connect.cursor() 
    cursor.execute('SELECT * FROM twitter_data limit 20') 
    data = cursor.fetchall() 
    
    return render_template("twitter_data.html", data=data) 
  
  
if __name__ == '__main__': 
  app.run(debug=True)