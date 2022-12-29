
def post_film():
    directors = [{'name': 'Schindler\'s List', 'genre': 'historical drama', 'release': datetime.date(1993, 11, 10),
                  'description': 'The film follows Oskar Schindler, a German industrialist who saved more than a thousand mostly Polish-Jewish',
                  'rating': 10, 'user_id': 6, 'director_id': '1'},
                 {'name': 'Interstellar', 'genre': 'science fiction', 'release': datetime.date(2014, 7, 23),
                  'description': 'Interstellar is a 2014 epic science fiction film co-written, directed, and produced by Christopher Nolan',
                  'rating': 10, 'user_id': 3, 'director_id': '4'},
                 {'name': 'Inception', 'genre': 'science fiction', 'release': datetime.date(2010, 1, 13),
                  'description': 'Inception is a 2010 science fiction action film written and directed by Christopher Nolan',
                  'rating': 10, 'user_id': 1, 'director_id': '4'},
                 {'name': 'Name1', 'genre': 'genre1', 'release': datetime.date(1997, 6, 7),
                  'description': 'description1', 'rating': 7, 'user_id': 2, 'director_id': '3'}]
    for director in directors:
        new_director = Film(id=director.get('id'), name=director.get('name'), genre=director.get('genre'),
                            release=director.get('release'), description=director.get('description'),
                            rating=director.get('rating'),
                            user_id=director.get('user_id'), director_id=director.get('director_id'))
        db.session.add(new_director)
        db.session.commit()
