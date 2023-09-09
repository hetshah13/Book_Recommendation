''' pip install virtualenv 
virtualenv env
use activation file
pip install flask
then change debugger from python to python:flask
flask run (click on running http)
congratuation het 
'''
from os import name
import pandas,pickle
from flask import Flask, render_template, request
import numpy as np
import pickle

popular_df1 = pandas.read_pickle(open('popular.pkl','rb'))
pt = pandas.read_pickle(open('pt.pkl','rb'))
books= pandas.read_pickle(open('books.pkl','rb'))
similarity_score = pandas.read_pickle(open('similarity_score.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html',book_name = list(popular_df1['Book-Title'].values),
                        Author = list(popular_df1['Book-Author'].values),
                        Images = list(popular_df1['Image-URL-M'].values),
                        Votes = list(popular_df1['num_ratings'].values),
                        Rating = list(popular_df1['avg_ratings'].values)
                        )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books',  methods= ['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_item = sorted(list(enumerate(similarity_score[index])),key = lambda x: x[1], reverse=True)[1:11]

    data = []
    for i in similar_item:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)


if __name__ =='__main__':
    app.run()