#! /usr/bin/env python

import os
import sys
import fileinput
import string

#########################################################
########### User Defined Variables (BEGIN) ##############


### Reference release
<<<<<<< trackingPerformanceValidation.py
RefRelease='CMSSW_5_2_0'
=======
RefRelease='CMSSW_5_2_0_pre5'
>>>>>>> 1.34

### Relval release (set if different from $CMSSW_VERSION)
<<<<<<< trackingPerformanceValidation.py
NewRelease='CMSSW_5_2_0'
=======
NewRelease='CMSSW_5_2_0_pre6'
>>>>>>> 1.34

### startup and ideal sample list

### This is the list of STARTUP-conditions relvals 
startupsamples= [
    'RelValTTbar', 
    'RelValMinBias', 
    'RelValQCD_Pt_3000_3500'
]
### the list can be empty if you want to skip the validation for all the samples
#startupsamples= []

### This is the list of startup relvals (with PileUP)
#startupsamples= ['RelValTTbar_Tauola']


### This is the list of IDEAL-conditions relvals 
startupsamples= [
'RelValMinBias',   ### list of samples to be validated for each pre-release  
<<<<<<< trackingPerformanceValidation.py
#'RelValQCD_Pt_3000_3500',
#'RelValSingleElectronPt35', 
#'RelValTTbar', 
#'RelValSingleMuPt10', 
#'RelValSingleMuPt100',
#'RelValQCD_FlatPt_15_3000',
=======
'RelValQCD_Pt_3000_3500',
'RelValSingleElectronPt35', 
'RelValTTbar', 
'RelValSingleMuPt10', 
'RelValSingleMuPt100',
'RelValQCD_FlatPt_15_3000',
>>>>>>> 1.34
### additional samples to be validated for each mayor release
#'RelValQCD_Pt_80_120',
#'RelValSingleElectronPt10', 
# 'RelValSingleMuPt1', 
# 'RelValSinglePiPt1', 
# 'RelValSinglePiPt10', 
# 'RelValSinglePiPt100', 
#    
]

### the list can be empty if you want to skip the validation for all the samples
idealsamples= []

### This is the list of IDEAL-conditions relvals (with PileUP
#idealsamples= ['RelValZmumuJets_Pt_20_300_GEN']


### Sample version: v1,v2,etc..
Version='v3'
#Version='LowLumiPileUp-v1'
#Version='BX156-v2'
#Version='BX2808-v2'

### Ideal and Statup tags
<<<<<<< trackingPerformanceValidation.py
IdealTag='MC_52_V4A'
StartupTag='START52_V4A'
=======
IdealTag='MC_52_V2'
StartupTag='START52_V2'
>>>>>>> 1.34

<<<<<<< trackingPerformanceValidation.py
RefIdealTag='MC_52_V4A'
RefStartupTag='START52_V4A'
=======
RefIdealTag='MC_52_V1'
RefStartupTag='START52_V1'
>>>>>>> 1.34
### PileUp: "PU" . No PileUp: "noPU"
#PileUp='noPU'
PileUp='noPU'



### Track algorithm name and quality. Can be a list.
<<<<<<< trackingPerformanceValidation.py
Algos= ['ootb']
#Algos= ['ootb', 'iter0', 'iter1','iter2','iter3','iter4','iter5','iter6']
Qualities=['']
#Qualities=['', 'highPurity']
=======
#Algos= ['ootb']
Algos= ['ootb', 'iter0', 'iter1','iter2','iter3','iter4','iter5','iter6']
#Qualities=['']
Qualities=['', 'highPurity']
>>>>>>> 1.34

### Leave unchanged unless the track collection name changes
Tracksname=''

# Sequence. Possible values:
#   -only_validation
#   -re_tracking
#   -digi2track
#   -only_validation_and_TP
#   -re_tracking_and_TP
#   -digi2track_and_TP
#   -harvesting
#   -preproduction
#   -comparison_only


#Sequence='comparison_only'
Sequence='harvesting'
#Sequence='only_validation'



### Default label is GlobalTag_noPU__Quality_Algo. Change this variable if you want to append an additional string.
NewSelectionLabel=''


### Reference and new repository
RefRepository = '/afs/cern.ch/cms/Physics/tracking/validation/MC'
NewRepository = 'new' # copy output into a local folder


### use the following repository only if you have AFS privileges and you know what you are doing

### for preproduction samples:
### RefRepository = '/afs/cern.ch/cms/performance/tracker/activities/reconstruction/tracking_performance/preproduction'
### NewRepository = '/afs/cern.ch/cms/performance/tracker/activities/reconstruction/tracking_performance/preproduction'



### AFS location of central harvesting output. It can be used to avoid running the harvesting by yourself
castorHarvestedFilesDirectory='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/data/RelVal/CMSSW_4_2_x'



