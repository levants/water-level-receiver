"""
Created on Aug 24, 2016

Server to receive water levels

@author: Levan Tsinadze
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from sys import argv

from flask import Flask, request, json
from flask.templating import render_template

from bson import json_util
from org.maxin.mongo import mongo_connector as MONGO
from org.maxin.mongo.mongo_connector import mongo_receiver
from org.maxin.services import config
from org.maxin.utils import controller_utils


app = Flask(__name__)
mongo_address = None
mongo_client = None

class water_level_controller(object):
  """Class for water level controller"""

  def __init__(self):
    self.mongo_client = mongo_client
  
  def read_level(self, container_id):
    """Reads water level info from database
      Args:
        container_id - container identifier
      Return:
        water_level - last recorder water level
    """
    level_record = self.mongo_client.read_last_record(container_id)
    if level_record is None:
      water_level = "None"
    else:
      water_level = level_record[MONGO.LEVEL_KEY]
      
    return water_level
  
  def write_level(self, level_info, container_id):
    """Adds record water level info record to database
      Args:
        level_info - water level
        container_id - container identifier
      Return:
        Transaction message
    """
    return self.mongo_client.validate_and_insert(level_info, container_id)
  
  def read_containers(self):
    """Reads all containers
      Returns:
        all container records
    """
    container_records = self.mongo_client.read_containers()
    results = []  
    if container_records is not None:
      for cont_record in container_records:
        result = json.dumps(cont_record, default=json_util.default)
        results.append(result)
    result_json = json.dumps(results)
    
    return result_json
  
  def update_container(self, container_id, longitude, latitude):
    """Updates container record in datanase
      Args:
        container_id - container identifier
        longitude - longitude coordinate
        latitude - latitude coordinate
      Returns:
        respone_data - response for record update
    """
    
    if container_id is None or longitude is None or latitude is None:
        respone_data = render_template("index.html")
    else:
      container_idi = int(container_id)
      longitudef = float(longitude)
      latitudef = float(latitude)
      respone_data = self.mongo_client.inert_container(container_idi, longitudef, latitudef)
    
    return respone_data
    
  def read_or_write(self, request):
    """Reads or writes data in / from database
      Args:
        request - REST request
      Return:
        respone_data - response from database
    """
    
    container_id = request.args.get('container_id')
    if container_id is not None:
      if request.args.get('read') is not None:
        respone_data = self.read_level(container_id)
      elif request.args.get('write') is not None:
        level_info = request.args.get('level_info')
        respone_data = self.write_level(level_info, container_id)
      else:
        respone_data = render_template("index.html")
    elif request.args.get('containers') is not None:
      if request.args.get('update') is not None:
        longitude = request.args.get('long')
        latitude = request.args.get('lat')
        container_id = request.args.get('cont')
        respone_data = self.update_container(container_id, longitude, latitude)
      else:
        respone_data = self.read_containers()
    else:
      respone_data = render_template("index.html")
      
    return str(respone_data)
  
  def write_coordinates(self):
    container_id = request.args.get('container_id')
    if container_id is not None:
      pass
    
# Receives water level information from HTTP request
@app.route('/', methods=['GET', 'POST'])
def receive_level():
  """Service with HTTP methods
    Return:
      resp - HTTP response
  """
  
  if request.method == 'POST':
    pass
  elif request.method == 'GET':
    leveL_controller = water_level_controller()
    resp = leveL_controller.read_or_write(request)
    
    return resp
    
if __name__ == "__main__":
  
  flags = config.service_config()
  (host_nm, port_nm, mongo_address) = (flags.host, flags.port, flags.mongo_address)
  mongo_client = mongo_receiver(mongo_address)
  
  app.run(host=host_nm, port=port_nm, threaded=True)
