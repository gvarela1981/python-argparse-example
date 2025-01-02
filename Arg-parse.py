#!/usr/bin/env python
# coding: utf-8


# In[1]: Documentacion

# ### Monitorea Geoevent a traves de api REST - Valida estado de Inputs
# Consulta el estado de los INPUTS de GeoEvent para su posterior validacion 
# con una plataforma de monitoreo como NAGIOS
# Los parametros se definen en el paso In[4]


# In[2]: Importando librerias
import requests
import os
import sys
import argparse
import json
from cryptography.fernet import Fernet
from arcgis.gis import GIS
import logging
from logging.handlers import RotatingFileHandler
import json

# In[3]: Define funciones
def get_local_path():
    local_path = os.path.realpath('') 
    if os.path.exists(local_path + '\\GE-Monitor.py') == True:
        return local_path
    else:
        local_path = os.path.dirname(__file__)
        return local_path
    
def get_credentials():
    credentials = os.path.realpath('') +'\\'+ 'credentials.json'
    if os.path.exists(credentials) == True:
        pass
    else:
        credentials = os.path.dirname(__file__) +'\\'+ 'credentials.json'

    with open(credentials) as json_data:
        credentials = json.load(json_data)

    key = bytes(credentials['key'].encode())

    ciphered_text = Fernet(key)
    encoded_credentials = credentials['values'].split('-%$&-')
    decoded_credentials = {'portal_desa_user': ciphered_text.decrypt(bytes(encoded_credentials[0].encode())).decode(),
                            'portal_desa_password': ciphered_text.decrypt(bytes(encoded_credentials[1].encode())).decode(),
                            'portal_test_user': ciphered_text.decrypt(bytes(encoded_credentials[2].encode())).decode(),
                            'portal_test_password': ciphered_text.decrypt(bytes(encoded_credentials[3].encode())).decode(),
                            'portal_prod_user': ciphered_text.decrypt(bytes(encoded_credentials[4].encode())).decode(),
                            'portal_prod_password': ciphered_text.decrypt(bytes(encoded_credentials[5].encode())).decode(),
                            'sgip_desa_user': ciphered_text.decrypt(bytes(encoded_credentials[6].encode())).decode(),
                            'sgip_desa_password': ciphered_text.decrypt(bytes(encoded_credentials[7].encode())).decode(),
                            'ge_desa_user': ciphered_text.decrypt(bytes(encoded_credentials[8].encode())).decode(),
                            'ge_desa_password': ciphered_text.decrypt(bytes(encoded_credentials[9].encode())).decode(),
                            'ge_pub_user': ciphered_text.decrypt(bytes(encoded_credentials[8].encode())).decode(),
                            'ge_pub_password': ciphered_text.decrypt(bytes(encoded_credentials[9].encode())).decode()
    }
    return decoded_credentials


# In[4]: Define variables
# Obtiene credenciales
decoded_credentials = get_credentials()
# GeoEvent Credentials
_ge_user = decoded_credentials['ge_pub_user']
_ge_password = decoded_credentials['ge_pub_password']
# _ge_user = 'GAT_MONITOR'
# _ge_password = 'AA_GEgat2024$'
_ge_url = 'https://arba-163m.domainba.com'
_input_energia_ids = [
    '3d9ba073-e33f-4a4a-8112-515f5a257990', #SQL_OK
    '735a361e-55f6-4f59-8f78-2c53719e4e56' # Campamentos
    ]
# Variables de LOG
_maxBytes = 10000000 # 10MB
_backupCount = 5 # Mantener 5 archivos

# In[5]: Iniciando y creando logs
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Creo handlers para loggear en pantallay en un archivo
stdoutHanlder = logging.StreamHandler(sys.stdout)
errHandler = logging.handlers.RotatingFileHandler(f"{get_local_path()}\\error.log", maxBytes=_maxBytes, backupCount=_backupCount)

# Seteo el formato de log
fmt = logging.Formatter(
    "%(filename)s: | %(asctime)s | %(levelname)s | %(lineno)s | %(message)s"
)

# Seteo nivel de error para cada handler
stdoutHanlder.setLevel(logging.DEBUG)
errHandler.setLevel(logging.INFO)

# Seteo el formato de mensaje para cada Handler
stdoutHanlder.setFormatter(fmt)
errHandler.setFormatter(fmt)

# Agrego ambos handler al logger
logger.addHandler(stdoutHanlder)
logger.addHandler(errHandler)

# Ejemplos de LOGS
# logger.debug("Inforcaion de debug")
# logger.info("Importando librerías")
# logger.warning("Importando librerías")
# logger.error("Error generico", exc_info=True)
# logger.critical("Error generico", exc_info=True)

# Arguments Parser
parser = argparse.ArgumentParser(description="Monitorea inputs de GeoEvent. Opcionalmente se reinicia un input")
parser.add_argument("--servicio_id")
args = parser.parse_args()
logger.debug(f"servicio_id es {args.servicio_id}")

# In[6]: Comienza el script
logger.info("Comenzando")
# Adquiriendo token
_ge_token_url = _ge_url + ":6443/arcgis/tokens/f=json"
body = {'f': 'json', 'username': _ge_user, 'password': _ge_password, 'referer': '{0}geoevent/admin'.format(_ge_url)}
logger.debug(f"{_ge_token_url}: {_ge_user}: {_ge_password}")
r = requests.post(_ge_token_url, data=body)

try:
    assert r.status_code == 200, "No se obtuvo token GE"
    logger.debug(f"Respuesta de inicion sesion: {r.status_code}")
except Exception as e:
        logger.error(f"Terminado con error. {str(e)}")
        exit()

response = json.loads(r.content)
try:
    _token = response['token']
    logger.info("Se obtuvo token GE")
except Exception as e:
    logger.error(f"Terminado con error. La respuesta de inicion de sesion no contiene un token: {str(e)}")
    exit()

# Preparando request a Geoevent
headers = {
    'Content-Type': 'application/json',
    "GeoEventAuthorization": _token
}

# Consultando estado de inputs
_ge_api_url = _ge_url + ":6143/geoevent/admin"
_ge_api_inputs = _ge_api_url + "/input"
_results = []

for id in _input_energia_ids:
    try:
        input_energia_url = _ge_api_inputs + "/" + id
        logger.debug(input_energia_url)
        energia_response = requests.request('GET', input_energia_url, headers=headers)
        assert energia_response.status_code == 200, f"No se encontro el input '{id}'"
        response = json.loads(energia_response.content)
        runningState = response['runningState']
        logger.info(f"El estado del input es {runningState}")
        # Chequeo de estado
        _results.append(f"{runningState}")
    except Exception as e:
        logger.info(f"Error al consultar input. {str(e)}")
        _results.append(f"ERROR")

# Chequeo general de todos los estados
if "STOPPED" in _results:
    logger.info("Terminado: Al menos un input esta detenido")
    logger.debug(_results)
    sys.exit(1)
else:
    logger.info("Terminado: ningun input esta detenido")
    logger.debug(_results)
    sys.exit(0)