### Default Nevents
defaultNevents ='-1'

### Put here the number of event to be processed for specific samples (numbers must be strings) 
### if not specified is defaultNevents:
Events={}
#Events={'RelValTTbar':'4000'}

### template file names. Usually should not be changed.
cfg='trackingPerformanceValidation_cfg.py'
macro='macro/TrackValHistoPublisher.C'

########### User Defined Variables (END) ################
#########################################################





### Reference directory name (the macro will search for ReferenceSelection_Quality_Algo)
ReferenceSelection=RefIdealTag+'_'+PileUp
StartupReferenceSelection=RefStartupTag+'_'+PileUp






#########################################################################
############ Functions

def replace(map, filein, fileout):
    replace_items = map.items()
    while 1:
        line = filein.readline()
        if not line: break
        for old, new in replace_items:
            line = string.replace(line, old, new)
        fileout.write(line)
    fileout.close()
    filein.close()
    
############################################

    
def do_validation(samples, GlobalTag, trackquality, trackalgorithm):
    global Sequence, Version, RefSelection, RefRepository, NewSelection, NewRepository, defaultNevents, Events, castorHarvestedFilesDirectory
    global cfg, macro, Tracksname
    print 'Tag: ' + GlobalTag
    tracks_map = { 'ootb':'general_AssociatorByHits','iter0':'cutsRecoZero_AssociatorByHits','iter1':'cutsRecoFirst_AssociatorByHits','iter2':'cutsRecoSecond_AssociatorByHits','iter3':'cutsRecoThird_AssociatorByHits','iter4':'cutsRecoFourth_AssociatorByHits','iter5':'cutsRecoFifth_AssociatorByHits','iter6':'cutsRecoSixth_AssociatorByHits'}
    tracks_map_hp = { 'ootb':'cutsRecoHp_AssociatorByHits','iter0':'cutsRecoZeroHp_AssociatorByHits','iter1':'cutsRecoFirstHp_AssociatorByHits','iter2':'cutsRecoSecondHp_AssociatorByHits','iter3':'cutsRecoThirdHp_AssociatorByHits','iter4':'cutsRecoFourthHp_AssociatorByHits','iter5':'cutsRecoFifthHp_AssociatorByHits','iter6':'cutsRecoSixthHp_AssociatorByHits'}
    if(trackalgorithm=='iter0' or trackalgorithm=='ootb'):
        mineff='0.5'
        maxeff='1.025'
        maxfake='0.7'
    elif(trackalgorithm=='iter1'):
        mineff='0.0'
        maxeff='0.5'
        maxfake='0.8'
    elif(trackalgorithm=='iter6'):
        mineff='0.0'
        maxeff='0.5'
        maxfake='0.8'
    else:
        mineff='0'
        maxeff='0.1'
        maxfake='0.8'
    #build the New Selection name
    NewSelection=GlobalTag + '_' + PileUp
    if( trackquality !=''):
        NewSelection+='_'+trackquality
    if(trackalgorithm!=''and not(trackalgorithm=='ootb' and trackquality !='')):
        NewSelection+='_'+trackalgorithm
    if(trackquality =='') and (trackalgorithm==''):
        if(Tracksname==''):
            NewSelection+='_ootb'
            Tracks='generalTracks'
        else:
           NewSelection+= Tracks
    if(Tracksname==''):
        Tracks='cutsRecoTracks'
    else:
        Tracks=Tracksname
    NewSelection+=NewSelectionLabel
    listofdatasets = open('listofdataset.txt' , 'w' )
    #loop on all the requested samples
    for sample in samples :
        templatecfgFile = open(cfg, 'r')
        templatemacroFile = open(macro, 'r')
        print 'Get information from DBS for sample', sample
        newdir=NewRepository+'/'+NewRelease+'/'+NewSelection+'/'+sample 
	cfgFileName=sample+GlobalTag
        #check if the sample is already done
        if(os.path.isfile(newdir+'/building.pdf' )!=True):    

            if( Sequence=="harvesting"):
            	harvestedfile='./DQM_V0001_R000000001__' + GlobalTag+ '__' + sample + '__Validation.root'
                print harvestedfile
            elif( Sequence=="preproduction"):
                harvestedfile='./DQM_V0001_R000000001__' + sample+ '-' + GlobalTag + '_preproduction_312-v1__GEN-SIM-RECO_1.root'
            elif( Sequence=="comparison_only"):
                harvestedfile='./DQM_V0001_R000000001__' + sample+ '__' + NewRelease+ '-' +GlobalTag + '-v1__GEN-SIM-RECO.root'
                cpcmd='rfcp '+ castorHarvestedFilesDirectory +'/' + harvestedfile + ' .'
                returncode=os.system(cpcmd)
                if (returncode!=0):
                    print 'copy of harvested file from castor for sample ' + sample + ' failed'
                    continue
            #search the primary dataset
            cmd='dbsql "find  dataset where dataset like /'
            cmd+=sample+'/'+NewRelease+'-'+GlobalTag+'*'+Version+'/GEN-SIM-RECO order by dataset.createdate "'
            cmd+='|grep '+sample+'|grep -v test|tail -1'
            print cmd
            dataset= os.popen(cmd).readline().strip()
            print 'DataSet:  ', dataset, '\n'

            #Check if a dataset is found
            if dataset!="":
                    listofdatasets.write(dataset)
                    #Find and format the list of files
                    cmd2='dbsql "find file where dataset like '+ dataset +'"|grep ' + sample
                    filenames='import FWCore.ParameterSet.Config as cms\n'
                    filenames+='readFiles = cms.untracked.vstring()\n'
                    filenames+='secFiles = cms.untracked.vstring()\n'
                    filenames+='source = cms.Source ("PoolSource",fileNames = readFiles, secondaryFileNames = secFiles)\n'
                    filenames+='readFiles.extend( [\n'
                    first=True
                    print cmd2
                    for line in os.popen(cmd2).readlines():
                        filename=line.strip()
                        if first==True:
                            filenames+="'"
                            filenames+=filename
                            filenames+="'"
                            first=False
                        else :
                            filenames+=",\n'"
                            filenames+=filename
                            filenames+="'"
                    filenames+=']);\n'

                    # if not harvesting find secondary file names
                    if(Sequence!="preproduction"):
                            cmd3='dbsql  "find dataset.parent where dataset like '+ dataset +'"|grep ' + sample
                            parentdataset=os.popen(cmd3).readline()
                            print 'Parent DataSet:  ', parentdataset, '\n'

                    #Check if a dataset is found
                            if parentdataset!="":
                                    cmd4='dbsql  "find file where dataset like '+ parentdataset +'"|grep ' + sample 
                                    filenames+='secFiles.extend( [\n'
                                    first=True

                                    for line in os.popen(cmd4).readlines():
                                        secfilename=line.strip()
                                        if first==True:
                                            filenames+="'"
                                            filenames+=secfilename
                                            filenames+="'"
                                            first=False
                                        else :
                                            filenames+=",\n'"
                                            filenames+=secfilename
                                            filenames+="'"
                                    filenames+='\n ]);\n'
                            else :
                                    print "No primary dataset found skipping sample: ", sample
                                    continue
                    else :
                            filenames+='secFiles.extend( (               ) )'

                    cfgFile = open(cfgFileName+'.py' , 'w' )
                    cfgFile.write(filenames)

                    if (Events.has_key(sample)!=True):
                            Nevents=defaultNevents
                    else:
                            Nevents=Events[sample]
                    thealgo=trackalgorithm
                    thequality=trackquality
                    if(trackalgorithm=='ootb'):
                        thealgo=''
                    if(thealgo!=''):
                        thealgo='\''+thealgo+'\''
                    if(trackquality!=''):
                        thequality='\''+trackquality+'\''
                    symbol_map = { 'NEVENT':Nevents, 'GLOBALTAG':GlobalTag, 'SEQUENCE':Sequence, 'SAMPLE': sample, 'ALGORITHM':thealgo, 'QUALITY':thequality, 'TRACKS':Tracks}


                    cfgFile = open(cfgFileName+'.py' , 'a' )
                    replace(symbol_map, templatecfgFile, cfgFile)
                    if(( (Sequence=="harvesting" or Sequence=="preproduction" or Sequence=="comparison_only") and os.path.isfile(harvestedfile) )==False):
                        # if the file is already harvested do not run the job again
                        #cmdrun='cmsRun ' +cfgFileName+ '.py >&  ' + cfgFileName + '.log < /dev/zero '
                        cmdrun='cmsRun ' +cfgFileName+ '.py'
                        retcode=os.system(cmdrun)
                    else:
                        retcode=0

            else:      
                    print 'No dataset found skipping sample: '+ sample, '\n'  
                    continue

            if (retcode!=0):
                    print 'Job for sample '+ sample + ' failed. \n'
            else:
                    if (Sequence=="harvesting" or Sequence=="preproduction" or Sequence=="comparison_only"):
                            #copy only the needed histograms
                            if(trackquality==""):
                                    print "Copying DQM file"
                                    rootcommand='root -b -q -l CopySubdir.C\\('+ '\\\"'+harvestedfile+'\\\",\\\"val.' +sample+'.root\\\",\\\"'+ tracks_map[trackalgorithm]+ '\\\"\\) >& /dev/null'
                                    #rootcommand='root -b -q -l CopySubdir.C\\('+ '\\\"'+harvestedfile+'\\\",\\\"val.' +sample+'.root\\\",\\\"'+ tracks_map[trackalgorithm]+ '\\\"\\)'
                                    os.system(rootcommand)
                            elif(trackquality=="highPurity"):
                                    print "Copying DQM file"
                                    os.system('root -b -q -l CopySubdir.C\\('+ '\\\"'+harvestedfile+'\\\",\\\"val.' +sample+'.root\\\",\\\"'+ tracks_map_hp[trackalgorithm]+ '\\\"\\) >& /dev/null')
                                    #os.system('root -b -q -l CopySubdir.C\\('+ '\\\"'+harvestedfile+'\\\",\\\"val.' +sample+'.root\\\",\\\"'+ tracks_map_hp[trackalgorithm]+ '\\\"\\)')


                    referenceSample=RefRepository+'/'+RefRelease+'/'+RefSelection+'/'+sample+'/'+'val.'+sample+'.root'
                    if os.path.isfile(referenceSample ):
                            replace_map = { 'NEW_FILE':'val.'+sample+'.root', 'REF_FILE':RefRelease+'/'+RefSelection+'/val.'+sample+'.root', 'REF_LABEL':sample, 'NEW_LABEL': sample, 'REF_RELEASE':RefRelease, 'NEW_RELEASE':NewRelease, 'REFSELECTION':RefSelection, 'NEWSELECTION':NewSelection, 'TrackValHistoPublisher': cfgFileName, 'MINEFF':mineff, 'MAXEFF':maxeff, 'MAXFAKE':maxfake}

                            if(os.path.exists(RefRelease+'/'+RefSelection)==False):
                                    os.makedirs(RefRelease+'/'+RefSelection)
                            os.system('cp ' + referenceSample+ ' '+RefRelease+'/'+RefSelection)  
                    else:
                            print "No reference file found at: ", RefRelease+'/'+RefSelection
                            replace_map = { 'NEW_FILE':'val.'+sample+'.root', 'REF_FILE':'val.'+sample+'.root', 'REF_LABEL':sample, 'NEW_LABEL': sample, 'REF_RELEASE':NewRelease, 'NEW_RELEASE':NewRelease, 'REFSELECTION':NewSelection, 'NEWSELECTION':NewSelection, 'TrackValHistoPublisher': cfgFileName, 'MINEFF':mineff, 'MAXEFF':maxeff, 'MAXFAKE':maxfake}


                    macroFile = open(cfgFileName+'.C' , 'w' )
                    replace(replace_map, templatemacroFile, macroFile)


                    os.system('root -b -q -l '+ cfgFileName+'.C'+ '>  macro.'+cfgFileName+'.log')


                    if(os.path.exists(newdir)==False):
                            os.makedirs(newdir)

                    print "moving pdf files for sample: " , sample
                    os.system('mv  *.pdf ' + newdir)

                    print "moving root file for sample: " , sample
                    os.system('mv val.'+ sample+ '.root ' + newdir)

                    print "copy py file for sample: " , sample
                    os.system('cp '+cfgFileName+'.py ' + newdir)
	
	
        else:
            print 'Validation for sample ' + sample + ' already done. Skipping this sample. \n'




