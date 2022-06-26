import sqlite3
import json


def showing_columns():
    """
    Выводит название всех имеющихся в базе колонок.
    """
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        query = ("""
                SELECT * FROM netflix
                """)
        query_result = cur.execute(query)
    columns = ['Список колонок в базе netflix.db:']
    for column in query_result.description:
        columns.append(column[0])
    with open('columns.txt', 'w', encoding='utf-8') as file:
        print(*columns, file=file, sep='\n')


def movie_search(title=''):
    """
    Возвращает информацию о фильме по его точному названию в формате json.
    """
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        query = ("""
                SELECT title, country, release_year, listed_in, description FROM netflix
                WHERE title = :myvalue 
                """)
        cur.execute(query, {"myvalue": title})
        query_result = cur.fetchall()
    columns = ['title', 'country', 'release_year', 'listed_in', 'description']
    data_preparation = {}
    for number, column in enumerate (columns):
        data_preparation[column] = query_result[0][number]
    json_data = json.dumps(data_preparation)
    return json_data


def search_movie_by_year(with_year=0, by_year=0):
    """
    Возвращает информацию о фильмах в заданном диапазоне лет в формате json.
    """
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        query = ("""
                SELECT title, release_year FROM netflix
                WHERE release_year BETWEEN :myvalue_with AND :myvalue_by
                LiMIT 100
                """)
        cur.execute(query, {"myvalue_with": with_year, "myvalue_by": by_year})      #LIKE '%' + :myvalue + '%'
        query_result = cur.fetchall()
    data_preparation = []
    for tuple in query_result:
        element_data_preparation = {'title': tuple[0], 'release_year': tuple[1]}
        data_preparation.append(element_data_preparation)
    json_data = json.dumps(data_preparation)
    return json_data


def search_movie_by_rating_for(rating_1='', rating_2='', rating_3=''):
    """
    Возвращает информацию о фильмах по заданному рейтингу в формате json.
    """
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        query = ("""
                SELECT title, rating, description FROM netflix
                WHERE rating IN (:mv_rating_1, :mv_rating_2, :mv_rating_3)
                """)
        cur.execute(query, {"mv_rating_1": rating_1, "mv_rating_2": rating_2, "mv_rating_3": rating_3})
        query_result = cur.fetchall()
    data_preparation = []
    for tuple in query_result:
        element_data_preparation = {'title': tuple[0], 'rating': tuple[1], 'description': tuple[2]}
        data_preparation.append(element_data_preparation)
    json_data = json.dumps(data_preparation)
    return  json_data


def search_movie_by_genre(genre=''):
    """
    Возвращает информацию о фильмах по заданному жанру в формате json.
    """
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        query = ("""
                SELECT title, description FROM netflix
                WHERE listed_in LIKE :mv_genre
                ORDER BY release_year DESC
                LIMIT 10
                """)
        cur.execute(query, {"mv_genre": f'%{genre}%'})
        query_result = cur.fetchall()
    data_preparation = []
    for tuple in query_result:
        element_data_preparation = {'title': tuple[0], 'description': tuple[1]}
        data_preparation.append(element_data_preparation)
    json_data = json.dumps(data_preparation)
    return  json_data


def search_acting_teams(actor_1='', actor_2=''):
    """
    Возвращает список актёров, снимавшихся более 2 раз с заданной парой актёров.
    """
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        query = ("""
                SELECT "cast" FROM netflix
                WHERE "cast" LIKE :mv_actors   
                LIMIT 10
                """)
        cur.execute(query, {"mv_actors": f'%{actor_1}%{actor_2}%'})
        query_result = cur.fetchall()
    actors_in_team = []
    actors_for_search = []
    search_actors = []
    for tuple in query_result:                  # Переводим строки актёров из картежей в общий список
        actors = tuple[0].split(', ')
        print(actors)
        actors_in_team.extend(actors)
    for actor in actors_in_team:                # Убираем из списка заданных актёров.
        if actor not in [actor_1, actor_2]:
            actors_for_search.append(actor)
    for actor in actors_for_search:             # Выбираем в финальный список актёров, встречающихся в общем списке больше 2 раз и не попавшие уже в этот список.
        if actors_for_search.count(actor) > 2 and actor not in search_actors:
            search_actors.append(actor)
    return  search_actors


def search_movie_three_parameters(type_='', release_year=0, listed_in=''):
    """
    ВВозвращает описание фильмов по заданным типу, году и жанру в формате json.
    """
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        query = ("""
                SELECT title, description FROM netflix
                WHERE "type" = :mv_type AND release_year = :mv_release_year AND listed_in LIKE :mv_listed_in
                """)
        cur.execute(query, {"mv_type": type_, "mv_release_year": release_year, "mv_listed_in": f'%{listed_in}%'})
        query_result = cur.fetchall()
        data_preparation = []
        for tuple in query_result:
            element_data_preparation = {'title': tuple[0], 'description': tuple[1]}
            data_preparation.append(element_data_preparation)
        json_data = json.dumps(data_preparation)
        return json_data
