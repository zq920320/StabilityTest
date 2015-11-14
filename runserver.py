from StabilityTest import app
app.config.from_pyfile('settings.py', silent=True)
app.run(debug=True)