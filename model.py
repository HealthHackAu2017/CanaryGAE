from google.appengine.ext import ndb

class EpisodeModel(ndb.Model):
    
    somedata = ndb.JsonProperty()
    mylist = [[], [], [], [], [], [], [], [], [], [], []]
    
    start_time = ndb.IntegerProperty()
    end_time = ndb.IntegerProperty()
    
    user = ndb.StringProperty()

    def addRecord(self, tnano, ax, ay, az, gx, gy, gz, red, ir, red_filt, ir_filt):
        self.mylist[0].append(tnano)
        self.mylist[1].append(ax)
        self.mylist[2].append(ay)
        self.mylist[3].append(az)
        self.mylist[4].append(gx)
        self.mylist[5].append(gy)
        self.mylist[6].append(gz)
        self.mylist[7].append(red)
        self.mylist[8].append(ir)
        self.mylist[9].append(red_filt)
        self.mylist[10].append(ir_filt)
    
        self.somedata = self.mylist

        if (self.start_time == None): self.start_time = tnano
        self.end_time = tnano
    

    def getData(t_start, t_end, fields):
        return 0
