from flask import Flask, request
app = Flask(__name__)


from logica.diarios import Principal
import time

@app.route('/')
def index():
    return {'message': 'sc-diarios-py'}

@app.route('/sc-diarios', methods=['POST'])
def diarios():
    json = request.get_json()
    start = time.time()
    
    url = json['url']
    fecha_scraping = json['fecha_scraping']
    
    process= Principal(url, fecha_scraping)
    process.logica()
    end = time.time()
    dif = end - start
    return {'codRes':'00',
            'message': 'sc-diarios-py', 
            'tiempo': dif
            }


if __name__ == '__main__':
    app.run(debug=True)
