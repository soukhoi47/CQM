# -*- coding: utf-8 -*-
"""Programme de gestion de de Job et Queue
Alexandre Aury - 09/2012
Licence GPL
Release notes: 0.12.09:
"""

import subprocess
import time
import glob
import os
import shutil
import loggingCQM
import gestionConfigFiles


# Variables Globales ===========================================================
# Configuration ===========================================================
# globalInputFolder = r"C:\Temp\input"
# globalOutputFolder = r"C:\Temp\output"
# globalWorkFolder = r"C:\Temp\work"
# globalTempFolder = r""
# globalCmdAbaqus = "abaqus"
# GLOBAL_CPUS_MAX = 1
# globalRefreshTime = 30
# _LOG_FILE = globalWorkFolder + r"\log_daemon.log"

class Job:
    """Classe définissant un Job par:
    -jobType [abq,lmgc90,script]
    -cmd
    """

    def __init__(self, jobType="", cmd=""):
        # ajouter la vérification du type à la création du Job
        self.jobType = jobType
        self.cmd = cmd

    def __str__(self):
        """méthode retournant la commande d'un Job à partir de la converssion en string"""
        return self.cmd

    def execJob(self):
        """Méthode permettant d'exécuter une commande dans un nouveau process
        """
        # ajouter la gestion du popen dans un log + suivi du PID
        subprocess.call(str(self), shell=True)


class JobAbq(Job):
    """Classe JobAbq hérite de job
    instance d'un job Abaqus
    """
    def __init__(self, inputFileName, pathToInputFile, optCmd="", cpus=1):
        Job.__init__(self, jobType="abq")

        self.inputFileName = inputFileName.split('.')[0]
        self.pathToInputFile = pathToInputFile

        if cpus > GLOBAL_CPUS_MAX:
            self.cpus = GLOBAL_CPUS_MAX
        elif cpus <= 0:
            self.cpus = 1
        else:
            self.cpus = cpus

        self.optCmd = optCmd

    def __str__(self):
        strJob = ""
        strJob = globalCmdAbaqus + ' analysis job=' + self.inputFileName + ' input=' + \
            globalWorkFolder + self.pathToInputFile + \
            self.inputFileName + ".inp"
        strJob = strJob + ' cpus=' + str(self.cpus)
        strJob = strJob + ' ask=off'
        if not globalTempFolder == "":
            strJob = strJob + ' scratch=' + globalTempFolder
        if not self.optCmd == "":
            strJob = strJob + ' ' + self.optCmd
        strJob = strJob  # + ' interactive'

        return strJob

    #def waitCompletion(nbConcurrentJobs=1):
            
    def execJob(self):
        """Méthode permettant d'exécuter un Job Abaqus dans un nouveau process
        """
        # ajouter la gestion du popen dans un log + suivi du PID
        inputFileExists = False
        inputFileExists = os.path.isfile(
            globalInputFolder + self.pathToInputFile + self.inputFileName + ".inp")
        if not inputFileExists:
            print "Le fichier spécifié n'existe pas..."
        else:
            # copie du fichier dans le dossier de travail
            if not os.path.isdir(globalWorkFolder + self.pathToInputFile):
                os.makedirs(globalWorkFolder + self.pathToInputFile)

            shutil.move(globalInputFolder + self.pathToInputFile + self.inputFileName +
                        ".inp", globalWorkFolder + self.pathToInputFile + self.inputFileName + ".inp")

            strJob = str(self)
            print strJob
            os.chdir(os.path.normpath(
                globalWorkFolder + r"/" + self.pathToInputFile))

            # loggingCQM.main_logger.info("%s",os.path.normpath(globalWorkFolder
            # + r"\\" + self.pathToInputFile))

            # appeler la fonction de la classe mère
            loggingCQM.main_logger.info("Executing Job %s", self.inputFileName)
            # jobCurrent = subprocess.call(str(self), shell = True)
            loggingCQM.main_logger.info("abaqus command: %s", str(self))

            jobCurrent = subprocess.Popen(str(self), shell=True)
            returnCode = jobCurrent.wait()

            time.sleep(30)
            while os.path.isfile(globalWorkFolder + self.pathToInputFile + self.inputFileName + ".023"):
                time.sleep(30)

            loggingCQM.main_logger.critical(
                "Job finished with return Code: %s", returnCode)

            # copie des résultats dans le dossier de stockage/partage
            if not os.path.isdir(globalOutputFolder + self.pathToInputFile):
                os.makedirs(globalOutputFolder + self.pathToInputFile)
            for resultFile in glob.glob(globalWorkFolder + self.pathToInputFile + self.inputFileName + '.*'):
                shutil.move(resultFile, globalOutputFolder +
                            resultFile[len(globalWorkFolder):])


