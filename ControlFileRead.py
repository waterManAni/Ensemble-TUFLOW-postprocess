from Directory_Scanner import *

def get_dir (controlfile, relativepath):
    orig_dir = os.getcwd ()
    controlfileparent,controlfilename = os.path.split (controlfile)
    relativefileparent,relativefilename = os.path.split (relativepath)
    os.chdir (controlfileparent)
    try:
        if (len(relativefileparent)>0): #if controlfile and relativefile are in different sub-directory or directory up
            os.chdir (relativefileparent)
            resultdir = os.path.join (os.getcwd(), relativefilename)
        else:
            resultdir = os.path.join (os.getcwd(), relativefilename) #if controlfile and relativefile are in same directory
        os.chdir (orig_dir)
        return (resultdir)
    except:
        print ('Could not find: '+ relativefileparent)

def clrscr():
    print("\033[H\033[J")
    os.system ('cls')

def striplist (listofstrings):
    cleanedlist=[]
    for item in listofstrings:
        cleanedlist.append(item.strip())
    return cleanedlist
        

def TF_cmd_read (filepath):
    fileread= open (filepath,'r')
    commands =[]
    for command in fileread:
        execline= command.split('!')[0] #split out all the commented section !, anything before is item[0]
        execline= execline.strip() #strip removes all whitespaces like space and \n at start and end of string
        if len(execline)>0:
            splitCmds = execline.split ('==',1) #split out by before and after == as index 0 and 1
            splitcmd = striplist(splitCmds)
            if len (splitcmd)>1:
                splitcmd [1]= striplist(splitcmd[1].split ('|'))
            commands.append (splitcmd)
    return commands #returns the tcf command split to list of list with: first part before == as string, second part as list of options
#example [['If Scenario', ['HPC','SGS']],['GIS Format', [SHP]],........]


def containsanystring (string, includetexts):
    contain_TF=1
    if len (''.join(includetexts))>0: #if any strings are passed inside includetexts
        contains=[x.upper () for x in includetexts] #CONVERT EVERYTHING TO UPPER CASE FOR NON CASE SENSITIVE
        contain_TF= any(substring in string.upper() for substring in contains) #TRUE IF ANY INCLUDETEXTS ARE CONTAINED IN THE STRING
        return contain_TF

def Eventdefn (tcf):
    tcfdf = pdd.DataFrame (TF_cmd_read(tcf),columns=['Command','Values'])
    Eventfiledf = tcfdf[(tcfdf.Command == 'Event File')] #filter out all the lines containing "Event File ==" command
    r,c=Eventfiledf.shape
    Eventdefinitions=[]
    for i in range(r):
        Eventfilelist = Eventfiledf.values[i][1]
        Eventfileloc = get_dir (tcf, Eventfilelist[0])
        [Eventdefinitions. append(a) for a in TF_cmd_read (Eventfileloc)]
    
    ECFDF=pdd.DataFrame (Eventdefinitions,columns=['Command','Values'])
    EventDF= ECFDF[(ECFDF.Command =='BC Event Source')]
    Eventcategories=pdd.DataFrame(EventDF.Values.to_list(), columns=['Type', 'Values'])
    
    
    FreqClasses= list(dict.fromkeys((Eventcategories [Eventcategories.Type.str.contains('AEP|ARI')]).Values.to_list()))
    DurClasses= list(dict.fromkeys((Eventcategories [Eventcategories.Type.str.contains('DUR|dur')]).Values.to_list()))
    TPClasses= list(dict.fromkeys((Eventcategories [Eventcategories.Type.str.contains('TP|tp')]).Values.to_list()))
    CCClasses=list(dict.fromkeys((Eventcategories [Eventcategories.Type.str.contains('CC|cc')]).Values.to_list()))
    return (FreqClasses, CCClasses, DurClasses, TPClasses)

    
        

