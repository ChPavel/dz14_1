from flask import Flask, render_template
from main import movie_search, search_movie_by_year, search_movie_by_rating_for, search_movie_by_genre

app = Flask(__name__)

@app.route('/')
def start_page():
    """
    Главная страница.
    """
    return 'Поиск фильмов'

@app.route('/movie/<title>/')
def page_movie_by_name(title):
    """
    Страница выбранного фильма.
    """
    movie = movie_search(title)
    return movie

@app.route('/movie/<int:with_year>/to/<int:by_year>/')
def page_movie_by_year(with_year, by_year):
    """
    Страница фильмов, отобранных в указанном диапазоне лет.
    """
    movie = search_movie_by_year(with_year, by_year)
    return movie

@app.route('/rating/children/')
def page_movie_for_children():
    """
    Страница детской подборки.
    """
    movie = search_movie_by_rating_for('G')
    return movie

@app.route('/rating/family/')
def page_movie_for_family():
    """
    Страница семейной подборки.
    """
    movie = search_movie_by_rating_for('G', 'PG', 'PG-13')
    return movie

@app.route('/rating/adult/')
def page_movie_for_adult():
    """
    Страница взрослой подборки.
    """
    movie = search_movie_by_rating_for('R', 'NC-17')
    return movie

@app.route('/genre/<genre>/')
def page_movie_by_genre(genre):
    """
    Страница жанровой подборки.
    """
    movie = search_movie_by_genre(genre)
    return movie

if __name__ == '__main__':
    app.run(debug=True)