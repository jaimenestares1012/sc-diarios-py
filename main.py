from flask import Flask, request
app = Flask(__name__)


from logica.diarios import Principal

@app.route('/')
def index():
    return {'message': 'sc-diarios-py'}

@app.route('/sc-diarios', methods=['POST'])
def diarios():
    json = request.get_json()
    url = json['url']
    fecha_scraping = json['fecha_scraping']
    
    process= Principal(url, fecha_scraping)
    process.logica()
    return {'codRes':'00',
            'message': 'sc-diarios-py'}


if __name__ == '__main__':
    app.run(debug=True)
