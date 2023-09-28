from PO_Peaks import *
import datetime
import sys
from Stat_Plot import *



def PO_Stat(TP_peaks): #this function will extract min, max and median peak for peaks in the dataframe and also return corresponding event/scenario and relevant _PO.csv file
    statlist=[]
    TP_peaks.sort_values ('Peak',inplace=True)
    r=len (TP_peaks.index)
    medianpos=int(r / 2) + 1 #round up if odd, +1 if even
    looplist = ['Scenarios','Flow_Location','Frequency','Duration','tp','File']
    for f in looplist:
        statlist.append(TP_peaks[f].iloc[medianpos-1])
    statlist.append(TP_peaks['Peak'].iloc[medianpos-1])
    statlist.append(TP_peaks['Peak'].iloc[0])
    statlist.append(TP_peaks['Peak'].iloc[-1])
    return statlist

def POpostprocessdir(resultsdir):
    clrscr()
    postprocessfolder= os.path.join (resultsdir,'_Postprocess_PO_'+datetime.datetime.now().strftime("%B%d"))
    try:
        os.mkdir(postprocessfolder)
        os.mkdir(os.path.join(postprocessfolder,'plots'))
    except:
        print ('Postprocess Folder already exists')
    print ('Saving postprocess results to: ', postprocessfolder)
    return postprocessfolder


clrscr()
tcffile = sys.argv[1]#read in the arguments from batch file, 0 is the .py file itself
Resultsfolder= sys.argv[2]




postprocessfolder = POpostprocessdir (Resultsfolder)


PO_Resultfile = os.path.join (postprocessfolder,('PO_List_.csv'))
PO_Peakfile = os.path.join (postprocessfolder,('Peaks.csv'))
PO_Statsfile= os.path.join (postprocessfolder,('Stats.csv'))

Save_PO_Peaks (tcffile, Resultsfolder, PO_Resultfile, PO_Peakfile)



PO_peaks=read_csv (PO_Peakfile,',',0,0,0)
statdf= pdd.DataFrame(columns=['Scenario','Location','Freq','Tcrit', 'Median_TP',
                              'Median_File','Median_Q','Min_Q','Max_Q'])


for grbyscenarios in PO_peaks.groupby ('Scenarios'):
    for grbyloc in grbyscenarios[1].groupby ('Flow_Location'):
        for grbyfr in grbyloc[1].groupby ('Frequency'):
            AppendStat=[]
            for grbydur in grbyfr[1].groupby ('Duration'):
                TPStat = PO_Stat(grbydur[1])
                try:
                    if TPStat[6]>AppendStat[6]:
                        AppendStat=TPStat
                except:
                    AppendStat=TPStat #if appendstat is empty, just get first group of stats i.e. first duration in a frequency group
            statdf.loc[len(statdf)]=AppendStat              
                
statdf.to_csv(PO_Statsfile,index=False)
 
clrscr()
save_plots (PO_Statsfile, os.path.join(postprocessfolder,'plots'))