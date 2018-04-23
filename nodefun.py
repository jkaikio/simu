import numpy as np
from graafi import *
import cv2

def readFloatArg(label,args,ifnotvalue=0.0):
    if label in args:
        variable = float(args[label][0])
    else: variable=ifnotvalue
    return variable    
def readIntArg(label,args,ifnotvalue=0):
    if label in args:
        variable = int(args[label][0])
    else: variable=ifnotvalue
    return variable    
def readBoolArg(label,args,ifnotvalue=False):
    if label in args:
        variable = args[label][0]
        if type(variable)==str:
            variable = eval(variable)
    else: variable=ifnotvalue
    return variable    
def readStrArg(label,args,ifnotvalue=""):
    if label in args:
        variable = str(args[label][0])
    else: variable=ifnotvalue
    return variable   


def NF_Monitor(args, node, draw=False):
    if not "NF_Monitor" in args:
        NFMonitor = Monitor(label = node.label)
        NFMonitor.sourcelabels = list(args.keys())
        args["NF_Monitor"]=NFMonitor
        args["M_reset"]=timedArg(False)
        node.mximsize=0.6
    NFMonitor=args["NF_Monitor"]
    if draw:
        node.image = NFMonitor.Draw()
        return args
    NFMonitor.bgcolor=node.color
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
            data.append(args[l][0])
        self.MonitorData.append(data)
        if "M_nth" in args:
            self.every_nth=int(args["M_nth"][0])
        if "M_ave" in args:
            self.ave = int(args["M_ave"][0])
        return args

    def Draw(self):
        col=np.array(self.bgcolor,dtype=np.uint8)
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

        cv2.line(img,(0,int(self.h/2)),(self.w,int(self.h/2)),colorblend(col,col+128,0.3),2,cv2.LINE_AA)

        for j in range(ld):
            #for i
            #cv2.polylines(img, np.int32([points]), 1, (255,255,255))
            if (type(data[0,j]) != bool) and (data[0,j] is not None)and (type(data[0,j]) != str):
                for i in range(len(data)-1): 
                    color= np.array((int(32*np.sin(8.0*j/(ld+1))),int(32*np.sin(8.0*j/(ld+1))),int(32*np.cos(8.0*j/(ld+1)))),dtype=np.uint8)
                    #color=np.array(color/max(color)*128,dtype=np.uint8)
                    color=col+color+128
                    color=colorblend(color,col,0.2)      
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
        node.mximsize=0.2
    NFEnvironment=args["NF_Environment"]
    if draw:
        node.image= NFEnvironment.Draw()
        return args   
    args = NFEnvironment.update(args,node)

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
        self.time=0.0# +0.*24*3600# syyspäivä
        self.deltatime=60.0 #sekunteina 
        self.bgcolor = (50,20,5)
        self.date=""
        self.clock=""

    def update(self, args, node):
        if "Time" in args:
            self.time=float(args["Time"][0])
        self.time+=self.deltatime #vaihdetaan logiikan pyytämään aikahyppyyn myöhemmin
        tim = self.time
        year=tim/(365*24*3600)
        day_of_year=tim%(365*24*3600)/(24*3600)
        hour_of_day=(tim%(24*3600))/3600
        minute=np.floor((tim%3600)/60)
        second= np.floor((tim%60)/60)
        dt=time.ctime(14850000+tim)[4:-5]
        #print(hour_of_day,minute,second,dt[7:])
        #print(day_of_year,dt[:6])
        self.date=dt[:6]
        self.clock=dt[7:]
        self.date=self.date+" y:"+str(int(year))
        #lightness = max((-1*np.cos(hour_of_day/24*2*np.pi)+\
        #                0.5*np.cos(day_of_year/365*2*np.pi))+\
        #                np.average(np.random.random(5)-0.3),0)
        sunh = AuKorkeus(day_of_year+172,hour_of_day,leveyspiiri=65) #Oulu!!!
        lightness = sd=sigmoid((sunh-7)/2)
        self.bgcolor=tuple([min(k*lightness*255,255)for k in [.8,1,1.3]])
        self.bgcolor = colorblend(node.color, self.bgcolor, 0.4)
        args["Lightness"] = timedArg(lightness)
        if "Time" in args:
            args["Time"] = timedArg(self.time)
        return args

    def Draw(self):
        im=np.ones((120,230,3),dtype=np.uint8)
        im[:,:,0]=self.bgcolor[0]
        im[:,:,1]=self.bgcolor[1]
        im[:,:,2]=self.bgcolor[2]
        col=np.array(self.bgcolor,dtype=np.uint8)
        color=colorblend(col,col+128,0.4)
        cv2.putText(im,self.date,(5,50),cv2.FONT_HERSHEY_SIMPLEX,1.2,color,3)
        cv2.putText(im,self.clock,(5,100),cv2.FONT_HERSHEY_SIMPLEX,1.2,color,3)
        #cv2.putText(im,self.date,(5,50),cv2.FONT_HERSHEY_SIMPLEX,1.2,(255,255,255),4)
        #cv2.putText(im,self.clock,(5,100),cv2.FONT_HERSHEY_SIMPLEX,1.2,(255,255,255),4)
        #cv2.putText(im,self.date,(5,50),cv2.FONT_HERSHEY_SIMPLEX,1.2,(0,0,0),2)
        #cv2.putText(im,self.clock,(5,100),cv2.FONT_HERSHEY_SIMPLEX,1.2,(0,0,0),2)
        return im

