"""
Created on May 22, 2017

Configure service parameters

@author: Levan Tinadze
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

def service_config():
  """Configures service from command line arguments
    Returns:
      flags - configuration flags
  """
  
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument('--host',
                          type=str,
                          default='0.0.0.0.',
                          help='Server address')
  arg_parser.add_argument('--port',
                          type=int,
                          default=8585,
                          help='Server port number')
  arg_parser.add_argument('--mongo_address',
                          type=str,
                          default='127.0.0.0',
                          help='MongoDB server address')
  (flags, _) = arg_parser.parse_known_args()
  
  return flags