#import FWCore.ParameterSet.Config as cms

process = cms.Process("TkVal")
process.load("FWCore.MessageService.MessageLogger_cfi")

### standard includes
process.load('Configuration/StandardSequences/GeometryPilot2_cff')
process.load("Configuration.StandardSequences.RawToDigi_cff")
process.load("Configuration.EventContent.EventContent_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("SimGeneral.MixingModule.mixNoPU_cfi")

### conditions
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = 'STARTUP_V1::All'
process.GlobalTag.globaltag = 'GLOBALTAG::All'


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(NEVENT)
)
process.source = source

### validation-specific includes
#process.load("SimTracker.TrackAssociation.TrackAssociatorByChi2_cfi")
process.load("SimTracker.TrackAssociation.TrackAssociatorByHits_cfi")
process.load("Validation.RecoTrack.cuts_cff")
process.load("Validation.RecoTrack.MultiTrackValidator_cff")
process.load("SimGeneral.TrackingAnalysis.trackingParticles_cfi")
process.load("DQMServices.Components.EDMtoMEConverter_cff")

process.load("Validation.Configuration.postValidation_cff")

### configuration MultiTrackValidator ###
process.multiTrackValidator.outputFile = 'val.SAMPLE.root'


process.cutsRecoTracks.algorithm = cms.string('ALGORITHM')
process.cutsRecoTracks.quality = cms.string('QUALITY')

process.multiTrackValidator.associators = ['TrackAssociatorByHits']

process.multiTrackValidator.label = ['TRACKS']
if (process.multiTrackValidator.label[0] == 'generalTracks'):
    process.multiTrackValidator.UseAssociators = cms.bool(False)
else:
    process.multiTrackValidator.UseAssociators = cms.bool(True)
######


#process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring (
#    FILENAMES
#    )
#)
#process.extend("RelValTTbar_cff")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)


process.digi2track = cms.Sequence(process.siPixelDigis*process.SiStripRawToDigis*
                                  process.trackerlocalreco*
                                  process.ckftracks*
                                  process.cutsRecoTracks*
                                  ##process.cutsTPEffic*process.cutsTPFake* these modules are now useless
                                  process.multiTrackValidator)
#redo also tracking particles
process.digi2track_and_TP = cms.Sequence(process.mix*process.trackingParticles*
                                  process.siPixelDigis*process.SiStripRawToDigis*
                                  process.trackerlocalreco*
                                  process.ckftracks*
                                  process.cutsRecoTracks*
                                  ##process.cutsTPEffic*process.cutsTPFake* these modules are now useless
                                  process.multiTrackValidator)

process.re_tracking = cms.Sequence(process.siPixelRecHits*process.siStripMatchedRecHits*
                                   process.ckftracks*
                                   process.cutsRecoTracks*
                                   ##process.cutsTPEffic*process.cutsTPFake* these modules are now useless
                                   process.multiTrackValidator
                                   )

process.re_tracking_and_TP = cms.Sequence(process.mix*process.trackingParticles*
                                   process.siPixelRecHits*process.siStripMatchedRecHits*
                                   process.ckftracks*
                                   process.cutsRecoTracks*
                                   ##process.cutsTPEffic*process.cutsTPFake* these modules are now useless
                                   process.multiTrackValidator
                                   )

if (process.multiTrackValidator.label[0] == 'generalTracks'):
    process.only_validation = cms.Sequence(##process.cutsTPEffic*process.cutsTPFake* these modules are now useless
                                           process.multiTrackValidator)
else:
    process.only_validation = cms.Sequence(process.cutsRecoTracks*
                                           ##process.cutsTPEffic*process.cutsTPFake* these modules are now useless
                                           process.multiTrackValidator)
    
if (process.multiTrackValidator.label[0] == 'generalTracks'):
    process.only_validation_and_TP = cms.Sequence(process.mix*process.trackingParticles*process.multiTrackValidator)
else:
    process.only_validation_and_TP = cms.Sequence(process.mix*process.trackingParticles*process.cutsRecoTracks*
                                                  process.multiTrackValidator)

### customized versoin of the OutputModule
### it save the mininal information which is necessary to perform tracking validation (tracks, tracking particles, 
### digiSimLink,etc..)

process.customEventContent = cms.PSet(
     outputCommands = cms.untracked.vstring('drop *')
 )

process.customEventContent.outputCommands.extend(process.RecoTrackerRECO.outputCommands)
process.customEventContent.outputCommands.extend(process.BeamSpotRECO.outputCommands)
process.customEventContent.outputCommands.extend(process.SimGeneralFEVTDEBUG.outputCommands)
process.customEventContent.outputCommands.extend(process.RecoLocalTrackerRECO.outputCommands)
process.customEventContent.outputCommands.append('keep *_simSiStripDigis_*_*')
process.customEventContent.outputCommands.append('keep *_simSiPixelDigis_*_*')
process.customEventContent.outputCommands.append('drop SiStripDigiedmDetSetVector_simSiStripDigis_*_*')
process.customEventContent.outputCommands.append('drop PixelDigiedmDetSetVector_simSiPixelDigis_*_*')



process.OUTPUT = cms.OutputModule("PoolOutputModule",
                                  process.customEventContent,
                                  fileName = cms.untracked.string('output.SAMPLE.root')
                                  )

ValidationSequence="SEQUENCE"

if ValidationSequence=="harvesting":
    process.DQMStore.collateHistograms = False

    process.dqmSaver.convention = 'Offline'

    process.dqmSaver.saveByRun = cms.untracked.int32(-1)
    process.dqmSaver.saveAtJobEnd = cms.untracked.bool(True)
    process.dqmSaver.forceRunNumber = cms.untracked.int32(1)


    process.dqmSaver.workflow = "/GLOBALTAG/SAMPLE/Validation"
    process.DQMStore.verbose=3

    process.options = cms.untracked.PSet(
        fileMode = cms.untracked.string('FULLMERGE')
        )
    for filter in (getattr(process,f) for f in process.filters_()):
        if hasattr(filter,"outputFile"):
            filter.outputFile=""


process.harvesting= cms.Sequence(process.postValidation*process.EDMtoMEConverter*process.dqmSaver)




### final path and endPath
process.p = cms.Path(process.SEQUENCE)
#process.outpath = cms.EndPath(process.OUTPUT)


