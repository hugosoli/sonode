import sys
import os
import json
import csv

rootDir = sys.argv[1]
print(rootDir)
	
todoDatos = []

#Se pone python3 + integrador.py + salidaData

def integrador(root, file):
	file_name, file_extension = os.path.splitext(file)
	with open(root + '/' + file) as f:
		data = json.load(f)
		datosDeUno = []
		datosDeUno.append(file_name)
		datosDeUno.append(data.get('lowlevel').get('average_loudness'))
		datosDeUno.append(data.get('lowlevel').get('mfcc').get('mean'))
		#aqui poner mas descriptores
		datosDeUnoFlatten = [a for x in datosDeUno for a in (x if isinstance(x, list) else [x])]
		todoDatos.append(datosDeUnoFlatten)

for root, dirs, files in os.walk(rootDir):
    path = root.split(os.sep)
    print((len(path) - 1) * '---', os.path.basename(root))
    for file in files:
        #print(len(path) * '---', file)
        file_name, file_extension = os.path.splitext(file)
        if file_extension.lower() == ".json":
        	print(len(path) * '---', file)
        	integrador(root,file)

archivoSalida  = open(rootDir + '/' + 'datosDescriptoresTodos.csv', 'w')
with archivoSalida:
	writer = csv.writer(archivoSalida)
	for row in todoDatos:
		writer.writerow(row)