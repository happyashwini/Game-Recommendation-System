from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import os
import pickle

app = Flask(__name__)

games = pd.read_csv('games.csv')
M = None

def replace_name(x):
    return games[games['gameId'] == x].title.values[0]

if(os.path.exists('trained_data.pkl')):
    with open('trained_data.pkl', 'rb') as input:
        M = pickle.load(input)
else:
    ratings = pd.read_csv('ratings.csv')
    ratings.gameId = ratings.gameId.map(replace_name)
    M = ratings.pivot_table(index=['userId'], columns=['gameId'], values='rating')
    print('done training')

    with open('trained_data.pkl', 'wb') as output:
        pickle.dump(M, output, pickle.HIGHEST_PROTOCOL)
        print("SAVED")


def pearson(s1, s2):
    """this takes object of two pd.series and returns pearson correlation"""
    s1_c = s1 - s1.mean()
    s2_c = s2 - s2.mean()
    return np.sum(s1_c * s2_c) / np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c ** 2))


def get_recs(game_name, M, num):
    reviews = []
    for title in M.columns:
        if title == game_name:
            continue
        cor = pearson(M[game_name], M[title])
        if np.isnan(cor):
            continue
        else:
            reviews.append((title, cor))

    reviews.sort(key=lambda tup: tup[1], reverse=True)
    return reviews[:num]


@app.route('/')
def mainpage():
    return render_template('mainpage.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    text = request.form['text']
    gamename = text.upper()
    print(gamename)

    recs = get_recs(gamename, M, 5)
    print(recs[:5])

    return render_template('recommendation.html', result=recs)


if __name__ == "__main__":
    app.debug = True
    app.run()