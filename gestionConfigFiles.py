# -*- coding: utf-8 -*-
"""Bibliothèque de fonction de gestion des fichiers de configuration de CQM
Alexandre Aury - 09/2012
Licence GPL
Release notes: 0.12.09:
"""
#dConfigWindows = {"installFolder":r'C:\CQM', "workFolder":r'C:\Temp\work', "inputFolder":r'C:\Temp\input',
#                  "outputFolder":r'C:\Temp\output', "logFileName":'log_CQM.log', "maxCPUS":1 ,"abqCmd":'abaqus', 
#                  "refreshTime":30 }


import ConfigParser
import os
import __builtin__

dConfigWindows = {"calcFolders":{"installFolder":r'C:\CQM', "workFolder":r'C:\Temp\work', "inputFolder":r'C:\Temp\input',
                  "outputFolder":r'C:\Temp\output', "logFileName":'log_CQM.log'},
                  "calcParam": {"maxCPUS":1 ,"maxGPUS":1,"prlJobs":2, "abqCmd":'abaqus'},
                  "CQMParam":{"refreshTime":30}}


def writeConfigFile(configVar, configFile):
    
    config = ConfigParser.RawConfigParser()
    
    temp = configVar["calcFolders"]
    config.add_section('calcFolders')
    config.set('calcFolders', 'installFolder', temp["installFolder"])
    config.set('calcFolders', 'workFolder', temp["workFolder"])
    config.set('calcFolders', 'inputFolder', temp["inputFolder"])
    config.set('calcFolders', 'outputFolder', temp["outputFolder"])
    config.set('calcFolders', 'logFileName', temp["logFileName"])
    config.set('calcFolders', 'logFile', '%(outputFolder)\\%(logFileName)')
    
    temp = configVar["calcParam"]
    config.add_section('calcParam')
    config.set('calcParam', 'maxCPUS', temp["maxCPUS"])
    config.set('calcParam', 'maxGPUS', temp["maxGPUS"])
    config.set('calcParam', 'prlJobs', temp["prlJobs"])
    config.set('calcParam', 'abqCmd', temp["abqCmd"])
    
    temp = configVar["CQMParam"]
    config.add_section('CQMParam')
    config.set('CQMParam', 'refreshTime', temp["refreshTime"])
    
    # Writing our configuration file to 'configCQM.cfg'
    #os.chdir(os.path.normpath(temp["installFolder"]))
    #with open(configFile, 'wb') as curConfigFile:
    curConfigFile=open(configFile, 'wb')
    config.write(curConfigFile)
        
        
def readConfigFile(configFile):
    #use SafeConfigParser in case of default value
    config = ConfigParser.SafeConfigParser()
    config.read(configFile)
    
    #init return configDic
    configDict = {}
    #RAZ temp dic
    temp = {}
    #reading calcFolder parameters
    temp["installFolder"] = config.get('calcFolders', 'installFolder')
    temp["workFolder"] = config.get('calcFolders', 'workFolder')
    temp["inputFolder"] = config.get('calcFolders', 'inputFolder')
    temp["outputFolder"] = config.get('calcFolders', 'outputFolder')
    temp["logFile"] = config.get('calcFolders', 'logFile')

    configDict["calcFolders"] = temp
    #RAZ temp dic
    temp = {}
    #reading calcParam parameters
    temp["maxCPUS"] = config.get('calcParam', 'maxCPUS')
    temp["maxGPUS"] = config.get('calcParam', 'maxGPUS')
    temp["prlJobs"] = config.get('calcParam', 'prlJobs')
    temp["abqCmd"] = config.get('calcParam', 'abqCmd')
    configDict["calcParam"] = temp
    
    #RAZ temp dic
    temp = {}
    #reading CQMParam parameters
    temp["refreshTime"] = config.get('CQMParam', 'refreshTime')
    configDict["CQMParam"] = temp
    
    return configDict

def applConfig(configDict):
    # global globalInstalFolder
    # global globalWorkFolder
    # global globalInputFolder
    # global globalOutputFolder
    # global _LOG_FILE
    # global GLOBAL_CPUS_MAX
    # global globalCmdAbaqus
    # global globalRefreshTime

    tempConf = {}
    
    tempConf = configDict["calcFolders"]
    
    __builtin__.globalInstalFolder = tempConf["installFolder"]
    __builtin__.globalWorkFolder = tempConf["workFolder"]
    __builtin__.globalInputFolder = tempConf["inputFolder"]
    __builtin__.globalOutputFolder = tempConf["outputFolder"]
    __builtin__._LOG_FILE = tempConf["logFile"]

    tempConf = configDict["calcParam"]

    __builtin__.GLOBAL_CPUS_MAX = int(tempConf["maxCPUS"])
    __builtin__.GLOBAL_GPUS_MAX = int(tempConf["maxGPUS"])
    __builtin__.GLOBAL_PRL_JOBS = int(tempConf["prlJobs"])
    __builtin__.globalCmdAbaqus = tempConf["abqCmd"]
    
    tempConf = configDict["CQMParam"]

    __builtin__.globalRefreshTime = float(tempConf["refreshTime"])
    
    
def writeJobFile(configVar, configFile):
    config = ConfigParser.RawConfigParser()
    
    config.add_section('JobParameters')
    config.set('JobParameters', 'cpus', configVar["cpus"])
    config.set('JobParameters', 'optCmd', configVar["optCmd"])
    
    # Writing our configuration file to 'configCQM.cfg'
    #os.chdir(os.path.normpath(temp["installFolder"]))
    #with open(configFile, 'wb') as curConfigFile:
    curConfigFile=open(configFile, 'wb')
    config.write(curConfigFile)

def readJobFile(configFile):
    #use SafeConfigParser for default value
    config = ConfigParser.SafeConfigParser()
    config.read(configFile)
    
    #init return configDic
    configDict = {}
    
    #reading calcParam parameters
    configDict["cpus"] = config.get('JobParameters', 'cpus')
    configDict["optCmd"] = config.get('JobParameters', 'optCmd')
    
    
    return configDict

    
if __name__ == "__main__":
    
    #configuration file writing test
    writeConfigFile(dConfigWindows,"configCQM.cfg")

    #configuration file reading test
    