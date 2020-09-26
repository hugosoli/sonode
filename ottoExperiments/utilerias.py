import os
import sys, os.path, json
from gaia2 import *
import gaia2.fastyaml as yaml
from optparse import OptionParser
import argparse

def convertJsonToSig(filelist_file, result_filelist_file):
    fl = yaml.load(open(filelist_file, 'r'))

    result_fl = fl
    errors = []

    for trackid, json_file in fl.items():
        try:
            data = json.load(open(json_file))
            # remove descriptors, that will otherwise break gaia_fusion due to incompatibility of layouts
            if 'tags' in data['metadata']:
                del data['metadata']['tags']
            if 'sample_rate' in data['metadata']['audio_properties']:
                del data['metadata']['audio_properties']['sample_rate']
            if 'lossless' in data['metadata']['audio_properties']:
                del data['metadata']['audio_properties']['lossless']

            sig_file = os.path.splitext(json_file)[0] + '.sig'

            yaml.safe_dump(data, open(sig_file, 'w'))
            result_fl[trackid] = sig_file

        except:
            errors += [json_file]

    yaml.dump(result_fl, open(result_filelist_file, 'w'))

    print("Failed to convert", len(errors), "files:")
    for e in errors:
        print(e)

    return len(errors) == 0

def getFilePaths(path_dir, extension):
    path_list = []
    for file in os.listdir(path_dir):
        if file.endswith("."+extension):
            path_list.append(os.path.join(path_dir, file))
    return path_list


def agregarSigPunto(data_set,path_sig):

    basename_ext = os.path.basename(path_sig)
    basename, file_extension = os.path.splitext(basename_ext)

    p = Point()
    p.load(path_sig)
    p.setName(basename)
    ds.addPoint(p)
    return 1

    

# MAIN
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Genera base de datos desde una carpeta de sonidfo")

    parser.add_argument("-i",required=True, help="directorio de entrada")
    parser.add_argument("-o",required=True, help="directorio de salida")
    args = parser.parse_args()

    dir_path = args.i
    out_path = args.o

    #========================
    ds = DataSet()        

    # Obtiene una lista de paths de los archivos json en la carpeta
    archivos_json = getFilePaths(dir_path,'json')

    # Para cada path json, lo convierte a .sig
    for json_file in archivos_json:
        basename_ext = os.path.basename(json_file)
        basename, file_extension = os.path.splitext(basename_ext)
        out_file = os.path.join(out_path,basename+'.sig')
        convertJsonToSig(json_file,out_file)

    # Obtiene una lista de paths de los archivos sig en la carpeta
    archivos_sig = getFilePaths(out_path,'sig')

    # Para cada archivo sig, lo agrega a la base de datos
    for a in archivos_sig:
        agregarSigPunto(ds,a)

    # Exporta la base de datos al folder output especificado
    ds.save(os.path.join(out_path,'missonidos.db'))
