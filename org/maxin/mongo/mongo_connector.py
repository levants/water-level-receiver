"""
Created on Aug 24, 2016

MongoDB connector for water level receiver

@author: Levan Tsinadze
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime

from org.maxin.mongo.abstract_mongo_connector import CONTAINER_KEY, INERT_ERROR, INERT_OK, LEVEL_KEY, RECORD_TIME, INERT_NONEED
from org.maxin.mongo.abstract_mongo_connector import abstract_mongo_receiver


class mongo_receiver(abstract_mongo_receiver):
  """MongoDB client for water level database"""
  
  def __init__(self, host='localhost', port=27017):
    super(mongo_receiver, self).__init__(host, port)
    
  def init_collection(self):
    """Initializes water level collection 
      from database
      Return:
        level_collection - water level collection
    """
    
    db = self.init_database()
    level_collection = db.level_collection
    
    return level_collection
  
  def create_record(self, level_info, container_id):
    """Creates water level record for database
      Args:
        level_info - water level
        container_id - identifier of water container
      Return:
        mongo_record - water level record
    """
    return {
              CONTAINER_KEY: container_id,
              LEVEL_KEY: level_info,
              RECORD_TIME: datetime.datetime.utcnow()
            }
    
  def init_last_record_query(self, container_id):
    """Initializes last record query
      Args:
        container_id - container identifier
      Return:
        last record query
    """
    return {'$query': {CONTAINER_KEY:container_id},
            '$orderby': {RECORD_TIME:-1}}
  # Inserts record to database
  def insert_data(self, level_info, container_id):
    """Inserts water level info
      Args:
        level_info - water level
        container_id - identifier of water container
      Return:
        level_id - assigned unique identifier of record
    """
    
    mongo_record = self.create_record(level_info, container_id)
    level_collection = self.init_collection()
    level_id = level_collection.insert_one(mongo_record).inserted_id
    print(level_id)
    
    if level_id is not None:
      result_value = INERT_OK
    else:
      result_value = INERT_ERROR
    
    return result_value

  def read_last_record(self, container_id):
    """Reads last record from database by container identifier
      Args:
        container_id - container identifier
      Return:
        level_record - water level info
    """
    
    level_collection = self.init_collection()
    lr_query = self.init_last_record_query(container_id)
    level_record = level_collection.find_one(lr_query)
    
    return level_record
  
  def validate_level(self, ext_info, level_info):
    """Validates where level info should be inserted
      Args:
        ext_info - existed level info
        level_info new level info
    """
    ext_number = float(ext_info)
    return ext_number - 1 > level_info or ext_number + 1 < level_info
  
  def validate_and_insert(self, level_info, container_id):
    """Validates and adds water level info to database
      Args:
        level_info - water level
        container_id - identifier of water container
      Return:
        level_id - assigned unique identifier of record
    """
    if level_info is None:
      level_number = -1
    else:
      level_number = float(level_info)
    level_record = self.read_last_record(container_id)
    if level_record is None or self.validate_level(level_record[LEVEL_KEY], level_number) :
      result_value = self.insert_data(level_number, container_id)
    else:
      result_value = INERT_NONEED
      
    return result_value