def AuKorkeus(vuodenpaiva,kellonaika,leveyspiiri=65):
        fLeveyspiiri=float(leveyspiiri)
        fAkselinkallistus=23.43
        fAkselinkallistus_Nyt=np.cos(float(vuodenpaiva+10)/365*2*np.pi)*fAkselinkallistus
        fSunHeigth=-np.cos(float(kellonaika)/24*np.pi*2)*(90-fLeveyspiiri)-fAkselinkallistus_Nyt
        P=950
        T=0        
        sh=fSunHeigth
        fSunHeigth=sh+P/(273+T)*(0.1594+0.0196*sh+0.00002*sh*sh)/(1+0.505*sh+0.0845*sh*sh) #Ilmakeh�n refraktio
        return fSunHeigth    

def NF_SolarCell(args, node, draw=False): 
    Lightness = readFloatArg("Lightness",args)
    
    Light_to_volt=3.0
    MaxVolt=5
    V_PV = max(min(Lightness*Light_to_volt,MaxVolt),0)
    args["V_PV"] = timedArg(V_PV)
    #print("SolarCell",Lightness,V_PV)
    return args

def switchimage(bgcolor,onstate):
    img=cv2.imread("onoff2.png")
    im=np.ones((428,428,3),dtype=np.uint8)
    
    im[:,:,0]=bgcolor[0]
    im[:,:,1]=bgcolor[1]
    im[:,:,2]=bgcolor[2]
    imB=im[107-22:107-22+236,107:107+214,0]
    imG=im[107-22:107-22+236,107:107+214,1]
    imR=im[107-22:107-22+236,107:107+214,2]
    B=img[:,:,1].copy()
    
    if onstate:
        swcol=colorblend(bgcolor,(0,255,0),0.3)
    else:
        swcol=colorblend(bgcolor,(0,0,255),0.3)
    imB[B<200]=swcol[0]
    imG[B<200]=swcol[1]
    imR[B<200]=swcol[2]    
    im[107-22:107-22+236,107:107+214, 0]=imB.copy()
    im[107-22:107-22+236,107:107+214, 1]=imG.copy()
    im[107-22:107-22+236,107:107+214, 2]=imR.copy()
    return im


def NF_MainSwitch(args, node, draw=False):
    if draw:
        node.image=switchimage(node.color,readBoolArg("OnState_Main",args))
        return args
    if node.maximized:
        OnState_Main = readBoolArg("OnState_Main",args)
        args["OnState_Main"]= timedArg(not OnState_Main)
        node.maximized=False
    return args

def NF_Supercap(args, node, draw=False): #PIKATESTI...
    V_SC         = readFloatArg("V_SC",args)
    E_SC         = readFloatArg("E_SC",args) 
    P_SC_Out     = readFloatArg("P_SC_Out",args)
    P_SC_Out_Req = readFloatArg("P_SC_Out_Req",args)
    P_SC_In      = readFloatArg("P_SC_In",args)

    vuoto = 0.00002*E_SC

    E_SC += (P_SC_In - vuoto - P_SC_Out)*60 # P=UI, E=P*dt, 
    E_SC = min(E_SC,1000)
    E_SC = max(E_SC,0)
    
    args["E_SC"]=timedArg(E_SC)
    return args

def NF_Batt(args, node, draw=False): #PIKATESTI...
    E_Batt       = readFloatArg("E_Batt",args)
    V_Batt       = readFloatArg("V_Batt",args)
    P_Batt       = readFloatArg("P_Batt",args)

    dt=60

    E_Batt -= P_Batt*dt# P=UI, E=P*dt, 
    #E = min(E,5000)
    E_Batt = max(E_Batt,0)
    args["E_Batt"]=timedArg(E_Batt)
    return args


 
