#ifndef MultiTrackValidatorBase_h
#define MultiTrackValidatorBase_h

/** \class MultiTrackValidatorBase
 *  Base class for analyzers that produces histrograms to validate Track Reconstruction performances
 *
 *  $Date: 2007/11/13 10:46:45 $
 *  $Revision: 1.33 $
 *  \author cerati
 */

#include <memory>

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "MagneticField/Engine/interface/MagneticField.h" 
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h" 

#include "SimTracker/TrackAssociation/interface/TrackAssociatorByChi2.h"

#include "DQMServices/Core/interface/DaqMonitorBEInterface.h"
#include "DQMServices/Daemon/interface/MonitorDaemon.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "PhysicsTools/RecoAlgos/interface/RecoTrackSelector.h"
#include "PhysicsTools/RecoAlgos/interface/TrackingParticleSelector.h"

#include <iostream>
#include <sstream>
#include <string>
#include <TH1F.h>
#include <TH2F.h>

class MultiTrackValidatorBase {
 public:
  /// Constructor
  MultiTrackValidatorBase(const edm::ParameterSet& pset):
    dbe_(0),
    sim(pset.getParameter<std::string>("sim")),
    label(pset.getParameter< std::vector<edm::InputTag> >("label")),
    label_tp_effic(pset.getParameter< edm::InputTag >("label_tp_effic")),
    label_tp_fake(pset.getParameter< edm::InputTag >("label_tp_fake")),
    associators(pset.getParameter< std::vector<std::string> >("associators")),
    out(pset.getParameter<std::string>("out")),
    min(pset.getParameter<double>("min")),
    max(pset.getParameter<double>("max")),
    nint(pset.getParameter<int>("nint")),
    useFabs(pset.getParameter<bool>("useFabsEta")),
    minpT(pset.getParameter<double>("minpT")),
    maxpT(pset.getParameter<double>("maxpT")),
    nintpT(pset.getParameter<int>("nintpT"))
    {
      dbe_ = edm::Service<DaqMonitorBEInterface>().operator->();
    }
  
  /// Destructor
  virtual ~MultiTrackValidatorBase(){ }
  
  virtual void doProfileX(TH2 * th2, MonitorElement* me){
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

  virtual void doProfileX(MonitorElement * th2m, MonitorElement* me) {
    MonitorElementRootH2 * meh2 = dynamic_cast<MonitorElementRootH2*>(th2m);
    if (!meh2)   {throw cms::Exception("MultiTrackValidator") << "no cast to rootH2"; }
    TH2F * h = dynamic_cast<TH2F*>(&(**meh2));
    if (!h)    {throw cms::Exception("MultiTrackValidator") << "no cast to h2"; }
    doProfileX(h, me);
  }

  virtual double getEta(double eta) {
    if (useFabs) return fabs(eta);
    else return eta;
  }
  
  void fillPlotFromVector(MonitorElement* h, std::vector<int>& vec) {
    for (unsigned int j=0; j<vec.size(); j++){
      h->setBinContent(j+1, vec[j]);
    }
  }

  void fillPlotFromVectors(MonitorElement* h, std::vector<int>& numerator, std::vector<int>& denominator,std::string type){
    double value,err;
    for (unsigned int j=0; j<numerator.size(); j++){
      if (denominator[j]!=0){
	if (type=="effic")
	  value = ((double) numerator[j])/((double) denominator[j]);
	else if (type=="fakerate")
	  value = 1-((double) numerator[j])/((double) denominator[j]);
	else return;
	err = sqrt( value*(1-value)/(double) denominator[j] );
	h->setBinContent(j+1, value);
	h->setBinError(j+1,err);
      }
      else {
	h->setBinContent(j+1, 0);
      }
    }
  }

  void setUpVectors() {
    std::vector<double> etaintervalsv;
    std::vector<double> pTintervalsv;
    std::vector<int>    totSIMveta,totASSveta,totASS2veta,totRECveta;
    std::vector<int>    totSIMvpT,totASSvpT,totASS2vpT,totRECvpT;
    
    double step=(max-min)/nint;
    std::ostringstream title,name;
    etaintervalsv.push_back(min);
    for (int k=1;k<nint+1;k++) {
      double d=min+k*step;
      etaintervalsv.push_back(d);
      totSIMveta.push_back(0);
      totASSveta.push_back(0);
      totASS2veta.push_back(0);
      totRECveta.push_back(0);
    }
    
    etaintervals.push_back(etaintervalsv);
    totSIMeta.push_back(totSIMveta);
    totASSeta.push_back(totASSveta);
    totASS2eta.push_back(totASS2veta);
    totRECeta.push_back(totRECveta);
  
    double steppT = (maxpT-minpT)/nintpT;
    pTintervalsv.push_back(minpT);
    for (int k=1;k<nintpT+1;k++) {
      double d=minpT+k*steppT;
      pTintervalsv.push_back(d);
      totSIMvpT.push_back(0);
      totASSvpT.push_back(0);
      totASS2vpT.push_back(0);
      totRECvpT.push_back(0);
    }
    pTintervals.push_back(pTintervalsv);
    totSIMpT.push_back(totSIMvpT);
    totASSpT.push_back(totASSvpT);
    totASS2pT.push_back(totASS2vpT);
    totRECpT.push_back(totRECvpT);
  }

 protected:

  DaqMonitorBEInterface* dbe_;

  std::string sim;
  std::vector<edm::InputTag> label;
  edm::InputTag label_tp_effic;
  edm::InputTag label_tp_fake;
  std::vector<std::string> associators;
  std::string out;
  double  min, max;
  int nint;
  bool useFabs;
  double minpT, maxpT;
  int nintpT;
  
  edm::ESHandle<MagneticField> theMF;

  std::vector<const TrackAssociatorBase*> associator;

  //sim
  std::vector<MonitorElement*> h_ptSIM, h_etaSIM, h_tracksSIM, h_vertposSIM;

  //1D
  std::vector<MonitorElement*> h_tracks, h_fakes, h_nchi2, h_nchi2_prob, h_hits, h_charge;
  std::vector<MonitorElement*> h_effic, h_efficPt, h_fakerate, h_recoeta, h_assoceta, h_assoc2eta, h_simuleta;
  std::vector<MonitorElement*> h_recopT, h_assocpT, h_assoc2pT, h_simulpT;
  std::vector<MonitorElement*> h_pt, h_eta, h_pullTheta,h_pullPhi0,h_pullD0,h_pullDz,h_pullQoverp;

  //2D  
  std::vector<MonitorElement*> etares_vs_eta, nrec_vs_nsim;

  //assoc hits
  std::vector<MonitorElement*> h_assocFraction, h_assocSharedHit;

  //#hit vs eta: to be used with doProfileX
  std::vector<MonitorElement*> nhits_vs_eta;
  std::vector<MonitorElement*> h_hits_eta;
 
  std::vector< std::vector<double> > etaintervals;
  std::vector< std::vector<double> > pTintervals;
  std::vector< std::vector<int> > totSIMeta,totRECeta,totASSeta,totASS2eta;
  std::vector< std::vector<int> > totSIMpT,totRECpT,totASSpT,totASS2pT;
};


#endif
