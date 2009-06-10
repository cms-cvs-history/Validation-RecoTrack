import FWCore.ParameterSet.Config as cms

trackerSeedValidator = cms.EDFilter("TrackerSeedValidator",
    associators = cms.vstring('TrackAssociatorByHits'),
    useFabsEta = cms.bool(True),
    minpT = cms.double(0.0),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    min = cms.double(0.0),
    max = cms.double(2.5),
    nintHit = cms.int32(25),
    label = cms.VInputTag(cms.InputTag("newSeedFromTriplets")),
    maxHit = cms.double(25.0),
    TTRHBuilder = cms.string('WithTrackAngle'),
    nintpT = cms.int32(200),
    label_tp_fake = cms.InputTag("cutsTPFake"),
    label_tp_effic = cms.InputTag("cutsTPEffic"),
    useInvPt = cms.bool(False),
    maxpT = cms.double(100.0),
    outputFile = cms.string(''),
#    outputFile = cms.string('validationPlotsSeed.root'),
    minHit = cms.double(0.0),
    sim = cms.string('g4SimHits'),
    nint = cms.int32(25),
#the following parameters  are not used at the moment
#but are needed since the seed validator hinerits from multitrack validator base
#to be fixed.
    minPhi = cms.double(-3.15),
    maxPhi = cms.double(3.15),
    nintPhi = cms.int32(36),
    minDxy = cms.double(0),
    maxDxy = cms.double(5),
    nintDxy = cms.int32(50),
    minDz = cms.double(-10),
    maxDz = cms.double(10),
    nintDz = cms.int32(100),
    ptRes_rangeMin = cms.double(-0.1),                                 
    ptRes_rangeMax = cms.double(0.1),
    phiRes_rangeMin = cms.double(-0.003),
    phiRes_rangeMax = cms.double(0.003),
    cotThetaRes_rangeMin = cms.double(-0.01),
    cotThetaRes_rangeMax = cms.double(+0.01),
    dxyRes_rangeMin = cms.double(-0.01),
    dxyRes_rangeMax = cms.double(0.01),
    dzRes_rangeMin = cms.double(-0.05),
    dzRes_rangeMax = cms.double(+0.05),
    ptRes_nbin = cms.int32(100),                                   
    phiRes_nbin = cms.int32(100),                                   
    cotThetaRes_nbin = cms.int32(120),                                   
    dxyRes_nbin = cms.int32(100),                                   
    dzRes_nbin = cms.int32(150) 
)


