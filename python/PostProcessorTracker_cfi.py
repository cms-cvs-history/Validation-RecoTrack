import FWCore.ParameterSet.Config as cms

postProcessorTrack = cms.EDAnalyzer("PostProcessor",
    subDirs = cms.untracked.vstring("RecoTrackV/Track/*"),
    efficiency = cms.vstring(
    "effic 'Efficiency vs #eta' num_assoc(simToReco)_eta num_simul_eta",
    "efficPt 'Efficiency vs p_{T}' num_assoc(simToReco)_pT num_simul_pT",
    "effic_vs_hit 'Efficiency vs hit' num_assoc(simToReco)_hit num_simul_hit",
    "fakerate 'Fake rate vs #eta' num_assoc(recoToSim)_eta num_reco_eta fake",
    "fakeratePt 'Fake rate vs p_{T}' num_assoc(recoToSim)_pT num_reco_pT fake",
    "fakerate_vs_hit 'Fake rate vs hit' num_assoc(recoToSim)_hit num_reco_hit fake"
    ),
    resolution = cms.vstring(
                             "cotThetares_vs_eta '#sigma(cot(#theta)) vs #eta' cotThetares_vs_eta",
                             "cotThetares_vs_pt '#sigma(cot(#theta)) vs p_{T}' cotThetares_vs_pt",
                             "h_dxypulleta 'd_{xy} Pull vs #eta' dxypull_vs_eta",
                             "dxyres_vs_eta '#sigma(d_{xy}) vs #eta' dxyres_vs_eta",
                             "dxyres_vs_pt '#sigma(d_{xy}) vs p_{T}' dxyres_vs_pt",
                             "h_dzpulleta 'd_{z} Pull vs #eta' dzpull_vs_eta",
                             "dzres_vs_eta '#sigma(d_{z}) vs #eta' dzres_vs_eta",
                             "dzres_vs_pt '#sigma(d_{z}) vs p_{T}' dzres_vs_pt",
                             "etares_vs_eta '#sigma(#eta) vs #eta' etares_vs_eta",
                             "h_phipulleta '#phi Pull vs #eta' phipull_vs_eta",
                             "h_phipullphi '#phi Pull vs #phi' phipull_vs_phi",
                             "phires_vs_eta '#sigma(#phi) vs #eta' phires_vs_eta",
                             "phires_vs_phi '#sigma(#phi) vs #phi' phires_vs_phi",
                             "phires_vs_pt '#sigma(#phi) vs p_{T}' phires_vs_pt",
                             "h_ptpulleta 'p_{T} Pull vs #eta' ptpull_vs_eta",
                             "h_ptpullphi 'p_{T} Pull vs #phi' ptpull_vs_phi",
                             "ptres_vs_eta '#sigma(p_{T}) vs #eta' ptres_vs_eta",
                             "ptres_vs_phi '#sigma(p_{T}) vs #phi' ptres_vs_phi",
                             "ptres_vs_pt '#sigma(p_{T}) vs p_{T}' ptres_vs_pt",
                             "h_thetapulleta '#theta Pull vs #eta' thetapull_vs_eta",
                             "h_thetapullphi '#theta Pull vs #phi' thetapull_vs_phi"
                             ),
    profile= cms.vstring(
                         "chi2mean 'mean #chi^{2} vs #eta' chi2_vs_eta",
                         "chi2mean_vs_phi 'mean #chi^{2} vs #phi' chi2_vs_phi",
                         "chi2mean_vs_nhits 'mean #chi^{2} vs n. hits' chi2_vs_nhits",
                         "hits_eta 'mean #hits vs eta' nhits_vs_eta",
                         "hits_phi 'mean #hits vs #phi' nhits_vs_phi",
                         "losthits_eta 'mean #lost hits vs #eta' nlosthits_vs_eta"
                         ),
    outputFileName = cms.untracked.string("")
)
