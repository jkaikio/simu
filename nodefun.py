import numpy as np
from graafi import *
import cv2

def NF_Monitor(args, node, draw=False):
    if not "NF_Monitor" in args:
        NFMonitor = Monitor(label = node.label)
        NFMonitor.sourcelabels = list(args.keys())
        args["NF_Monitor"]=NFMonitor
        args["M_reset"]=timedArg(False)
    NFMonitor=args["NF_Monitor"]
    if draw:
        node.image = NFMonitor.Draw()
        return args
    NFMonitor.update(args)
    
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
        self.every_nth=1
        self.ave=1
    
    def update(self,args):
        #dt=self.deltatime #vaihdetaan logiikan pyytämään aikahyppyyn myöhemmin
        #self.sourcelabels = []
        if "M_reset" in args:
            if args["M_reset"][0]:
                self.MonitorData=[]
                args["M_reset"]=timedArg(False)
         
        data=[]
        for l in self.sourcelabels:
            #if (type(args[l]) != bool) and (args[l] is not None)and (type(args[l]) != str):
            #    args[l]=args[l]+np.random.random()-0.5  ##TOIMIIKO??
            data.append(args[l][0])
        self.MonitorData.append(data)
        if "M_nth" in args:
            self.every_nth=int(args["M_nth"][0])
        if "M_ave" in args:
            self.ave = int(args["M_ave"][0])
        return args

    def Draw(self):
        data=np.array(self.MonitorData)
        if self.ave>1:
            Vconv=np.ones(self.ave,dtype=float)/self.ave
            for i in range(len(data[0])):
                if (type(data[0,i]) != bool) and (data[0,i] is not None)and (type(data[0,i]) != str):
                    data[:,i]=np.convolve(data[:,i],Vconv,mode="same")
        data=data[0::self.every_nth]
        data=data[-self.w:]

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

def NF_Environment(args, node, draw=False):
    if not "NF_Environment" in args:
        NFEnvironment = Environment(label = node.label)
        ##NF_Environment.sourcelabels = list(args.keys())
        args["NF_Environment"]=NFEnvironment
    NFEnvironment=args["NF_Environment"]
    if draw:
        node.color = NFEnvironment.bgcolor 
        return args   
    args = NFEnvironment.update(args)

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
        if "Time" in args:
            self.time=float(args["Time"][0])
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
        if "Time" in args:
            args["Time"] = timedArg(self.time)
        return args

def NF_SolarCell(args, node, draw=False): #PIKATESTI...
    if "Lightness" in args:
        args["V_PV"] = timedArg(args["Lightness"][0]*3.0)
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

def NF_Supercap(args, node, draw=False): #PIKATESTI...
    #print("SUPPEERRR")
    if "V_PV" in args:
        V_PV = float(args["V_PV"][0])
        #print(V_PV)
    else: V_PV=0.0
    if "P_Tot_Out" in args:
        P_Out = float(args["P_Tot_Out"][0])
        #print("E",E)
    else: P_Out =0
    if "E_SC" in args:
        E = float(args["E_SC"][0])
        #print("E",E)
    else: E=0.0
    E+=(V_PV*.015 - .02-P_Out)*60 # P=UI, E=P*dt, 
    E = min(E,1000)
    E = max(E,0)
    #print("E",E)
    args["E_SC"]=timedArg(E)
    return args

def NF_Batt(args, node, draw=False): #PIKATESTI...
    #print("SUPPEERRR")
    if "E_Batt" in args:
        E = float(args["E_Batt"][0])
        #print(V_PV)
    else: E=0.0
    if "E_SC" in args:
        E_SC = float(args["E_SC"][0])
        #print("E",E)
    else: E_SC=0.0
    if "P_Tot_Out" in args:
        P_Out = float(args["P_Tot_Out"][0])
        #print("E",E)
    else: P_Out=0.0

    if E_SC<=0:
        E -= P_Out*60# P=UI, E=P*dt, 
        #E = min(E,5000)
        E = max(E,0)
    args["E_Batt"]=timedArg(E)
    return args

   