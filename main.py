from flask import Flask

app = Flask(__name__)


from logica.diarios import Principal

@app.route('/')
def index():
    return {'codRes':'00',
            'message': 'sc-diarios-py'}

@app.route('/sc-diarios')
def diarios():
    url = 'https://peru21.pe/archivo/politica/'
    process= Principal(url)
    process.logica()
    return {'codRes':'00',
            'message': 'sc-diarios-py'}


if __name__ == '__main__':
    app.run(debug=True)
