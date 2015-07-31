import sys
sys.dont_write_bytecode = True

from catpics.wsgi import app

app.run(host='0.0.0.0')
