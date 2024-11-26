import psycopg2

connection = psycopg2.connect(
    user='project_3',
    password='hck8fv',
    host='140.117.68.66',
    port='5432',
    dbname='project_3'
)
cursor = connection.cursor()