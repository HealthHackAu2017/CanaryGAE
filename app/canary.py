from model import EpisodeModel
from google.appengine.ext import ndb


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def processCSV(csv):
    
    # Fill the store array
    store = []
    idx = list(range(11,20))
    
    for j in idx: store.append([])
    
    for i,line in enumerate(csv.split('\n')):
        currentline = line[:-1].split(",")
        if len(currentline) < 21: continue
        if(i == 0):
            names = ['t'] + [currentline[j] for j in idx]
        else:
            x = [float(currentline[j]) if isfloat(currentline[j]) else float('nan') for j in idx]
            x = [int(currentline[2])]  + x
            store.append(x)
                        
                        
    # Create the data model
    episode = EpisodeModel(user='user id')
    
    for i in range(len(store)):
        if len(store[i]) < 10: continue
        episode.addRecord(store[i][0],
                          store[i][1],
                          store[i][2],
                          store[i][3],
                          store[i][4],
                          store[i][5],
                          store[i][6],
                          store[i][7],
                          store[i][8],
                          store[i][9],
                          0)
    k = episode.put()
    
    return k.urlsafe()
