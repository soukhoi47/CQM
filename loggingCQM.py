
# -*- coding: utf-8 -*-
"""Programme de gestion de logging
Alexandre Aury - 09/2012
Licence GPL
Release notes: 0.12.09
"""
import glob
import logging
import logging.handlers

def init_daemon_logging(_LOG_FILE):
    LOG_FILENAME = _LOG_FILE
    
    # set-up a specific logger
    global main_logger
    main_logger = logging.getLogger('mainLogger')
    main_logger.setLevel(logging.DEBUG)

    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes = 800000, backupCount = 5)
    handler.setLevel(logging.DEBUG)
    
    # Add a Formater to the Handler
    formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s', \
                                  datefmt = '%d/%m/%Y %H:%M:%S', \
                                  )
    handler.setFormatter(formatter)
    
    # Add the Handler to the logger
    main_logger.addHandler(handler)
    
    
#    logging.basicConfig( \
#        filename=_LOG_FILE, \
#        level=logging.DEBUG, \
#        format='%(asctime)s %(levelname)s - %(message)s', \
#         datefmt='%d/%m/%Y %H:%M:%S', \
#     )
    
    
