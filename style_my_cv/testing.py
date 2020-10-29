from db import get_db

db = get_db()

result = db.execute('SELECT * FROM user')
print(result)