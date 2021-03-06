# -*- coding: utf-8 -*-
#import ipdb

from pyCGM2.Processing import c3dManager, cycle, analysis
from pyCGM2.Model.CGM2 import  cgm
from pyCGM2.Tools import btkTools
from pyCGM2.EMG import emgFilters
from pyCGM2 import enums
from pyCGM2.Processing import exporter


def makeAnalysis(DATA_PATH,
                    modelledFilenames,
                    type="Gait",
                    subjectInfo=None, experimentalInfo=None,modelInfo=None,
                    pointLabelSuffix=None,
                    kinematicLabelsDict=None,
                    kineticLabelsDict=None):

    """
    makeAnalysis : create the pyCGM2.Processing.analysis.Analysis instance

    :param DATA_PATH [str]: path to your data
    :param modelledFilenames [string list]: c3d files with model outputs


    **optional**

    :param type [str]: process files with gait events if selected type is Gait
    :param subjectInfo [dict]:  dictionnary gathering info about the patient (name,dob...)
    :param experimentalInfo [dict]:  dictionnary gathering info about the  data session (orthosis, gait task,... )
    :param modelInfo [dict]:  dictionnary gathering info about the used model)
    :param pointLabelSuffix [string]: suffix previously added to your model outputs
    :param kinematicLabelsDict [dict]: dictionnary with two entries,Left and Right, pointing to kinematic model outputs you desire processes
    :param kineticLabelsDict [dict]: dictionnary with two entries,Left and Right, pointing to kinetic model outputs you desire processes

    .. note::

        The dictionnaries (subjectInfo,experimentalInfo,modelInfo) is interesting
        if you want to find these information within the xls file




    """

    #---- c3d manager
    c3dmanagerProcedure = c3dManager.UniqueC3dSetProcedure(DATA_PATH,modelledFilenames)
    cmf = c3dManager.C3dManagerFilter(c3dmanagerProcedure)
    cmf.enableEmg(False)
    trialManager = cmf.generate()


    #----cycles
    if type == "Gait":
        cycleBuilder = cycle.GaitCyclesBuilder(spatioTemporalTrials=trialManager.spatioTemporal["Trials"],
                                                   kinematicTrials = trialManager.kinematic["Trials"],
                                                   kineticTrials = trialManager.kinetic["Trials"],
                                                   emgTrials=trialManager.emg["Trials"])

    else:
        cycleBuilder = cycle.CyclesBuilder(spatioTemporalTrials=trialManager.spatioTemporal["Trials"],
                                                   kinematicTrials = trialManager.kinematic["Trials"],
                                                   kineticTrials = trialManager.kinetic["Trials"],
                                                   emgTrials=trialManager.emg["Trials"])

    cyclefilter = cycle.CyclesFilter()
    cyclefilter.setBuilder(cycleBuilder)
    cycles = cyclefilter.build()



    #----analysis
    if kinematicLabelsDict is None:
        kinematicLabelsDict = cgm.CGM.ANALYSIS_KINEMATIC_LABELS_DICT

    if kineticLabelsDict is None:
        kineticLabelsDict = cgm.CGM.ANALYSIS_KINETIC_LABELS_DICT



    if type == "Gait":
        analysisBuilder = analysis.GaitAnalysisBuilder(cycles,
                                                      kinematicLabelsDict = kinematicLabelsDict,
                                                      kineticLabelsDict = kineticLabelsDict,
                                                      pointlabelSuffix = pointLabelSuffix)
    else:
        analysisBuilder = analysis.AnalysisBuilder(cycles,
                                                      kinematicLabelsDict = kinematicLabelsDict,
                                                      kineticLabelsDict = kineticLabelsDict,
                                                      pointlabelSuffix = pointLabelSuffix)


    analysisFilter = analysis.AnalysisFilter()
    analysisFilter.setInfo(subject=subjectInfo, model=modelInfo, experimental=experimentalInfo)
    analysisFilter.setBuilder(analysisBuilder)
    analysisFilter.build()

    return analysisFilter.analysis

    #files.saveAnalysis(analysis,DATA_PATH,"Save_and_openAnalysis")

def exportAnalysis(analysisInstance,DATA_PATH,name, mode="Advanced"):

    """
    exportAnalysis : export the pyCGM2.Processing.analysis.Analysis instance in a xls spreadsheet

    :param analysisInstance [pyCGM2.Processing.analysis.Analysis]: pyCGM2 analysis instance
    :param DATA_PATH [str]: path to your data
    :param name [string]: name of the output file

    **optional**

    :param mode [string]: structure of the output xls (choice: Advanced[Default] or Basic)

    .. note::

        the advanced xls organizes data by row ( one raw = on cycle)
        whereas the Basic mode exports each model output in a new sheet



    """

    exportFilter = exporter.XlsAnalysisExportFilter()
    exportFilter.setAnalysisInstance(analysisInstance)
    exportFilter.export(name, path=DATA_PATH,excelFormat = "xls",mode = mode)


