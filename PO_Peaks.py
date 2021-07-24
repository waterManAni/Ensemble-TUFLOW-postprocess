import csv
from ControlFileRead import *

def read_csv (filepathname, separator, skip_row, header_row, skip_cols):
    returncsv = pdd. read_csv (filepathname, sep= separator, skiprows = skip_row,header=header_row)
    
    if skip_cols >0: #loop through the columns and delete them
        for d in range (skip_cols): #range extends from 0, which is the first column to skip_cols-1 (which is the nth column)
            returncsv.drop(returncsv.columns[0], axis=1, inplace=True) #drop it like it's cold, inplace=true basically modifies the returncsv itself without returning anything
        return returncsv
    else:
        return returncsv

def empty_csv (emptycsvfilename,header):
    with open(emptycsvfilename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer =None
        return emptycsvfilename


def filenameonly (filepath):
    filenameonly = os.path.splitext (os.path.basename (filepath))[0]
    return filenameonly


def eventclassify (stringname, classes):
    strname= stringname.upper() # all text before _ are classified as events).upper()
    classescaps = [x.upper () for x in classes]
    for c in classescaps:
       if strname.find (c)>-1:
           event = c
           remainingtext= strname.replace (event,'')
           break
       else:
           event=''
           remainingtext=strname
    return event, remainingtext


def Save_PO_Peaks (tcffile, outputfolder, csvlist_file, CSV_Peaks):
    tcffilename= filenameonly (tcffile)
    FreqClasses, CCClasses, DurClasses, TPClasses = Eventdefn (tcffile)
    
    directory_scan (['_PO.csv'],[''],outputfolder, csvlist_file)
    csvlistfile = read_csv (csvlist_file,",",0,0,0)#Read the csv containing list of csv files
    
    r,c=csvlistfile.shape
    empty_csv(CSV_Peaks, ['Flow_Location', 'Peak','File','Scenarios', 'Frequency', 'Duration', 'tp']) #create empty csv with the filename and given headers
    for i in range (r):
        skip_row = 0 #csvlistfile.values[i][1]
        skip_column = 2 #csvlistfile.values[i][2]
        PO_File_name = csvlistfile.values[i][0]
       
        filestring = (filenameonly (PO_File_name).replace (tcffilename,'')).replace ('_PO','')
        Freq,remainingtext = eventclassify(filestring,FreqClasses)
        Duration,remainingtext = eventclassify(remainingtext,DurClasses)
        TP,remainingtext = eventclassify(remainingtext,TPClasses)
        scenarios='_'.join (remainingtext.replace ('_',' ').replace('+',' ').split()) #everything else is scenarios, replace  all +, space and _ from file name with _
        
        PO_file = read_csv (PO_File_name, ",",skip_row,[0,1],skip_column)
        PO_file.columns = PO_file.columns.map('_'.join)
        
        max_flow = PO_file.max(axis = 0, skipna = True).to_frame()
        max_flow = max_flow.assign(file=PO_File_name,sc=scenarios, aepari=Freq,dur=Duration,tempp=TP)
        clrscr()
        print ("there are: ",r," Combinations of runs")
        print ("Appending ", i+1, " of ", r," : ", PO_File_name)
        max_flow.to_csv(CSV_Peaks, mode='a', header=False)

    










