from flask import Flask

app = Flask(__name__)


@app.route('/home', methods=['GET', 'POST'])
def home():
    return'''<h3>
    hello world
    <h3>
    '''


if __name__ == '__main__':
    app.run()