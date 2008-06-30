#ifndef SeedValidator_h
#define SeedValidator_h

/** \class SeedValidator
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

class SeedValidator : public edm::EDAnalyzer, protected MultiTrackValidatorBase {
 public:
  /// Constructor
  SeedValidator(const edm::ParameterSet& pset):MultiTrackValidatorBase(pset){
    builderName = pset.getParameter<std::string>("TTRHBuilder");
  }
  
  /// Destructor
  ~SeedValidator(){ }

  /// Method called before the event loop
  void beginRun( const edm::EventSetup &);
  /// Method called once per event
  void analyze(const edm::Event&, const edm::EventSetup& );
  /// Method called at the end of the event loop
  void endRun();
  
 private:
  std::string builderName;
  edm::ESHandle<TransientTrackingRecHitBuilder> theTTRHBuilder;
};


#endif
