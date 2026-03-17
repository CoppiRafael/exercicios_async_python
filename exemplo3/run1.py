from flask import Flask
import time

#VEREMOS UM EXEMPLO DE UM SERVIDOR SÍNCRONO 

app = Flask(__name__)

@app.route("/",methods=['GET'])
def hello_world():
    time.sleep(20)
    return {"hello":"world"}

if __name__ == "__main__": app.run(port=8000,threaded=False,host="0.0.0.0")

#digamos que eu faça duas requisições, a primeira vai levar 20 segundos e apenas após 40 segundos (20 da primeira 20 da segunda eu irei finalizar.)
