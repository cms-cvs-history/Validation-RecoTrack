import FWCore.ParameterSet.Config as cms

cutsRecoTracks = cms.EDFilter("RecoTrackSelector",
    src = cms.InputTag('generalTracks'),
    #default cuts are dummy: cut used to produce TDR plots are commented
    ptMin = cms.double(0.1),
    minRapidity = cms.double(-5.0), ##-2.5
    maxRapidity = cms.double(5.0), ##2.5
    tip = cms.double(120.0), ##3.5
    lip = cms.double(300.0), ##30
    minHit = cms.int32(3), ##8
    maxChi2 = cms.double(10000.0), ##not used in tdr
    quality = cms.string('loose'),
    algorithm = cms.string('')

)


