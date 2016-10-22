'''
Created on Aug 24, 2016

Server to receive water levels

@author: Levan Tsinadze
'''
from sys import argv

from flask import Flask, request

from org.maxin.mongo import mongo_connector as MONGO
from org.maxin.mongo.mongo_connector import mongo_receiver
import org.maxin.utils.controller_utils as controller_utils


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
      water_level = None
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
        respone_data = 'Server is running'
    else:
      respone_data = 'Could not find arguments'
      
    return str(respone_data)
      
    
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
  
  (host_nm, port_nm) = controller_utils.get_host_and_port(argv)
  if len(argv) > 1:
    mongo_address = argv[1]
  else:
    mongo_address = '127.0.0.1'
  mongo_client = mongo_receiver(mongo_address)
  
  app.run(host=host_nm, port=port_nm, threaded=True)