##########################################################################
#########################################################################
######## This is the main program
if(NewRelease==''): 
    try:
        #Get some environment variables to use
        NewRelease     = os.environ["CMSSW_VERSION"]
        
    except KeyError:
        print >>sys.stderr, 'Error: The environment variable CMSSW_VERSION is not available.'
        print >>sys.stderr, '       Please run cmsenv'
        sys.exit()
else:
    try:
        #Get some environment variables to use
        os.environ["CMSSW_VERSION"]
        
    except KeyError:
        print >>sys.stderr, 'Error: CMSSW environment variables are not available.'
        print >>sys.stderr, '       Please run cmsenv'
        sys.exit()



NewSelection=''

for algo in Algos:
    for quality in Qualities:
        RefSelection=ReferenceSelection
        if( quality !=''):
            RefSelection+='_'+quality
        if(algo!=''and not(algo=='ootb' and quality !='')):
            RefSelection+='_'+algo
        if(quality =='') and (algo==''):
            RefSelection+='_ootb'
        do_validation(idealsamples, IdealTag, quality , algo)
        RefSelection=StartupReferenceSelection
        if( quality !=''):
            RefSelection+='_'+quality
        if(algo!=''and not(algo=='ootb' and quality !='')):
            RefSelection+='_'+algo
        if(quality =='') and (algo==''):
            RefSelection+='_ootb'
        do_validation(startupsamples, StartupTag, quality , algo)
        
