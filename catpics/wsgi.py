import catpics

app = catpics.app

catpics.db.create_all()
app.register_blueprint(catpics.api.app.create_app())
app.register_blueprint(catpics.client.app.create_app())
