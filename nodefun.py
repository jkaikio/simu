import numpy as np
from graafi import *
import cv2

def NF_Monitor(args, node):
    if not "NF_Monitor" in args:
        NFMonitor = Monitor(label = node.label)
        NFMonitor.sourcelabels = list(args.keys())
        args["NF_Monitor"]=NFMonitor
    NFMonitor=args["NF_Monitor"]
    NFMonitor.update(args)
    node.image = NFMonitor.Draw()
    #node.image = np.zeros((200,200,3),dtype=np.uint8)
    #cv2.putText(node.image,"MONITOR",(10,120),cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255) ,4)

    return args


class Monitor():  #Template function
    def __init__(self, label="Monitor"):
        self.type = "Monitor"
        self.label =label
        self.parent = None
        #self.deltatime=60.0 #sekunteina 
        self.MonitorData =[]
        #self.monitorImage = None
        self.h=300
        self.w=500
        self.sourcelabels =[]#["V_PV","E_SC","Lightness"]
        self.minimized =False
        self.bgcolor = (50,20,5)
    
    def update(self,args):
        #dt=self.deltatime #vaihdetaan logiikan pyytämään aikahyppyyn myöhemmin
        #self.sourcelabels = []
        data=[]
        for l in self.sourcelabels:
            #if (type(args[l]) != bool) and (args[l] is not None)and (type(args[l]) != str):
            #    args[l]=args[l]+np.random.random()-0.5  ##TOIMIIKO??
            data.append(args[l][0])
        self.MonitorData.append(data)
        return args

    def Draw(self):
        #if not self.minimized:
        data=np.array(self.MonitorData[-self.w:])
        ld=len(data[0])
        mxd=list(np.zeros(ld))
        mnd=list(np.zeros(ld))
        for i in range(ld):
            if (type(data[0,i]) != bool) and (data[0,i] is not None)and (type(data[0,i]) != str):
                mxd[i]=max(data[:,i])
                mnd[i]=min(data[:,i])
                if mnd[i]>0:mnd[i]=0
                if mxd[i]<0:mxd[i]=0
                if mxd[i]>0 and mnd[i]==0:
                    data[:,i]=self.h-data[:,i]/mxd[i]*self.h
                if mxd[i]==0 and mnd[i]<0:
                    data[:,i]=data[:,i]/mnd[i]*self.h
                if mxd[i]>0 and mnd[i]<0:
                    data[:,i]=self.h/2-data[:,i]*2/max(mxd[i],-1*mnd[i])*self.h
        #if len(data)>300: data[:,:300]=data[:,-300:]
        img=np.ones((self.h,self.w,3), np.uint8)
        img[:,:,0]=self.bgcolor[0]
        img[:,:,1]=self.bgcolor[1]
        img[:,:,2]=self.bgcolor[2]

        cv2.line(img,(0,int(self.h/2)),(self.w,int(self.h/2)),(100,40,10),2,cv2.LINE_AA)

        for j in range(ld):
            #for i
            #cv2.polylines(img, np.int32([points]), 1, (255,255,255))
            if (type(data[0,j]) != bool) and (data[0,j] is not None)and (type(data[0,j]) != str):
                for i in range(len(data)-1): 
                    color= (int(215+40*np.sin(6.0*j/ld)),int(191+64*np.cos(6.0*j/ld)),int(191+64*np.cos(6.0*j/ld)))      
                    cv2.line(img,(i,int(data[i,j])),(i+1,int(data[i+1,j])),color,1,cv2.LINE_AA)
                    cv2.putText(img,str(np.round(mnd[j],2))+" < " + self.sourcelabels[j] + " < "+str(np.round(mxd[j],2)),\
                        (10,20+j*30),\
                        cv2.FONT_HERSHEY_SIMPLEX, .5, color )
        return img

def NF_Environment(args, node):
    if not "NF_Environment" in args:
        NFEnvironment = Environment(label = node.label)
        ##NF_Environment.sourcelabels = list(args.keys())
        args["NF_Environment"]=NFEnvironment
    NFEnvironment=args["NF_Environment"]
    args = NFEnvironment.update(args)
    node.color = NFEnvironment.bgcolor
    #node.image = NF_Environment.Draw()
    #node.image = np.zeros((200,200,3),dtype=np.uint8)
    #cv2.putText(node.image,"MONITOR",(10,120),cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255) ,4)

    return args


class Environment():  #Template function
    def __init__(self, label="Environment"):
        self.type = "Environment"
        self.label =label
        self.parent = None
        self.inside=False
        self.time=0.0 +0.*24*3600# syyspäivä
        self.deltatime=60.0 #sekunteina 
        self.bgcolor = (50,20,5)

    def update(self, args):
        self.time+=self.deltatime #vaihdetaan logiikan pyytämään aikahyppyyn myöhemmin
        time =12*3600 + self.time
        year=time/(365*24*3600)
        day_of_year=time%(365*24*3600)/(24*3600)
        hour_of_day=(time%(24*3600))/3600
        minute=np.floor((time%3600)/60)
        second= np.floor((time%60)/60)
        lightness = max((np.cos(hour_of_day/12*np.pi)+\
                        0.5*np.cos(day_of_year/365*2*np.pi))+\
                        np.average(np.random.random(5)-0.3),0)
        self.bgcolor=tuple([min(k*lightness*255,255)for k in [.8,1,1.3]])
        args["Lightness"] = timedArg(lightness)
        return args

def NF_SolarCell(args, node): #PIKATESTI...
    if "Lightness" in args:
        args["V_PV"] = timedArg(args["Lightness"][0])
    #if not "NF_Environment" in args:
    #    NFEnvironment = Environment(label = node.label)
    #    ##NF_Environment.sourcelabels = list(args.keys())
    #    args["NF_Environment"]=NFEnvironment
    #NFEnvironment=args["NF_Environment"]
    #args = NFEnvironment.update(args)
    #node.color = NFEnvironment.bgcolor
    return args

#def NF_MainSwitch(args, node): #PIKATESTI...
#    if "OnStata_Main" in args:
#        args["V_PV"] = timedArg(args["Lightness"][0])
    #if not "NF_Environment" in args:
    #    NFEnvironment = Environment(label = node.label)
    #    ##NF_Environment.sourcelabels = list(args.keys())
    #    args["NF_Environment"]=NFEnvironment
    #NFEnvironment=args["NF_Environment"]
    #args = NFEnvironment.update(args)
    #node.color = NFEnvironment.bgcolor
#    return args

   