from PO_Peaks import *
import datetime
import sys
import subprocess


def classify_and_sort_files(listoffiles, tcffile, ResultTypeAsString):
    classifieddf= pdd.DataFrame(columns=['Scenario','Frequency','Duration','TP','File'])
    #tcffile=fullpath to tcf file
    #ResultTypeAsString = '_h_Max' or '_PO' or '_d_Max'
    FreqClasses, CCClasses, DurClasses, TPClasses = Eventdefn (tcffile)
    tcffilename= filenameonly (tcffile)
    for eachfile in listoffiles:
        filestring = filenameonly (eachfile).replace (tcffilename,'').replace (ResultTypeAsString,'')
        freq,remainingtext = eventclassify(filestring,FreqClasses)
        dur,remainingtext = eventclassify(remainingtext,DurClasses)
        tp,remainingtext = eventclassify(remainingtext,TPClasses)
        scn='_'.join (remainingtext.replace ('_',' ').replace('+',' ').split()) #everything else is scenarios, replace  all +, space and _ from file name with _
        classifieddf.loc[len(classifieddf)]=[scn,freq,dur,tp,eachfile]  
    return classifieddf.sort_values(['Scenario','Frequency','Duration','TP'])

def grid_name (Event_details,Stattype):
    filename = Stattype+"_"+"_".join (Event_details)


def asc2asc (asc2ascexe, Operation,outputfolder,listofinput,eventsAsList):
    outfilename = "_". join (eventsAsList)
    outputfilepath =os.path.join (outputfolder,outfilename)
    inputgrids = ' '.join ('"'+infile+'"' for infile in listofinput)
    commandline = r'"'+asc2ascexe+'"' +' -b'+' -out '+ '"'+(outputfilepath+'.flt')+'"'+' -stat'+Operation + ' '+ inputgrids
    print (commandline)
    subprocess.run(commandline)
    return outputfilepath+'_'+Operation+'_Val.flt'

def Depthpostprocessdir(resultsdir):
    clrscr()
    postprocessfolder= os.path.join (resultsdir,'_Postprocess_d_'+datetime.datetime.now().strftime("%B%d"))
    try:
        os.mkdir(postprocessfolder)
    except:
        print ('Postprocess Folder already exists')
    print ('Saving postprocess results to: ', postprocessfolder)
    return postprocessfolder

def createsubfolder (parent, subfolderaslist):
    clrscr()
    subfolder=parent
    for item in subfolderaslist:
        subfolder= os.path.join (subfolder, item)
    try:
        os.makedirs(subfolder)
    except:
        pass
    print ('Saving Results to: ', subfolder)
    return subfolder



tcffile = sys.argv[1]#read in the arguments from batch file, 0 is the .py file itself
Resultsfolder= sys.argv[2]
ascexe= sys.argv[3]


postprfolder= Depthpostprocessdir (Resultsfolder)

######GET LIST OF FILES CONTAINING THE KEYWORD########

listofresults = findfiles (Resultsfolder,['_d_Max.flt'],[''])
classifiedresults=classify_and_sort_files(listofresults, tcffile, '_d_Max')
classifiedresults.to_csv (os.path.join (postprfolder, 'Depthgrids.csv'), index=False)

for grbyscnr in classifiedresults.groupby ('Scenario'):
    for grbyfr in grbyscnr[1].groupby ('Frequency'):
            Medgridlist=[]
            for grbydur in grbyfr[1].groupby ('Duration'):
                medianfolder= createsubfolder (postprfolder,[grbyscnr[0], grbyfr[0]])
                eventsAsList=[grbyfr[0],grbydur[0]]
                inputgrids= (grbydur[1].File).to_list()
                Medgrid = asc2asc (ascexe,'Median',medianfolder,inputgrids,eventsAsList)
                Medgridlist.append (Medgrid)
                #end of duration medians with Medgridlist
            maxofmedfolder= createsubfolder (postprfolder,[grbyscnr[0]])
            eventsAsList=[grbyfr[0]]
            Medgrid = asc2asc (ascexe,'Max',maxofmedfolder,Medgridlist,eventsAsList)
 
