from flask import Flask
from gaia2 import *
app = Flask(__name__)

@app.route("/")
def hello():
    filter = 'WHERE value.average_loudness < 1 AND label.chords_key = "Eb"'
    similarSongs2 = euclideanView.nnSearch('NR__EL__PiezaCilindrero01_0030.720952.wav.sig',euclideanMetric,filter).get(5)
    #print(similarSongs2)
    return "<h1 style='color:blue'>Listas!</h1>" + str(similarSongs2)

if __name__ == "__main__":
    dsRaw = DataSet()
    dsRaw.load("calindros-data-cruda.db")
    dsClean = DataSet()
    dsClean.load("calindros-data-clean.db")
    dsClean.setReferenceDataSet(dsRaw)
    euclideanMetric = DistanceFunctionFactory.create('euclidean', dsClean.layout())
    euclideanView = View(dsClean)
    #similarSongs1 = euclideanView.nnSearch('NR__EL__PiezaCilindrero01_0030.720952.wav.sig', euclideanMetric).get(10)
    #print(similarSongs1)
    app.run(host='0.0.0.0')
