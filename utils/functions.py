import hashlib

def urlnoticia(base, parrafo):
    palabras = parrafo.split()
    primera_palabra = palabras[0]
    segunda_palabra = palabras[1]
    ultima_palabra = palabras[-1]
    resultado = base + '#:~:text=' + primera_palabra + '%20' + segunda_palabra + ',' + ultima_palabra
    return resultado


def hashear(urlParrafo):
    hash_md5 = hashlib.md5()
    hash_md5.update(urlParrafo.encode('utf-8'))
    return hash_md5.hexdigest()
