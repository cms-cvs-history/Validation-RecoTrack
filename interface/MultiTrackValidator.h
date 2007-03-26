#ifndef MultiTrackValidator_h
#define MultiTrackValidator_h

/** \class MultiTrackValidator
 *  Class that prodecs histrograms to validate Track Reconstruction performances
 *
 *  $Date: 2007/03/26 10:13:49 $
 *  $Revision: 1.1 $
 *  \author cerati
 */

#include <memory>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "MagneticField/Engine/interface/MagneticField.h" 
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h" 

#include "SimTracker/TrackAssociation/interface/TrackAssociatorByChi2.h"

#include "DQMServices/Core/interface/DaqMonitorBEInterface.h"
#include "DQMServices/Daemon/interface/MonitorDaemon.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "Validation/RecoTrack/interface/RecoTrackSelector.h"
#include "Validation/RecoTrack/interface/TPEfficiencySelector.h"
#include "Validation/RecoTrack/interface/TPFakeRateSelector.h"

#include <iostream>
#include <string>
#include <TH1F.h>
#include <TH2F.h>

class MultiTrackValidator : public edm::EDAnalyzer {
 public:
  /// Constructor
  MultiTrackValidator(const edm::ParameterSet& pset):
    dbe_(0),
    sim(pset.getParameter<std::string>("sim")),
    label(pset.getParameter< std::vector<std::string> >("label")),
    associators(pset.getParameter< std::vector<std::string> >("associators")),
    out(pset.getParameter<std::string>("out")),
    min(pset.getParameter<double>("min")),
    max(pset.getParameter<double>("max")),
    nint(pset.getParameter<int>("nint")),
    minpT(pset.getParameter<double>("minpT")),
    maxpT(pset.getParameter<double>("maxpT")),
    nintpT(pset.getParameter<int>("nintpT")),
    selectRecoTracks(pset.getParameter<edm::ParameterSet>("RecoTracksCuts")),
    selectTPs4Efficiency(pset.getParameter<edm::ParameterSet>("TPEfficCuts")),
    selectTPs4FakeRate(pset.getParameter<edm::ParameterSet>("TPFakeRateCuts"))
    {
      dbe_ = edm::Service<DaqMonitorBEInterface>().operator->();
    }

  /// Destructor
  ~MultiTrackValidator(){ }

  /// Method called before the event loop
  void beginJob( const edm::EventSetup &);
  /// Method called once per event
  virtual void analyze(const edm::Event&, const edm::EventSetup& );
  /// Method called at the end of the event loop
  void endJob();

 private:

  DaqMonitorBEInterface* dbe_;

  std::string sim;
  std::vector<std::string> label, associators;
  std::string out;
  double  min, max;
  int nint;
  double minpT, maxpT;
  int nintpT;
  
  //sim
  std::vector<MonitorElement*> h_ptSIM, h_etaSIM, h_tracksSIM, h_vertposSIM;

  //1D
  std::vector<MonitorElement*> h_tracks, h_fakes, h_nchi2, h_nchi2_prob, h_hits, h_charge;
  std::vector<MonitorElement*> h_effic, h_fakerate, h_recoeta, h_assoceta, h_assoc2eta, h_simuleta;
  std::vector<MonitorElement*> h_recopT, h_assocpT, h_assoc2pT, h_simulpT;
  std::vector<MonitorElement*> h_pt, h_eta, h_pullTheta,h_pullPhi0,h_pullD0,h_pullDz,h_pullQoverp;

  //2D  
  std::vector<MonitorElement*> chi2_vs_nhits, etares_vs_eta, nrec_vs_nsim;

  //assoc chi2
  std::vector<MonitorElement*> h_assochi2, h_assochi2_prob;

  //chi2 and #hit vs eta: to be used with doProfileX
  std::vector<TH2F*> chi2_vs_eta, nhits_vs_eta, nlosthits_vs_eta;
  std::vector<MonitorElement*>  h_chi2meanh, h_hits_eta, h_losthits_eta;

  //resolution of track params: to be used with fitslicesytool
  std::vector<TH2F*> d0res_vs_eta, ptres_vs_eta, z0res_vs_eta, phires_vs_eta, cotThetares_vs_eta;
  std::vector<MonitorElement*> h_d0rmsh, h_ptrmsh, h_z0rmsh, h_phirmsh, h_cotThetarmsh;

  //pulls of track params vs eta: to be used with fitslicesytool
  std::vector<TH2F*> d0pull_vs_eta, ptpull_vs_eta, z0pull_vs_eta, phipull_vs_eta, thetapull_vs_eta;
  std::vector<MonitorElement*> h_d0pulleta, h_ptpulleta, h_z0pulleta, h_phipulleta, h_thetapulleta;
  
  std::vector< std::vector<double> > etaintervals;
  std::vector< std::vector<double> > pTintervals;
  std::vector< std::vector<int> > totSIMeta,totRECeta,totASSeta,totASS2eta;
  std::vector< std::vector<int> > totSIMpT,totRECpT,totASSpT,totASS2pT;

  edm::ESHandle<MagneticField> theMF;

  std::vector<const TrackAssociatorBase*> associator;
  const TrackAssociatorByChi2 * associatorForParamAtPca;
  RecoTrackSelector selectRecoTracks;
  TPEfficiencySelector selectTPs4Efficiency;
  TPFakeRateSelector selectTPs4FakeRate;
  
  void doProfileX(TH2 * th2, MonitorElement* me){
    if (th2->GetNbinsX()==me->getNbinsX()){
      TH1F * h1 = (TH1F*) th2->ProfileX();
      for (int bin=0;bin!=h1->GetNbinsX();bin++){
	me->setBinContent(bin+1,h1->GetBinContent(bin+1));
	me->setBinError(bin+1,h1->GetBinError(bin+1));
      }
    } else {
      throw cms::Exception("MultiTrackValidator") << "Different number of bins!";
    }    
  }
  
};


#endif