def NF_EHarvester(args, node, draw=False): 
    OnState_Main = readBoolArg("OnState_Main",args)
    V_PV         = readFloatArg("V_PV",args)
    V_PV_Out     = readFloatArg("P_PV_Out",args)
    E_Batt       = readFloatArg("E_Batt",args)
    V_Batt       = readFloatArg("V_Batt",args)
    P_Batt       = readFloatArg("P_Batt",args)
    V_SC         = readFloatArg("V_SC",args)
    E_SC         = readFloatArg("E_SC",args) 
    P_SC_Out     = readFloatArg("P_SC_Out",args)
    P_SC_Out_Req = readFloatArg("P_SC_Out_Req",args)
    P_SC_In      = readFloatArg("P_SC_In",args)
    P_To_Reg     = readFloatArg("P_To_Reg",args)
    V_To_Reg     = readFloatArg("V_To_Reg",args)
    P_Tot_Out     = readFloatArg("P_Tot_Out",args)
    V_Tot_Out     = readFloatArg("V_Tot_Out",args)
    TotalEnergy  = readFloatArg("TotalEnergy",args)
    PowerLowAlert = readBoolArg("PowerLowAlert",args)
    PowerShuttingDown = readBoolArg("PowerShuttingDown",args)

    dt=60

    OnState_EHarvester = (E_Batt+E_SC)>0 

    if (V_PV>0) and (not OnState_EHarvester) and OnState_Main: #(PV only)
        P_SC_In = V_PV*.01 #tähän virta...


    if OnState_Main and OnState_EHarvester:
        P_SC_In = V_PV*.015 #tähän virta...

        P_Batt=0.0
        P_SC_Out=0.0
        P_self=0.005

        P_rem = P_To_Reg + P_self #Harvesterin viemä virta...??
        P_SC_Max=0.07
        if E_SC>0:
            P_SC_Out=min(P_rem, P_SC_Max, E_SC/dt)
            P_SC_Out = max(P_SC_Out,0)
            P_rem = P_To_Reg - P_SC_Out
        P_Batt_Max=0.03            
        if E_Batt>0:
            P_Batt = min(P_rem, P_Batt_Max,E_Batt/dt)
            P_Batt = max(P_Batt,0)
            P_rem = P_rem - P_Batt
        
        V_To_Reg = 3.0
        if 0 < P_To_Reg < P_Batt + P_SC_Out:
            V_To_Reg = V_To_Reg * (P_Batt + P_SC_Out)/P_To_Reg
        P_To_Reg = P_Batt + P_SC_Out -P_self

        TotalEnergy = E_SC + E_Batt - P_To_Reg * dt
        Emax=1000
        if E_SC < 0.2*Emax:
            PowerLowAlert=True
        else: 
            PowerLowAlert=False
        if TotalEnergy < 0.02*Emax:
            PowerShuttingDown = True
        else:
            PowerShuttingDown = False

    if (not OnState_Main) or (not OnState_EHarvester):
        TotalEnergy= E_SC + E_Batt
        P_To_Reg =0.0
        P_SC_Out =0.0
        P_Batt =0.0
        PowerShuttingDown = True

    if not OnState_Main:
        P_SC_In =0.0

    #args["OnState_Main"]= timedArg(OnState_Main)
    #args["V_PV"]= timedArg(V_PV)
    #args["V_PV_Out"]= timedArg(V_PV_Out)
    #args["E_Batt"]= timedArg(E_Batt)
    #args["V_Batt"]= timedArg(V_Batt)
    args["P_Batt"]= timedArg(P_Batt)
    #args["V_SC"]= timedArg(V_SC)
    #args["E_SC"]= timedArg(E_SC)
    args["P_SC_Out"]= timedArg(P_SC_Out)
    #args["P_SC_Out_Req"]= timedArg(P_SC_Out_Req)
    args["P_SC_In"]= timedArg(P_SC_In)
    args["P_Tot_Out"]= timedArg(P_To_Reg)
    args["V_Tot_Out"]= timedArg(V_To_Reg)
    args["TotalEnergy"]= timedArg(TotalEnergy)
    args["PowerLowAlert"]= timedArg(PowerLowAlert)
    args["PowerShuttingDown"]= timedArg(PowerShuttingDown)
    return args

