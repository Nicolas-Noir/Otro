from flask import Flask, jsonify
import requests
from datetime import datetime
from pushbullet import Pushbullet

app = Flask(__name__)

API_KEY = 'd75b4eb1e6348a08579fc0d233bd1925'
LAT =  51.512697115980636#"-32.93493470612179" 
LON = -0.09196918410285405#'-60.649637853793514' 
PUSHBULLET_TOKEN = 'o.zO8z0GyjVOodMGLBK3kqRNdlEUAJnFKr'



def enviar_notificacion(mensaje):
    pb = Pushbullet(PUSHBULLET_TOKEN)
    pb.push_note('Clima', mensaje)



@app.route('/llueve', methods=['GET'])
def llueve():
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    datos = response.json()

    hoy = datetime.now().date()
    hoy_llueve = False

    for pronostico in datos['list']:
        fecha_pronostico = datetime.fromtimestamp(pronostico['dt']).date()

        if fecha_pronostico == hoy:
            if 'rain' in pronostico:
                hoy_llueve = True
                break

    if hoy_llueve:
        mensaje = 'Hoy llueve'
    else:
        mensaje = 'Hoy NO llueve'

    enviar_notificacion(mensaje)

    return jsonify({'mensaje': mensaje})
    
if __name__ == '__main__':
    app.run(debug=True)