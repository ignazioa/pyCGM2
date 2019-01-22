# -*- coding: utf-8 -*-
import logging

import matplotlib.pyplot as plt

# pyCGM2 settings
import pyCGM2
from pyCGM2.Lib import analysis

from pyCGM2 import enums
from pyCGM2.Processing import c3dManager
from pyCGM2.Model.CGM2 import  cgm,cgm2

from pyCGM2.Report import plot,plotFilters,plotViewers,normativeDatasets, annotator
from pyCGM2.Tools import trialTools
from pyCGM2.Report import plot



class oneAnalysis_GaitPlotTest():

    @classmethod
    def gaitDescriptiveKinematicPlotPanel(cls):

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

        # viewer
        kv = plotViewers.LowerLimbKinematicsPlotViewer(analysisInstance)
        kv.setConcretePlotFunction(plot.gaitDescriptivePlot)
        kv.setNormativeDataset(normativeDatasets.Schwartz2008("Free"))

        # filter
        pf = plotFilters.PlottingFilter()
        pf.setViewer(kv)
        pf.plot()


        ka = annotator.Annotator(pf.fig)
        ka.IncreasedRange(0,40,10,40, "Context", timing="Throughout Cycle")
        print(ka.getAnnotations())


        plt.show()



if __name__ == "__main__":

    plt.close("all")

    oneAnalysis_GaitPlotTest.gaitDescriptiveKinematicPlotPanel()

    # oneAnalysis_GaitPlotTest.gaitDescriptiveKinematicPlotPanel()
    # oneAnalysis_GaitPlotTest.gaitDescriptiveKinematicPlotPanel_recorded()
    # oneAnalysis_GaitPlotTest.gaitConsistencyKinematicPlotPanel()
    # oneAnalysis_GaitPlotTest.gaitDescriptiveKineticPlotPanel()
    #
    # multipleAnalysis_GaitPlotTest.gaitDescriptiveKinematicPlotPanel()
    # multipleAnalysis_GaitPlotTest.gaitConsistencyKinematicPlotPanel()
    # multipleAnalysis_GaitPlotTest.gaitMeanOnlyKinematicPlotPanel()
    # multipleAnalysis_GaitPlotTest.gaitConsistencyKineticPlotPanel()
    # multipleAnalysis_GaitPlotTest.gaitMeanOnlyKineticPlotPanel()
