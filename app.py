import os
from os.path import join, dirname
from dotenv import load_dotenv

from pymongo import MongoClient
from flask import Flask, request, render_template, jsonify

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

# ROUTE BASE
@app.route('/')
def base():
    return render_template('index.html')

# ROUTE POST GOALS to database
@app.route('/bucket', methods=['POST'])
def post_bucket():
    receive_goal = request.form['given_goal']
    # Set the number (goals ke berapa gitu)
    # sum total document in database and nest it in count var
    count = db.bucket.count_documents({}) # extracting no dictionary
    num = count + 1
    bucket_doc = {
        'num':num,
        'goal':receive_goal,
        'done':0 # Goal status -> means not done yet, uncomplete (False value)
    }
    db.bucket.insert_one(bucket_doc)
    return jsonify({'msg':'Data saved!'})
    
# ROUTE GET GOALS recently added from database
@app.route('/bucket', methods=['GET'])
def get_bucket():
    goals_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'bucket_list':goals_list})

# ROUTE POST UPDATE for status done
@app.route('/bucket/done', methods = ['POST'])
def update_done():
    done_stat = request.form['given_num']
    db.bucket.update_one({'num': int(done_stat)}, {'$set':{'done':1}})
    return jsonify({'msg':'Update done!'})

# ROUTE POST DELETE done 
@app.route('/bucket/delete', methods=['POST']) 
def delete_done():
    del_stat = request.form['del_num']
    db.bucket.delete_one({'num':int(del_stat), 'done':1})
    return jsonify({'msg':'Delete bucket success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)