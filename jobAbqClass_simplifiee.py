"""Calsse de gestion de job Abaqus 6.11 simplifiée
Alexandre Aury - 11/2012
Release notes: 0.12.11:
"""

class Job:
    """Classe définissant un Job par:
    -cmd
    """
    
    def __init__(self, jobType = "", cmd = ""):
        #ajouter la vérification du type à la création du Job
        self.jobType = jobType
        self.cmd = cmd

    def __str__(self):
        """méthode retournant la commande d'un Job à partir de la converssion en string"""
        return self.cmd

    def execJob(self):
        """Méthode permettant d'exécuter une commande dans un nouveau process
        """
        #ajouter la gestion du popen dans un log + suivi du PID
        subprocess.call(str(self), shell = True)
        
class JobAbq(Job):
    """Classe JobAbq hérite de job
    instance d'un job Abaqus
    paramètres d'entrés: self, inputFileName, pathToInputFile, optCmd [Default void], cpus [default 1]
    """
    def __init__(self, inputFileName, pathToInputFile, optCmd = "", cpus = 1):
        Job.__init__(self, jobType = "abq")
        
        self.inputFileName = inputFileName.split('.')[0]
        self.pathToInputFile = pathToInputFile
        self.optCmd = optCmd
        
    def __str__(self):
        strJob = ""
        strJob = globalCmdAbaqus + ' analysis job=' + self.inputFileName + ' input=' self.pathToInputFile + self.inputFileName + ".inp" 
        strJob = strJob + ' cpus=' + str(self.cpus)
        strJob = strJob + ' ask=off'
        if not self.optCmd == "":
            strJob = strJob + ' ' + self.optCmd
        strJob = strJob + ' interactive'
        
        return strJob
    
    def execJob(self):
        """Méthode permettant d'exécuter un Job Abaqus dans un nouveau process
        """
        #ajouter la gestion du popen dans un log + suivi du PID
        inputFileExists = False
        inputFileExists = os.path.isfile(self.pathToInputFile + self.inputFileName + ".inp")
        if not inputFileExists:
            print "Le fichier spécifié n'existe pas..."
        else :

            strJob = str(self)
            print strJob
            os.chdir(os.path.normpath(r"\\" + self.pathToInputFile))
            
            jobCurrent = subprocess.Popen(str(self),shell=True)
            returnCode=jobCurrent.wait()
            
            time.sleep(10)
            while os.path.isfile(self.pathToInputFile + self.inputFileName + ".023"):
                time.sleep(10)