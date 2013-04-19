# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import loggingCQM
import gestionConfigFiles
import logging
import time

# Variables Globales ===========================================================
#renseigner le dossier d'installation de CQM
#sys.path.append(r"C:\CQM")
#dossier de travail de CQM
#globalWorkFolder = r"C:\Temp\work"#r"/home/alexandre/abq_tmp/work"
##emplacement du fichier de log général de CQM
#_LOG_FILE = globalWorkFolder + r"\log_daemon.log"

# Programme principal ===========================================================
def main():
    #vérifie si une autre instance de CQM existe déjà
    pidDaemon = 0
    loggingCQM.main_logger.critical("%s", str(pidDaemon))
    if os.path.isfile(globalWorkFolder + r"/daemon.023"):
            print "Daemon already running"
            loggingCQM.main_logger.critical("Daemon already running or .023 file still exist")
    else:
            #crée le fichier de lock
            daemonRunning = file(globalWorkFolder + r"/daemon.023", "w")
            daemonRunning.close()
            loggingCQM.main_logger.critical("daemon started")
            #lancement du processus de gestion de tache
            processDaemon = subprocess.Popen(["python", "lancement_job_obj.py" ])
#            processDaemon= subprocess.Popen(["python", "lancement_job_obj.py"])
            pidDaemon =  processDaemon.pid

            loggingCQM.main_logger.info("calculation batch queue PID : %s", str(pidDaemon))
            #stocker le pid du gestionnaire et des taches dans un fichier de config pour les fermer à la demande
#            while not pidDaemon == 0:
#                time.sleep(1)
            returnCode=processDaemon.wait()
            
            loggingCQM.main_logger.critical("daemon stopped : return Code %s" , returnCode)
            
        
if __name__ == "__main__":
    
    config = gestionConfigFiles.readConfigFile(r"configCQM.cfg")
    gestionConfigFiles.applConfig(config)
    
    loggingCQM.init_daemon_logging(_LOG_FILE)
    
    main()
    
        


