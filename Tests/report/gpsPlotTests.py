# -*- coding: utf-8 -*-
import logging

import matplotlib.pyplot as plt
import numpy as np

# pyCGM2 settings
import pyCGM2
from pyCGM2.Lib import analysis
from pyCGM2 import enums
from pyCGM2.Processing import c3dManager,scores
from pyCGM2.Model.CGM2 import  cgm,cgm2

from pyCGM2.Report import plot,plotFilters,plotViewers,normativeDatasets
from pyCGM2.Tools import trialTools
from pyCGM2.Report import plot


class gpsPlotTest():

    @classmethod
    def singleAnalysis(cls):

        # ----DATA-----
        DATA_PATH = pyCGM2.TEST_DATA_PATH+"operations\\plot\\gaitPlot\\"
        modelledFilenames = ["gait Trial 03 - viconName.c3d"]


        #---- c3d manager
        #--------------------------------------------------------------------------
        c3dmanagerProcedure = c3dManager.UniqueC3dSetProcedure(DATA_PATH,modelledFilenames)
        cmf = c3dManager.C3dManagerFilter(c3dmanagerProcedure)
        cmf.enableEmg(False)
        trialManager = cmf.generate()

        #---- Analysis
        #--------------------------------------------------------------------------

        modelInfo=None
        subjectInfo=None
        experimentalInfo=None

        analysisInstance = analysis.makeAnalysis("Gait", "CGM1.0", DATA_PATH,modelledFilenames,None, None, None)


        ndp = normativeDatasets.Schwartz2008("Free")
        gps =scores.CGM1_GPS()
        scf = scores.ScoreFilter(gps,analysisInstance, ndp)
        scf.compute()

        # viewer
        kv = plotViewers.GpsMapPlotViewer(analysisInstance)

        # filter
        pf = plotFilters.PlottingFilter()
        pf.setViewer(kv)
        pf.setPath(DATA_PATH)
        pf.setPdfName(str("map"))
        pf.plot()

        plt.show()

if __name__ == "__main__":

    plt.close("all")

    gpsPlotTest.singleAnalysis()
