from flasktts.server import app

if __name__ == '__main__':
    app.debug = True
    app.run(host = 'localhost',port=5005)