def processEMG(DATA_PATH, trialFiles, emgChannels, highPassFrequencies=[20,200],envelopFrequency=6.0, fileSuffix=None):
    """
    processEMG : filters emg channels

    :param DATA_PATH [str]: path to your data
    :param trialFiles [string list]: c3d files with emg signals
    :param emgChannels [string list]: label of your emg channels

    **optional**

    :param highPassFrequencies [list of float]: boundaries of the bandpass filter
    :param envelopFrequency [float]: cut-off frequency for creating an emg envelop
    :param fileSuffix [string]: add suffix to the trial if you dont want overwriting your c3d

    """


    for trialFile in trialFiles:
        acq = btkTools.smartReader(DATA_PATH +trialFile)

        bf = emgFilters.BasicEmgProcessingFilter(acq,emgChannels)
        bf.setHighPassFrequencies(highPassFrequencies[0],highPassFrequencies[1])
        bf.run()

        envf = emgFilters.EmgEnvelopProcessingFilter(acq,emgChannels)
        envf.setCutoffFrequency(envelopFrequency)
        envf.run()

        outFilename = trialFile if fileSuffix is None  else trialFile+"_"+fileSuffix
        btkTools.smartWriter(acq,DATA_PATH+outFilename)



def makeEmgAnalysis(DATA_PATH,
                    processedEmgFiles,
                    emgChannels,
                    subjectInfo=None, experimentalInfo=None,
                    type="Gait"):

    """
    makeEmgAnalysis : create the pyCGM2.Processing.analysis.Analysis instance with only EMG signals


    :param DATA_PATH [str]: path to your data
    :param processedEmgFiles [string list]: c3d files with emg processed outputs
    :param emgChannels [string list]: label of your emg channels

    **optional**

    :param subjectInfo [dict]:  dictionnary gathering info about the patient (name,dob...)
    :param experimentalInfo [dict]:  dictionnary gathering info about the  data session (orthosis, gait task,... )
    :param type [str]: process files with gait events if selected type is Gait

    """



    c3dmanagerProcedure = c3dManager.UniqueC3dSetProcedure(DATA_PATH,processedEmgFiles)
    cmf = c3dManager.C3dManagerFilter(c3dmanagerProcedure)
    cmf.enableSpatioTemporal(False)
    cmf.enableKinematic(False)
    cmf.enableKinetic(False)
    cmf.enableEmg(True)
    trialManager = cmf.generate()

    #---- GAIT CYCLES FILTER
    #--------------------------------------------------------------------------

    #----cycles
    if type == "Gait":
        cycleBuilder = cycle.GaitCyclesBuilder(spatioTemporalTrials=trialManager.spatioTemporal["Trials"],
                                                   kinematicTrials = trialManager.kinematic["Trials"],
                                                   kineticTrials = trialManager.kinetic["Trials"],
                                                   emgTrials=trialManager.emg["Trials"])

    else:
        cycleBuilder = cycle.CyclesBuilder(spatioTemporalTrials=trialManager.spatioTemporal["Trials"],
                                                   kinematicTrials = trialManager.kinematic["Trials"],
                                                   kineticTrials = trialManager.kinetic["Trials"],
                                                   emgTrials=trialManager.emg["Trials"])

    cyclefilter = cycle.CyclesFilter()
    cyclefilter.setBuilder(cycleBuilder)
    cycles = cyclefilter.build()

    emgLabelList  = [label+"_Rectify_Env" for label in emgChannels]

    if type == "Gait":
        analysisBuilder = analysis.GaitAnalysisBuilder(cycles,
                                                      kinematicLabelsDict = None,
                                                      kineticLabelsDict = None,
                                                      emgLabelList = emgLabelList,
                                                      subjectInfos=subjectInfo,
                                                      modelInfos=None,
                                                      experimentalInfos=experimentalInfo)
    else:
        analysisBuilder = analysis.AnalysisBuilder(cycles,
                                                      kinematicLabelsDict = None,
                                                      kineticLabelsDict = None,
                                                      emgLabelList = emgLabelList,
                                                      subjectInfos=subjectInfo,
                                                      modelInfos=None,
                                                      experimentalInfos=experimentalInfo)

    analysisFilter = analysis.AnalysisFilter()
    analysisFilter.setBuilder(analysisBuilder)
    analysisFilter.build()

    analysisInstance = analysisFilter.analysis

    return analysisInstance

def normalizedEMG(analysis, emgChannels,contexts, method="MeanMax", fromOtherAnalysis=None):
    """
    normalizedEMG : perform normalization of emg in amplitude

    :param analysis [pyCGM2.Processing.analysis.Analysis]: pyCGM2 analysis instance
    :param emgChannels [string list]: label of your emg channels
    :param contexts [string list]: contexts associated with your emg channel

    **optional**

    :param method [str]: method of amplitude normalisation (choice MeanMax[default], MaxMax, MedianMax)
    :param fromOtherAnalysis [pyCGM2.Processing.analysis.Analysis]: amplitude normalisation from another analysis instance

    """

    i=0
    for label in emgChannels:


        envnf = emgFilters.EmgNormalisationProcessingFilter(analysis,label,contexts[i])


        if fromOtherAnalysis is not None:
            envnf.setThresholdFromOtherAnalysis(fromOtherAnalysis)

        if method is not "MeanMax":
            envnf.setMaxMethod(enums.EmgAmplitudeNormalization.MeanMax)
        elif method is not "MaxMax":
            envnf.setMaxMethod(enums.EmgAmplitudeNormalization.MaxMax)
        elif method is not "MedianMax":
            envnf.setMaxMethod(enums.EmgAmplitudeNormalization.MedianMax)

        envnf.run()
        i+=1
        del envnf
