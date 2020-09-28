from flask import Flask
from flask import current_app, flash, jsonify, make_response, redirect, request, url_for
from gaia2 import *
import random

app = Flask(__name__)

dsRaw = DataSet()
dsRaw.load("calindros-data-cruda.db")
dsClean = DataSet()
dsClean.load("calindros-data-clean.db")
dsClean.setReferenceDataSet(dsRaw)

valueNames = dsRaw.layout().descriptorNames(RealType)
labelNames = dsRaw.layout().descriptorNames(StringType)

euclideanMetric = DistanceFunctionFactory.create('euclidean', dsClean.layout())
euclideanView = View(dsClean)

@app.route("/staticsearch")
def staticsearch():
    similarSongs1 = euclideanView.nnSearch('NR__EL__PiezaCilindrero01_0030.720952.wav.sig', euclideanMetric).get(10)
    return "<h1 style='color:blue'>Listas!</h1>" + str(similarSongs1)

@app.route("/staticfilter")
def staticfilter():
        #similarSongs1 = euclideanView.nnSearch('NR__EL__PiezaCilindrero01_0030.720952.wav.sig', euclideanMetric).get(10)
    #print(similarSongs1)
    
    filter = 'WHERE value.average_loudness < 1 AND label.chords_key = "Eb"'
    similarSongs2 = euclideanView.nnSearch('NR__EL__PiezaCilindrero01_0030.720952.wav.sig',euclideanMetric,filter).get(5)
    #print(similarSongs2)
    return "<h1 style='color:blue'>Listas!</h1>" + str(similarSongs2)

@app.route("/jsontest")
def jsontest():
    random.seed(int(request.args.get('seed')))
    amount = int(request.args.get('amount'))
    sound = random.choice(dsRaw.pointNames())
    similarSounds = euclideanView.nnSearch(sound, euclideanMetric).get(amount)
    todaLaData = {}
    for pname in similarSounds:
        p = dsRaw.point(pname[0])
        data = {}
        data["euclideanDistance"] = pname[1]
        for name in labelNames:
            if type(p.label(name)) == str: data[name] = p.label(name)
        for name in valueNames:
            if type(p.value(name)) == float: data[name] = p.value(name)
        todaLaData[pname[0]] = data
    return jsonify(todaLaData)



if __name__ == "__main__":    
    app.run(host='0.0.0.0')
