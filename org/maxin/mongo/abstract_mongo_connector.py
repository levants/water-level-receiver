"""
Created on Oct 30, 2016

Mongo client for containers

@author: Levan Tsinadze
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime

from pymongo import MongoClient


CONTAINER_KEY = 'container_id'
LEVEL_KEY = 'level_info'
COORDINATES_KEY = 'container_coordinates'
LONGITUDE_KEY = 'long_val'
LATITUDE_KEY = 'lat_val'
RECORD_TIME = 'record_time'

UPDATE_SET = '$set'
RECORD_ID = '_id'

INERT_OK = 'OK'
INERT_ERROR = 'Could not save record cause of error'
INERT_NONEED = 'Level was not changed and not saved'

class abstract_mongo_receiver(object):
  """MongoDB client for water level database"""
  
  def __init__(self, host='localhost', port=27017):
    self.client = MongoClient(host, port)
    
  def init_database(self):
    """Initializes database
      Returns:
        database for water levels
    """
    return self.client.level_database
  
  def init_container_collection(self):
    """Initializes containers collection
      Returns:
        container_collection - collection for containers
    """
    
    db = self.init_database()
    container_collection = db.container_collection
    
    return container_collection
  
  def container_record(self, container_id, longitude, latitude):
    """Creates container record for database
      Args:
        container_id - identifier of water container
        longitude - longitude of container
        latitude - latitude for container
      Return:
        mongo_record - container record
    """
    
    return {
        CONTAINER_KEY: container_id,
        COORDINATES_KEY: {
            LONGITUDE_KEY: longitude,
            LATITUDE_KEY: latitude
          },
        RECORD_TIME: datetime.datetime.utcnow()
      }
  
  def container_update(self, container_id, longitude, latitude):
    """Creates container record for update in database
      Args:
        container_id - identifier of water container
        longitude - longitude of container
        latitude - latitude for container
      Return:
        mongo_record - container record for update
    """
    
    return ({
            CONTAINER_KEY:container_id
            },
            {
              UPDATE_SET:{
                RECORD_TIME: datetime.datetime.utcnow(),
                COORDINATES_KEY: {
                          LONGITUDE_KEY: longitude,
                          LATITUDE_KEY: latitude
                          }
                        }
            })
    
  def container_query(self, container_id):
    """Creates container query
      Args: 
        container_id
      Returns:
        container query
    """
    
    return {'$query': {CONTAINER_KEY:container_id},
            '$orderby': {RECORD_TIME:-1}}
    
  def get_container(self, container_id):
    """Gets container from database
      Args: 
        container_id - container identifier
      container_collection - collection from databse
      container_record - container record 
                         from database
    """
    
    container_collection = self.init_container_collection()
    cont_query = self.container_query(container_id)
    container_record = container_collection.find_one(cont_query)
    
    return (container_collection, container_record)
  
  def inert_container(self, container_id, longitude, latitude):
    """Inserts longitude and latitude for container identifier
      Args:
        container_id - container identifier
        longitude - longitude
        latitude - latitude
      Returns:
        record_id - record identifier
    """
    (container_collection, container_info) = self.get_container(container_id)
    if container_info is None:
      container_record = self.container_record(container_id, longitude, latitude)
      record_id = container_collection.insert_one(container_record).inserted_id
    else:
      record_id = container_info[RECORD_ID]
      (update_id, container_record) = self.container_update(container_id, longitude, latitude)
      upd_val = container_collection.update_one(update_id, container_record)
      print(upd_val)
      
    if record_id is not None:
      result_value = INERT_OK
    else:
      result_value = INERT_ERROR
    
    return result_value
  
  def read_containers(self):
    """Reads all containers
      Returns:
        containers
    """
    
    container_collection = self.init_container_collection()
    if container_collection is None:
        result = []
    else:
      result = []
      container_records = container_collection.find({})
      if container_records is not None:
        for container_record in container_records:
          result.append(container_record)
        
    return result
    
      
       
        