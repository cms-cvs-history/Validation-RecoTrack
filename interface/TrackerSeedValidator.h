#ifndef TrackerSeedValidator_h
#define TrackerSeedValidator_h

/** \class TrackerSeedValidator
 *  Class that prodecs histrograms to validate Track Reconstruction performances
 *
 *  $Date: 2008/02/11 15:02:11 $
 *  $Revision: 1.1 $
 *  \author cerati
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "Validation/RecoTrack/interface/MultiTrackValidatorBase.h"

#include "TrackingTools/TransientTrackingRecHit/interface/TransientTrackingRecHitBuilder.h"
#include "RecoTracker/TransientTrackingRecHit/interface/TkTransientTrackingRecHitBuilder.h"

class TrackerSeedValidator : public edm::EDAnalyzer, protected MultiTrackValidatorBase {
 public:
  /// Constructor
  TrackerSeedValidator(const edm::ParameterSet& pset):MultiTrackValidatorBase(pset){
    builderName = pset.getParameter<std::string>("TTRHBuilder");
  }
  
  /// Destructor
  ~TrackerSeedValidator(){ }

  /// Method called before the event loop
  void beginJob( const edm::EventSetup &);
  /// Method called once per event
  void analyze(const edm::Event&, const edm::EventSetup& );
  /// Method called at the end of the event loop
  void endJob();
  
 private:
  std::string builderName;
  edm::ESHandle<TransientTrackingRecHitBuilder> theTTRHBuilder;
};


#endif
