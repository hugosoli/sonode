import sys
import os
from essentia.standard import *
import numpy as np


#python3 cortador.py /Users/hugosg/Documents/OttoAudios/ /Users/hugosg/Documents/OttoSalida/
#entrada carpeta con sonidos
#salida lugar de carpeta nueva para guardar pedacitos

rootDir = sys.argv[1]
rootSalida = sys.argv[2]
print(rootDir)
os.mkdir(rootSalida)

contadorDeArchivos = 0

def segmentador(fileName):
	loader = essentia.standard.MonoLoader(filename=fileName)
	# and then we actually perform the loading:
	audio = loader()

	w = Windowing(type = 'hann')
	spectrum = Spectrum()  # FFT() would return the complex FFT, here we just want the magnitude spectrum
	mfcc = MFCC()

	logNorm = UnaryOperator(type='log')
	mfccs = []
	melbands = []
	melbands_log = []
	pool = essentia.Pool()
	print("num de samples", len(audio))
	for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512, startFromZero=True):
	    mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
	    pool.add('lowlevel.mfcc', mfcc_coeffs)
	    pool.add('lowlevel.mfcc_bands', mfcc_bands)
	    pool.add('lowlevel.mfcc_bands_log', logNorm(mfcc_bands))

	#pedazos muy grandes
	minimumSegmentsLength = 10 
	size1 = 300
	inc1 = 60
	size2 = 200
	inc2 = 20
	cpw = 1.5

	#pedazos muy pequenos
	minimumSegmentsLength = 1
	size1 = 30
	inc1 = 6
	size2 = 20
	inc2 = 2
	cpw = 0.5

	#pedazos muy pequenos2
	minimumSegmentsLength = 10
	size1 = 10
	inc1 = 5
	size2 = 1
	inc2 = 2
	cpw = 0

	#pedazos intermedios
	minimumSegmentsLength = 10
	size1 = 100
	inc1 = 30
	size2 = 60
	inc2 = 5
	cpw = 0

	features = [val for val in pool['lowlevel.mfcc'].transpose()]
	sbic = SBic(size1=size1, inc1=inc1,size2=size2, inc2=inc2,cpw=cpw, minLength=minimumSegmentsLength)
	# only BIC segmentation at the moment:
	segments = sbic(np.array(features))
	print(segments)
	grabadorDeSegmentos(audio,segments)

def grabadorDeSegmentos(audio, segments):
	for indxSegmento in range(len(segments) - 1):
		global contadorDeArchivos
		posDeInicio = int(segments[indxSegmento] * 512)
		posDeFinal = int(segments[indxSegmento + 1] * 512)
		writer = essentia.standard.MonoWriter(filename=rootSalida + "{:06d}".format(contadorDeArchivos) + ".wav", format="wav")(audio[posDeInicio:posDeFinal])
		contadorDeArchivos = contadorDeArchivos + 1

for root, dirs, files in os.walk(rootDir):
    path = root.split(os.sep)
    print((len(path) - 1) * '---', os.path.basename(root))
    for file in files:
        #print(len(path) * '---', file)
        file_name, file_extension = os.path.splitext(file)
        if file_extension.lower() == ".wav":
        	print(len(path) * '---', file)
        	segmentador(root + "/" + file)