class Queue:
    """Classe définissant une liste de job en attente
    """

    def __init__(self):
        self.queue = []
        self.localInputFolder = globalInputFolder

    def check_folder(self):
        tblJob = []
        InputSubfolderList = listdirectory(self.localInputFolder)
        for nomfich in InputSubfolderList:
            if nomfich[-4:] == ".inp":
                tblJob.append(nomfich)
        for job in tblJob:
            JobName = job.split('/')[-1].split('.')[0]
            print JobName
            addToQueue = True
            for Qjob in self.queue:
                if JobName == Qjob.inputFileName:
                    addToQueue = False
            if addToQueue:
                job = job = job[len(self.localInputFolder):]
                job = job.rstrip(JobName + ".inp")

                QjobObj = JobAbq(
                    inputFileName=JobName, pathToInputFile=job)

                loggingCQM.main_logger.info("Job %s created", JobName)

                self.queue.append(QjobObj)
                # self.queue.append({"inputFileName":JobName,
                # "path_to_inputFile":job, "nCPU":1})
                loggingCQM.main_logger.info("%s added to the Queue", JobName)


    def remove(self, Qjob):
        self.queue.remove(Qjob)
# Liste d'attente ===========================================================

def nbConcurentJobsRunning():
    tblJob = []
    InputSubfolderList = listdirectory(globalInputFolder)
    for nomfich in InputSubfolderList:
        if nomfich[-4:] == ".023":
            i=i+1
    return i

def listdirectory(path):
    fichier = []
    for root, dirs, files in os.walk(path):
        for i in files:
            fichier.append(os.path.join(root, i))
    return fichier

def alreadyRunning():
    if not os.path.isfile(globalWorkFolder + r"/daemon.023"):
        loggingCQM.main_logger.critical(
            "daemon.023 file deleted, closing CQM, ")
        return True
    else:
        return False

def daemonQueue():
    strQuit = False

    while strQuit == False:
        while queue.queue == []:
            queue.check_folder()
            if queue.queue == []:
                time.sleep(globalRefreshTime)
            if alreadyRunning():
                strQuit = True
                return

        if not queue.queue == []:
            for Qjob in queue.queue:
                if nbConcurentJobsRunning<1:
                    Qjob.execJob()
                    queue.remove(Qjob)
                    print(queue)

                while suivant==False:
                    if nbConcurentJobsRunning<1:
                        suivant=True
                    else:
                        suivant=False
                        
                if alreadyRunning():
                    strQuit = True
                    return


if __name__ == "__main__":

    config = gestionConfigFiles.readConfigFile(r"configCQM.cfg")
    gestionConfigFiles.applConfig(config)
    global queue

    queue = Queue()

    loggingCQM.init_daemon_logging(_LOG_FILE)
    loggingCQM.main_logger.info("new queue created")

    daemonQueue()

    exit()

#    os.chdir(r"C:\Temp\work")
#    subprocess.call(r"abaqus analysis job=beamgap input=C:\Temp\work\beamgap.inp cpus=1 ask=off interactive", shell=True)
#    print("fin")
