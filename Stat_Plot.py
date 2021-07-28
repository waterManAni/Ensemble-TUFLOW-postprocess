from PO_Peaks import *  
import os
from matplotlib import pyplot as plt

def save_plots (statscsv, outputfolder):
    stats=read_csv(statscsv,',',0,0,0)
    for grbyloc in stats.groupby('Location'):
        location= grbyloc[0]
        statlist=grbyloc[1]
        r,c=statlist.shape
        fig = plt.figure()
        
        for i in range (r):
            PO_file= read_csv(statlist['Median_File'].iloc[i],',',0,[0,1],1)
            PO_file.columns = PO_file.columns.map('_'.join)
            time = (PO_file.iloc[:,0]).to_list()
            values = (PO_file[location]).to_list()
            
            labeltext=''
            for labl in ['Freq','Scenario']:
                labeltext= labeltext+str(statlist[labl].iloc[i])+' '
            labeltext=labeltext.lower()+' ('+str(round(statlist['Median_Q'].iloc[i],2))+')'
            plt.plot (time,values,label=labeltext)
        plt.xlabel ('Time',fontsize=16)
        plt.ylabel('Values',fontsize=16)
        plt.legend (loc='best')
        outfig = os.path.join (outputfolder,location+'.jpg')
        fig.savefig(outfig,bbox_inches="tight")
        plt.close('all')