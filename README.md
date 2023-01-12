# nix_project

Functional requirements

1. Searching for movies should return partial matches.
2. To display search results, you must use pagination
(by default - 10 results per page).
3. Movie Operations:
   a. only authorized user can add films
   b. only an authorized user who added film or admin can delete it
   c. only an authorized user who added film or admin can edit it
   d. anyone can browse films
4. Movies can be filtered by:
   a. genres
   b. release
   c. director
5. Movies can be sorted by:
   a. rating
   b. release date
6. Movie Attributes:
   a. title
   b. genres
   c. release date
   d. director
   e. description (optional field)
   f. rating (0-10)
   g. poster
   h. the user who added the movie
7. When deleting a director, the film should NOT be deleted, instead it should be
set director='unknown'.
8. Loading data into the database should be accompanied by common sense validations.
meaning (for example, the year of release - must be a number, not a string).
9. In case of errors, adequate messages and error codes should be issued in order to
the API user could figure out what was causing the error.
10. Authorization must be present (it is recommended to use Flask-Login).

Run project:

1. pip install -r requirements.txt
2. python views.py 