#This is import for Sensors in RaspberryPi4 Ubuntu20.04 environment
import Adafruit_DHT, os, time
import RPi.GPIO as GPIO

from flask import Flask, render_template, url_for, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

GPIO.setmode(GPIO.BOARD)
pin_to_circuit = 7
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 18


class Dht11(Resource):
    def get(self):
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            return jsonify(temperature=temperature, humidity=humidity)
        else:
            return ("Sensor failure. Check wiring")

    
class Ldr(Resource):
    def get(self, pin_to_circuit):
        count = 0

        GPIO.setup(7, GPIO.OUT)
        GPIO.output(7, GPIO.LOW)
        time.sleep(0.1)

        GPIO.setup(7, GPIO.IN)

        while (GPIO.input(7) == GPIO.LOW):
            count += 1
        
        return jsonify(count=count)


api.add_resource(Dht11, '/dht11')
api.add_resource(Ldr, '/ldr')


@app.route('/')
@app.route('/home')
def home():
    print("you are in home end-point")
    return render_template('sensors.html', title='Home')


@app.route('/sensors')
def sensors():
    print("you are in sensors end-point")
    return render_template('sensors.html', title='Sensors')


@app.route('/about')
def about():
    print("you are in about end-point")
    return render_template('about.html', title='About')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='192.168.178.39',port=port, debug=True)