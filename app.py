from flask import Flask, render_template, request 
import sqlite3 
import requests
import pandas as pd
  
app = Flask(__name__, template_folder='templates') 
  
@app.route('/') 
@app.route('/home') 
def index(): 
    return render_template('index.html') 
  
connect = sqlite3.connect('database.db') 
connect.execute( 
    'CREATE TABLE IF NOT EXISTS twitter_data (tweetid TEXT, weekday TEXT, hour INTEGER, day INTEGER, lang TEXT,isreshare TEXT, reach INTEGER, retweetcount INTEGER,likes INTEGER, klout INTEGER, sentiment NUMERIC, text TEXT, locationid INTEGER, userid TEXT)') 


def store_dataset_in_database(url,filename, table_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        df = pd.read_excel(filename) 
        conn = sqlite3.connect('database.db')
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        return True
    else:
        print("Failed to download dataset")
        return False
    
url = 'https://query.data.world/s/kcszo2lcmmwf2nsag57l5xxqv5twrs?dws=00000'
filename = 'twitter.csv'
table_name = 'twitter_data'

if store_dataset_in_database(url, filename,table_name):
    # store_dataset_in_database(filename, table_name)
    print("Dataset downloaded and stored in database successfully")
    
@app.route('/twitter_data') 
def twitter_data(): 
    connect = sqlite3.connect('database.db') 
    cursor = connect.cursor() 
    cursor.execute('SELECT * FROM twitter_data limit 20') 
  
    data = cursor.fetchall() 
    return render_template("twitter_data.html", data=data) 
  
  
if __name__ == '__main__': 
  app.run(debug=True)