def NF_VRegulator(args, node, draw=False):
    
    #P_To_Reg     = readFloatArg("P_To_Reg",args)
    #V_To_Reg     = readFloatArg("V_To_Reg",args)
    #P_Tot_Out     = readFloatArg("P_Tot_Out",args)
    #V_Tot_Out     = readFloatArg("V_Tot_Out",args)
    
    #V_To_Reg = V_Tot_Out
    #P_To_Reg = P_Tot_Out
    #V_Tot_Out = V_Temp
    #P_Tot_Out = P_Temp

    #args["P_To_Reg"]= timedArg(P_To_Reg)
    #args["V_To_Reg"]= timedArg(V_To_Reg)
    #args["P_Tot_Out"]= timedArg(P_Tot_Out)
    #args["V_Tot_Out"]= timedArg(V_Tot_Out)
    return args

#    "Microcontroller":["TotalEnergy","PowerLowAlert","PowerShuttingDown","P_Tot_Out",\
#                       "V_Tot_Out","P_Sensors","Data_Sensors","OnState_Sensors",\
#                       "P_Indicator","OnState_indicator","OnState_Radio","PositioningRadio",\
#                       "RadioMessagePush","RadioMessagePull","NFC"],


def NF_Microcontroller(args, node, draw=False): 
    if not "NF_Microcontroller" in args:
        NFMicrocontroller = Microcontroller(label = node.label)
        #NFMicrocontroller.sourcelabels = list(args.keys())
        args["NF_Microcontroller"]=NFMicrocontroller
        node.mximsize=0.2
        #args["M_reset"]=timedArg(False)
    NFMicrocontroller=args["NF_Microcontroller"]
    if draw:
        node.image = NFMicrocontroller.Draw()
        return args
    NFMicrocontroller.update(args,node)

    return args

class Microcontroller():  #Template function
    def __init__(self, label="Microcontroller"):
        self.type = "Microcontroller"
        self.label =label
        self.parent = None
        self.time = 0.0
        self.deltatime=60.0 #sekunteina 
        self.bgcolor = (200,200,180)
        self.mode="off" #off, shutdown, deepsleep, sleep, energysaving, booting, on
        self.P={"off":0.0,"shutdown":0.005,"deepsleep":0.003,"wakingfromdeepsleep":0.01,\
                "sleep":0.007,"wakingfromsleep":0.01,"energysaving":0.01,"booting":0.01,"ON":0.02} 


    def update(self, args, node):
        P_Tot_Out     = readFloatArg("P_Tot_Out",args)
        V_Tot_Out     = readFloatArg("V_Tot_Out",args)
        TotalEnergy   = readFloatArg("TotalEnergy",args)
        PowerLowAlert = readBoolArg("PowerLowAlert",args)
        PowerShuttingDown = readBoolArg("PowerShuttingDown",args)
        self.mode     = readStrArg("MC_mode",args,"off")
        
        self.bgcolor=node.color
        self.time+=self.deltatime #vaihdetaan logiikan pyytämään aikahyppyyn myöhemmin

        if P_Tot_Out <= 0:
            self.mode="off"

        if self.mode=="off":
            P_Tot_Out=self.P["off"]
            if not PowerShuttingDown:
                self.mode="booting"
                P_Tot_Out=self.P["booting"]
            
        
        elif self.mode=="shutdown":
            P_Tot_Out=self.P["shutdown"]
            self.mode="off"
        
        elif self.mode=="booting":
            P_Tot_Out=self.P["booting"]
            self.mode="ON"

        elif self.mode=="ON":
            P_Tot_Out=self.P["ON"]
            if PowerLowAlert:
                self.mode="energysaving"
                P_Tot_Out= self.P["energysaving"]   
            if PowerShuttingDown:
                self.mode="shutdown"
                P_Tot_Out= self.P["shutdown"]  

        elif self.mode=="energysaving":
            if not PowerLowAlert:
                self.mode="ON" 
            P_Tot_Out= self.P["energysaving"]
            if PowerShuttingDown:
                self.mode="shutdown"
                P_Tot_Out= self.P["shutdown"]  

        args["MC_mode"]= timedArg(self.mode)
        args["P_To_Reg"]= timedArg(P_Tot_Out)
        args["V_To_Reg"]= timedArg(V_Tot_Out)
        return args

    def Draw(self):
        im=np.ones((100,300,3),dtype=np.uint8)
        im[:,:,0]=self.bgcolor[0]
        im[:,:,1]=self.bgcolor[1]
        im[:,:,2]=self.bgcolor[2]
        col=np.array(self.bgcolor,dtype=np.uint8)
        color=colorblend(col,col+128,0.6)
 
        cv2.putText(im,self.mode,(5,70),cv2.FONT_HERSHEY_SIMPLEX,1.2,color,3)
        #cv2.putText(im,self.mode,(5,70),cv2.FONT_HERSHEY_SIMPLEX,1.2,(0,0,0),2)
        return im



