import numpy as np
import cv2

#functions for Environment and Power
class Environment():  #Template function
    def __init__(self, label="Environment"):
        self.type = "Environment"
        self.label =label
        self.parent = None
        self.inside=False
        self.time=0.0 +100.*24*3600# syyspäivä
        self.deltatime=60.0 #sekunteina 
    
    def update(self):
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
        self.parent.bgcolor=tuple([min(k*lightness*255,255)for k in [.8,1,1.3]])
        self.parent.Sources.alldata["Lightness"] =lightness

    #def Draw(self,im):
    #    pass

    def Resize(self):
        self.parent.sizeSet(np.array([120,35]))    

    #def LBUTTONDOWN(self,x,y):
    #    return True
        
    #def LBUTTONUP(self,x,y):
    #    return True
        
    #def LBUTTONDBLCLK(self,x,y):
    #    return True
    
    #def MOUSEMOVE(self,x,y):
    #    return True
    
    def presentData(self):
        return self.label+": day#:"+str(self.time/(24*3600)) #tekstiä


class Photovoltaic():  #Template function
    def __init__(self, label="SolarCell"):
        self.type = "Photovoltaic"
        self.label =label
        self.parent = None
        self.deltatime=60.0 #sekunteina 
        self.V_PV_Out = 0.0
    
    def update(self):
        dt=self.deltatime #vaihdetaan logiikan pyytämään aikahyppyyn myöhemmin
        L=self.parent.Sources.alldata["Lightness"]
        self.V_PV_Out = L*3.0
        self.parent.bgcolor=tuple([min(k*self.V_PV_Out*50+kk,255)for k,kk in zip([0,1,-1],[100,100,255])])
        self.parent.Sources.alldata["V_PV_Out"] =self.V_PV_Out

    #def Draw(self,im):
    #    pass

    def Resize(self):
        self.parent.sizeSet(np.array([120,35]))    

    #def LBUTTONDOWN(self,x,y):
    #    return True
        
    #def LBUTTONUP(self,x,y):
    #    return True
        
    #def LBUTTONDBLCLK(self,x,y):
    #    return True
    
    #def MOUSEMOVE(self,x,y):
    #    return True
    
    def presentData(self):
        return self.label+": V_out"+str(self.V_PV_Out) #tekstiä

class Supercaps():  #Template function
    def __init__(self, label="Supercaps"):
        self.type = "Supercap"
        self.label =label
        self.parent = None
        self.deltatime=60.0 #sekunteina 
        self.E_SC=0.0
    
    def update(self):
        dt=self.deltatime #vaihdetaan logiikan pyytämään aikahyppyyn myöhemmin
        V_PV=self.parent.Sources.alldata["V_PV_Out"]
        self.E_SC+=(V_PV*.015 - .02)*dt # P=UI, E=P*dt, 
        self.E_SC = min(self.E_SC,1000)
        self.E_SC = max(self.E_SC,0)
        self.parent.bgcolor=tuple([min(k*self.E_SC/5+kk,255)for k,kk in zip([0,1,-1],[100,100,255])])
        self.parent.Sources.alldata["E_SC"] =self.E_SC

    #def Draw(self,im):
    #    pass

    def Resize(self):
        self.parent.sizeSet(np.array([120,35]))    

    #def LBUTTONDOWN(self,x,y):
    #    return True
        
    #def LBUTTONUP(self,x,y):
    #    return True
        
    #def LBUTTONDBLCLK(self,x,y):
    #    return True
    
    #def MOUSEMOVE(self,x,y):
    #    return True
    
    def presentData(self):
        return self.label+": E:"+str(self.E_SC) #tekstiä

class HarvesterCircuitry():  #Template function
    def __init__(self, label="NullFunc"):
        self.type = "NullFunc"
        self.label =label
        self.parent = None
    
    def update(self):
        #main on off
        if  not self.parent.Sources.alldata["Onstate"]:
            return
        
        

        V_PV=self.parent.Sources.alldata["V_PV_Out"]
    


    #def Draw(self,im):
    #    pass

    def Resize(self):
        self.parent.sizeSet(np.array([120,35]))    

    #def LBUTTONDOWN(self,x,y):
    #    return True
        
    #def LBUTTONUP(self,x,y):
    #    return True
        
    #def LBUTTONDBLCLK(self,x,y):
    #    return True
    
    #def MOUSEMOVE(self,x,y):
    #    return True
    
    def presentData(self):
        return self.label #tekstiä
