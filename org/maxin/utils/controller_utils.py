"""
Created on Jul 7, 2016

Utility module for water level controller

@author: Levan Tsinadze
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


def get_host_info(argv):
  """Initializes port from arguments
    Args:
      argv - command argument
    Return:
      host_nm - host address
  """
    
  if len(argv) > 2:
      host_nm = argv[2]
  else:
      host_nm = '0.0.0.0'
  
  return host_nm

def get_port_info(argv):
  """Initializes port from arguments
    Args:
      argv - command argument
    Return:
      port_nm - port number
  """
    
  if len(argv) > 3:
      port_nm = argv[3]
  else:
      port_nm = 8585
      
  return port_nm

def get_host_and_port(argv):
  """Initializes host and port from arguments
    Args:
      argv - command argument
    Return:
      (host_nm, port_nm) - host and port number
  """
  # Retrieves host and port from arguments or sets defaults
  host_nm = get_host_info(argv)
  port_nm = get_port_info(argv)
  
  return (host_nm, port_nm)
