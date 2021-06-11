from mycrypto import app


@app.route('/')
def flaskRulando():
    return 'Flask está rulando - @magallanesDev'