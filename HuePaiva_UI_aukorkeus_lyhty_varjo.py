# -*- coding: cp1252 -*-
import math
import time
fPi=float(355.0)/float(113)
import random
import time
import httplib
import urllib2
hueaddress="192.168.0.100"
conn = httplib.HTTPConnection(hueaddress)

fSHlim=math.cos(84.0/180*fPi) #math.cos(88.5/180*fPi)

def CopyList(list1,list2,plus,times):
        #list2=[0.0]*len(list1)
        for i in range(len(list1)):
                list2[i]=(list1[i]+plus)*times
        #return(list2)

##########GetHuefunktiot

def GetHueXY(lightid, getx, gety,getbri):
        #getx=[0.0]*len(lightid)
        #gety=[0.0]*len(lightid)
        #getbri=[0.0]*len(lightid)
        #print lightid
        for i in range(len(lightid)):
        
                conn.request("GET","/api/newdeveloper/lights/"+lightid[i])
                r1=conn.getresponse()
                data=r1.read()
                #print data

                xy=data[data.find("[")+1:data.find("]")]
                getx[i]=float(xy[0:xy.find(",")])
                gety[i]=float(xy[xy.find(",")+1:100])
                getbri[i]=float(data[data.find("bri")+5:data.find("hue")-2])
        #print getx, gety, getbri
        #return(getx,gety,getbri)

def GetHueName(lightid, getname,getreach):
        #getx=[0.0]*len(lightid)
        #gety=[0.0]*len(lightid)
        #getbri=[0.0]*len(lightid)
        #print lightid
        for i in range(len(lightid)):
                try:
                        conn.request("GET","/api/newdeveloper/lights/"+lightid[i])
                        r1=conn.getresponse()
                        data=r1.read()
                        #print data
                        j=data.find("name")
                        j=data.find(":",j)
                        j=data.find('"',j)+1
                        je=data.find('"',j)
                        getname[i]=data[j:je]
                        j=data.find("reachable")
                        j=data.find(":",j)
                        j=data.find("e",j)
                        #print data[j:j+5]
                        getreach[i]=(data[j-1]=="u") #trUe vs falSe
                except:
                        print "ERROR: Lampun "+lightid[i]+" tietoja ei pystytty lukemaan"
        #print getname, getreach

        #print getx, gety, getbri
        #return(getx,gety,getbri)

def SetHueName(id, setname):
        for i in range(len(id)):
                lname ='"name":"'+setname[i]+'"'
                hue_body="{"+lname+"}"        
                try:
                        hue_address="/api/newdeveloper/lights/"+id[i]
                        conn.request("PUT",hue_address,hue_body)
                        r1=conn.getresponse()
                        #data = r1.read()
                        #print data             
                except:
                        print "ERROR: Lampun "+id[i]+" nimea ei pystytty asettamaan"

def GetHueButtonevent():
        #getx=[0.0]*len(lightid)
        #gety=[0.0]*len(lightid)
        #getbri=[0.0]*len(lightid)
        #print lightid
        try:
                conn.request("GET","/api/newdeveloper/sensors/2")
                r1=conn.getresponse()
                data=r1.read()
                #print data
                j=data.find("buttonevent")
                j=data.find(":",j)
                je=data.find(',',j)
                data1=data[j+1:je]
                j=data.find("lastupdated")
                j=data.find(":",j)
                j=data.find('"',j)
                je=data.find('"',j+1)
                data=data[j+1:je]
                #print data
                return int(data1), data
                #getreach[i]=(data[j-1]=="u") #trUe vs falSe
        except:
                print "ERROR: Sensorin tietoja ei pystytty lukemaan"
 


def GetHueXY_IfChanged(lightid,x,y,bri,xold,yold,briold):
        change=False
        xx=[0.0]*len(lightid)
        yy=[0.0]*len(lightid)
        bribri=[0.0]*len(lightid)
        GetHueXY(lightid,xx,yy,bribri)
        #print x,y,bri
        #print xx,yy,bribri
        #print xold,yold,briold
        #print xyerr, xyerr<0.01, bribri==bri,(xyerr<0.01)*(bribri==bri)
        for i in range(len(lightid)):
                xs=float(int(x[i]*10000))/10000
                ys=float(int(y[i]*10000))/10000
                xyerr=(xx[i]-xs)*(xx[i]-xs)+(yy[i]-ys)*(yy[i]-ys)
                brierr=(bribri[i]-int(bri[i]))*(bribri[i]-int(bri[i]))
                if (xyerr<0.01)*(brierr<4)==0:
                        print "Light ",lightid[i]," changed to:", xx[i],yy[i],bribri[i]
                        xold[i]=xx[i]
                        yold[i]=yy[i]
                        briold[i]=bribri[i]
                        change=True
        return(change)

def InitialiseLights(lightid):
        len1=len(lightid)
        xu=[0.0]*len1
        yu=[0.0]*len1
        briu=[0.0]*len1
        x=[0.0]*len1
        y=[0.0]*len1
        bri=[0.0]*len1

        GetHueXY(lightid, xu,yu,briu)
        #print xu,yu,briu

        CopyList(xu,x,0,1)
        CopyList(yu,y,0,1)
        CopyList(briu,bri,0,1)
        #print x,y,bri
        return(xu,yu,briu,x,y,bri)

########## Varifunktiot
def XYColor(R,G,B):
        r=float(R)
        g=float(G)
        b=float(B)

        XX = r * 0.649926 + g * 0.103455 + b * 0.197109
        YY = r * 0.234327 + g * 0.743075 + b * 0.022598
        ZZ = r * 0.000000 + g * 0.053077 + b * 1.035763

        if R==0&G==0&B==0:
                x=.31
                y=.33
                bri=0
        else:
                x = XX /(XX + YY + ZZ)
                y = YY /(XX + YY + ZZ)
                bri = G
                if B>bri:
                        bri=B
                if R > bri:
                        bri=R           
        return(x,y,bri)

def RGBColor(x,y,bri):
        X=float(x)
        Y=float(y)
        Z=1-X-Y

        #Y = float(1)
        #X = (Y / y) * x
        #Z = (Y / y) * z

        r = float(X * 1.612 - Y * 0.203 - Z * 0.302)
        g = float(X * -0.509 + Y * 1.412 + Z * 0.066)
        b = float(X * .026 - Y * 0.072 + Z * 0.962)

        BRI=float(bri)
        if BRI>255:
                BRI=255.0
                print "HUOM!Bri > 255"
        if BRI<0:
                print "HUOM!Bri < 0"
                BRI=0
        
        R=BRI
        G=BRI*g/r
        B=BRI*b/r        
        if (g>r)&(g>=b):
                G=BRI
                R=BRI*r/g
                B=BRI*b/g
        if (b>r)&(b>=g):
                G=BRI*g/b
                R=BRI*r/b
                B=BRI
        if R<0:
                R=0
                BRI=0
        if G<0:
                G=0
                BRI=0
        if B<0:
                B=0
                BRI=0
        
        
        return(int(R),int(G),int(B))


        
def SumColorXY(x1, y1, bri1, x2, y2, bri2):
        bri = bri1+bri2+2
        x=(x1*(bri1+1) + x2*(bri2+1))/bri       
        y=(y1*(bri1+1) + y2*(bri2+1))/bri
        bri=bri-2
        scale =1
        if bri>255:
                bri=255
                scale=bri/(bri1+bri2)   
        if bri<0:
                bri=0
                print "Bri <0"
        return(x,y,bri,scale)

def WeightColorXY(x1, y1, bri1, x2, y2, bri2, weight2):
        bri1 = float(bri1+1)*(1-weight2)
        bri2 = float(bri2+1)*weight2
        bri=bri1+bri2
        x=(x1*bri1 + x2*bri2)/bri       
        y=(y1*bri1 + y2*bri2)/bri
        bri=bri-1
        scale=1
        if bri>255:
                bri=255
                scale=bri/(bri1+bri2)
        if bri<0:
                bri=0
        return(x,y,bri,scale)

def CleanColorXY(x,y,lighttype):
        if lighttype == "hue":
                xr=0.675
                yr=0.322
                xg=0.4091
                yg=0.518
                xb=0.167
                yb=0.04
                #print "hue",x,y
        else: #living colors, light strip
                xr=0.704
                yr=0.296
                xg=0.2151
                yg=0.7106
                xb=0.138
                yb=0.08
                #print "muu",  x,y
                
        xw=0.33
        yw=0.33

        #b-g suora
        xx=xb+(y-yb)/(yg-yb)*(xg-xb)
        #print xx
        if xx > x:
                c=(yb-yw)*(x-xw)-(xb-xw)*(y-yw)
                c=c/((xg-xb)*(y-yw)-(yg-yb)*(x-xw))
                x=xb+c*(xg-xb)
                y=yb+c*(yg-yb)
                #print "bg korjattu", x,y

        #r-g suora
        xx=xr+(y-yr)/(yg-yr)*(xg-xr)
        if xx < x:
                c=(yr-yw)*(x-xw)-(xr-xw)*(y-yw)
                c=c/((xg-xr)*(y-yw)-(yg-yr)*(x-xw))
                x=xr+c*(xg-xr)
                y=yr+c*(yg-yr)
                #print "rg korjattu", x,y

        #b-r suora
        yy=yb+(x-xb)/(xr-xb)*(yr-yb)
        if yy > y:
                c=(yb-yw)*(x-xw)-(xb-xw)*(y-yw)
                c=c/((xr-xb)*(y-yw)-(yr-yb)*(x-xw))
                x=xb+c*(xr-xb)
                y=yb+c*(yr-yb)
                #print "br korjattu", x,y

        return(x,y)                  

############# SetHueFunktiot

def SetHue(id, bri, x, y, ttime):
        
        for i in range(len(id)):
                lighttype="hue"
                if id[i]=="4":
                        lighttype="stripe"
                if id[i]=="13":
                        lighttype="stripe"
                if id[i]=="14":
                        lighttype="stripe"
                if id[i]=="15":
                        lighttype="stripe"
                if id[i]=="16":
                        lighttype="stripe"
                if id[i]=="10":
                        lighttype="livingcolors"
                if id[i]=="11":
                        lighttype="livingcolors"                      
                xt,yt=CleanColorXY(x[i],y[i],lighttype)

                onstate ="\"on\":true"
                bri_set ="\"bri\":"+str(int(bri[i]))
                color_set="\"xy\":["+str(float(int(xt*10000))/10000)+","+str(float(int(yt*10000))/10000)+"]"
                ttime_set ="\"transitiontime\":"+str(int(ttime))
                hue_body="{"+onstate+","+bri_set+","+color_set+","+ttime_set+"}"
                #print "SH", hue_body #############
        
                hue_address="/api/newdeveloper/lights/"+id[i]+"/state"
                try:
                        conn.request("PUT",hue_address,hue_body)
                        r1=conn.getresponse()
                        #data = r1.read()
                        #print data             
                except:
                        print "*************\n IoError on SetHue \n*************"
                #data = r1.read()
                #print data             

def SetHueOn(id, bri, x, y, ttime,on):
        
        for i in range(len(id)):
                lighttype="hue"
                if id[i]=="4":
                        lighttype="stripe"
                if id[i]=="13":
                        lighttype="stripe"
                if id[i]=="14":
                        lighttype="stripe"
                if id[i]=="15":
                        lighttype="stripe"
                if id[i]=="16":
                        lighttype="stripe"
                if id[i]=="10":
                        lighttype="livingcolors"
                if id[i]=="11":
                        lighttype="livingcolors"                      
                xt,yt=CleanColorXY(x[i],y[i],lighttype)

                if on[i]:
                        onstate ="\"on\":true"
                else:
                        onstate ="\"on\":false"
                bri_set ="\"bri\":"+str(int(bri[i]))
                color_set="\"xy\":["+str(float(int(xt*10000))/10000)+","+str(float(int(yt*10000))/10000)+"]"
                ttime_set ="\"transitiontime\":"+str(int(ttime))
                hue_body="{"+onstate+","+bri_set+","+color_set+","+ttime_set+"}"
                #print "SHO", hue_body #############
        
                hue_address="/api/newdeveloper/lights/"+id[i]+"/state"
                try:
                        conn.request("PUT",hue_address,hue_body)
                        r1=conn.getresponse()
                        #data = r1.read()
                        #print data             
                except:
                        print "*************\n IoError on SetHue \n*************"
                #data = r1.read()
                #print data             

def SetHueUnLit(id, bri, x, y, ttime):
        
        for i in range(len(id)):
                if bri[i]<0:
                        bri[i]=0
                onstate ="\"on\":false"
                bri_set ="\"bri\":"+str(int(bri[i]))
                color_set="\"xy\":["+str(float(int(x[i]*10000))/10000)+","+str(float(int(y[i]*10000))/10000)+"]"
                ttime_set ="\"transitiontime\":"+str(int(ttime))
                hue_body="{"+onstate+","+bri_set+","+color_set+","+ttime_set+"}"
                #print "SHU",hue_body

                hue_address="/api/newdeveloper/lights/"+id[i]+"/state"

                try:
                        conn.request("PUT",hue_address,hue_body)
                        r1=conn.getresponse()
                        #data = r1.read()
                        #print data             

                except:
                        print "*************\n IoError on SetHueUnLit \n*************"
                            


def HueOnOff(id, onTrue):
        onstate="true"
        if onTrue=="off":
                onstate="false"
        if onTrue=="Off":
                onstate="false"
        if onTrue=="OFF":
                onstate="false"
        if onTrue==0:
                onstate="false"
        if onTrue==False:
                onstate="false" 
        onstate ="\"on\":"+onstate
        hue_body="{"+onstate+"}"        
        
        for ids in id:
                hue_address="/api/newdeveloper/lights/"+ids+"/state"
                conn.request("PUT",hue_address,hue_body)
                r1=conn.getresponse()
                #data = r1.read()
                #print data             

####################HUEDEMO####################################

def HueDemo(iddemo):

#iddemo=["10","11","4","6","1","7","8","5","9"]

    bri_dim=[0.0]*len(iddemo)
    bri_quad=[64.0]*len(iddemo)
    bri_half=[128.0]*len(iddemo)
    bri_3quad=[190.0]*len(iddemo)
    bri_full=[255.0]*len(iddemo)
    x_wh=[0.33]*len(iddemo)
    y_wh=[0.33]*len(iddemo)
    x_r=[0.7]*len(iddemo)
    y_r=[0.3]*len(iddemo)
    x_b=[0.1]*len(iddemo)
    y_b=[0.04]*len(iddemo)
    x_y=[0.5]*len(iddemo)
    y_y=[0.4]*len(iddemo)
    x_rand=[0.25,0.15,0.65,0.4,0.45,0.6,0.3,0.18,0.5]
    y_rand=[0.70,0.20,0.30,0.5,0.18,0.3,0.3,0.05,0.4]
    x_rand2=[0.15,0.65,0.25,0.5,0.4,0.45,0.6,0.3,0.18]
    y_rand2=[0.20,0.30,0.70,0.4,0.5,0.18,0.3,0.3,0.05]

    SetHue(iddemo, bri_dim, x_r, y_r, 10)
    time.sleep(2)
    SetHue(iddemo, bri_dim, x_b, y_b, 10)
    time.sleep(2)

    id=[iddemo[0]]
    bri=[bri_quad[0]]
    brid=[bri_dim[0]]
    x=[x_r[0]]
    y=[y_r[0]]

    SetHue(id, bri, x, y, 1)
    time.sleep(0.1)
    SetHue(id, brid, x, y, 1)
    time.sleep(0.3)
    SetHue(id, bri, x, y, 1)
    time.sleep(0.1)
    SetHue(id, brid, x, y, 1)
    time.sleep(0.5)

    SetHue(id, bri, x, y, 5)
    time.sleep(0.5)

    for i in range(len(iddemo)):
        id=[iddemo[i]]
        SetHue(id, bri, x, y, 5)
        time.sleep(0.5)
        #SetHue(id, brid, x, y, 10)

    for i in range(5):
        ii=random.randint(5,8)
        id=[iddemo[ii]]
        SetHue(id, bri, x, y, 3)
        time.sleep(0.3)
        SetHue(id, brid, x, y, 3)

    SetHue(iddemo[5:9], bri_half[5:9], x_r[5:9], y_r[5:9], 5)
    time.sleep(0.5)
    

    id=[iddemo[0]]
    bri=[bri_half[0]]
    brid=[bri_dim[0]]
    x=[x_y[0]]
    y=[y_y[0]]

    SetHue(id, bri, x, y, 1)
    time.sleep(0.1)
    SetHue(id, brid, x, y, 1)
    time.sleep(0.3)
    SetHue(id, bri, x, y, 1)
    time.sleep(0.1)
    SetHue(id, brid, x, y, 1)
    time.sleep(0.5)


    SetHue(id, bri, x, y, 5)
    time.sleep(0.5)

    for i in range(len(iddemo)):
        id=[iddemo[i]]
        SetHue(id, bri, x, y, 5)
        time.sleep(0.5)
        #SetHue(id, brid, x, y, 10)

    for i in range(5):
        ii=random.randint(5,8)
        id=[iddemo[ii]]
        SetHue(id, bri, x, y, 3)
        time.sleep(0.3)
        SetHue(id, brid, x, y, 3)

    SetHue(iddemo[5:9], bri_half[5:9], x_y[5:9], y_y[5:9], 5)
    time.sleep(0.5)

    id=[iddemo[0]]
    bri=[bri_3quad[0]]
    brid=[bri_dim[0]]
    x=[x_wh[0]]
    y=[y_wh[0]]

    SetHue(id, bri, x, y, 1)
    time.sleep(0.1)
    SetHue(id, brid, x, y, 1)
    time.sleep(0.3)
    SetHue(id, bri, x, y, 1)
    time.sleep(0.1)
    SetHue(id, brid, x, y, 1)
    time.sleep(0.5)


    SetHue(id, bri, x, y, 5)
    time.sleep(0.5)

    for i in range(len(iddemo)):
        id=[iddemo[i]]
        SetHue(id, bri, x, y, 5)
        time.sleep(0.5)
        #SetHue(id, brid, x, y, 10)

    for i in range(5):
        ii=random.randint(5,8)
        id=[iddemo[ii]]
        SetHue(id, bri, x, y, 3)
        time.sleep(0.3)
        SetHue(id, brid, x, y, 3)

    SetHue(iddemo[5:9], bri_half[5:9], x_wh[5:9], y_wh[5:9], 5)
    time.sleep(0.5)


    bri=[bri_full[0]]
    brid=[bri_dim[0]]

    ii=range(len(iddemo))
    ii.reverse()



    for i in ii:
        id=[iddemo[i]]
        SetHue(id, bri, x, y, 1)
        #x_rand[i]=random.random()*0.6+.1
        #y_rand[i]=random.random()*0.6
        time.sleep(1)
    
    time.sleep(2)

    SetHue(iddemo, bri_full, x_rand, y_rand, 1)
    time.sleep(3)
    SetHue(iddemo, bri_half, x_rand2, y_rand2, 40)
    time.sleep(6)
    SetHue(iddemo, bri_dim, x_y, y_y, 40)
    time.sleep(4)
    SetHue(iddemo, bri_full, x_wh, y_wh, 10)
    time.sleep(1)
    SetHue(iddemo, bri_half, x_y, y_y, 50)
    time.sleep(5)
    SetHue(iddemo[5:9], bri_3quad[5:9], x_wh[5:9], y_wh[5:9], 50)


############## Aurinkofunktiot

def AuKorkeus(vuodenpaiva,kellonaika,leveyspiiri):
        fLeveyspiiri=float(leveyspiiri)
        fAkselinkallistus=23.43
        fAkselinkallistus_Nyt=math.cos(float(vuodenpaiva+10)/365*2*fPi)*fAkselinkallistus
        fSunHeigth=-math.cos(float(kellonaika)/24*fPi*2)*(90-fLeveyspiiri)-fAkselinkallistus_Nyt
        return(fSunHeigth)

def AuNousuLasku(vuodenpaiva,leveyspiiri):
        fLeveyspiiri=float(leveyspiiri)
        fAkselinkallistus=23.43
        fAkselinkallistus_Nyt=math.cos(float(vuodenpaiva+10)/365*2*fPi)*fAkselinkallistus

        MaxHeigth=90-(fLeveyspiiri+fAkselinkallistus_Nyt)
        MinHeigth=(fLeveyspiiri-fAkselinkallistus_Nyt)-90
        #print MaxHeigth, MinHeigth

        ValoisaAika=float(0)
        if MaxHeigth > 0:
                if MinHeigth < 0:
                        fAlpha_apu=math.asin(math.tan(fLeveyspiiri/180*fPi)*math.tan(fAkselinkallistus_Nyt/180*fPi))*180/fPi
                        ValoisaAika=(90-fAlpha_apu+1)/180*24
                        return(12-ValoisaAika/2,12+ValoisaAika/2)
        if MaxHeigth < 0:
            ValoisaAika =0
            return(-1,-1)
        if MinHeigth > 0:
            ValoisaAika =24
            return(-2,-2)
        


        
        fSunHeigth=-math.cos(float(kellonaika)/24*fPi*2)*(90-fLeveyspiiri)-fAkselinkallistus_Nyt
        return(fSunHeigth)

def AuPituuspiiriKorjaus(pituuspiiri):
        h=float(pituuspiiri)/15.0-2 #Suomessa
        #h=int(mn)+2
        #mn=mn-int(mn)
        #if mn>0.5:
        #        mn=mn-1
        #        h=h+1
        #if mn<-0.5:
        #        mn=mn+1
        #        h=h-1
        #mn=(h+mn)*-60
        mn=h*-60
        print "Pituuspiirikorjaus: "+str(int(mn))+" min"
        return(int(mn))

def AuEoTKorjaus(vuodenpaiva):
        M=6.24+0.01720197*vuodenpaiva #Suurinpiirtein
        EoTkorjaus=-7.659*math.sin(M)+9.863*math.sin(2*M+3.5932) #Equation of time - maan radan ellipsisyys
        print "Ajantasaus: "+str(int(EoTkorjaus))
        return (int(EoTkorjaus))
        
        
def AuVariXY(fSunHeigth,fTropoHeigth):  
        #fTropoHeigth=fTropoHeigth*0.2
        P=950
        T=0
        
        sh=fSunHeigth
        fSunHeigth=sh+P/(273+T)*(0.1594+0.0196*sh+0.00002*sh*sh)/(1+0.505*sh+0.0845*sh*sh) #Ilmakehän refraktio
        
        #print sh, fSunHeigth
        
        #fRvaim= float(1)/1.1 #per 200 km
        #fGvaim= float(1)/2 #per 90 km
        #fBvaim = float (1)/2 #per 10 km

        #fRvaim_l=float(300)
        #fGvaim_l=float(40)
        #fBvaim_l=float(10)

        fRvaim= float(1)/1.1 #per 200 km
        fGvaim= float(1)/2 #per 90 km
        fBvaim = float (1)/2 #per 10 km

        fRvaim_l=float(247)#(87)
        fGvaim_l=float(85)#(77)#(153)
        fBvaim_l=float(29)#(19)



        if fSunHeigth>0:
                fSkythick = fTropoHeigth/(math.cos(fPi/2-fSunHeigth/180*fPi)+0.50572*pow(6.07995+fSunHeigth,-1.6364)) #airmass, karsten & young (1989)
        else:
                fSkythick = fTropoHeigth/(math.cos(fPi/2)+0.50572*pow(6.07995,-1.6364))

        fR=255*pow(fRvaim,fSkythick/fRvaim_l)
        fG=255*pow(fGvaim,fSkythick/fGvaim_l)
        fB=255*pow(fBvaim,fSkythick/fBvaim_l)
        #print fR,fG,fB
        x,y,bri=XYColor(int(fR),int(fG),int(fB))
        visible=1.0
        if fSunHeigth<0.25:
                visible=(fSunHeigth+0.25)/0.5
        if fSunHeigth<-.25:
                visible=0
        if fSunHeigth<0:
                bri=bri*(fSunHeigth+5.0)/5.0
        if fSunHeigth<-5:
                bri=0
        return(x,y,bri,visible)

        
        


def SkyVariXY(fSunHeigth,fTropoHeigth): 
        #fTropoHeigth=fTropoHeigth*0.5
        P=950
        T=0
        
        sh=fSunHeigth
        fSunHeigth=sh+P/(273+T)*(0.1594+0.0196*sh+0.00002*sh*sh)/(1+0.505*sh+0.0845*sh*sh) #Ilmakehän refraktio


        fRvaim= float(1)/1.1 #per 300 km
        fGvaim= float(1)/2 #per 200 km
        fBvaim = float (1)/2 #per 10 km

        fRvaim_l=float(247)#(87)
        fGvaim_l=float(85)#(77)#(153)
        fBvaim_l=float(29)#(19)

        if fSunHeigth>0:
                fSkythick = fTropoHeigth/(math.cos(fPi/2-fSunHeigth/180*fPi)+0.50572*pow(6.07995+fSunHeigth,-1.6364)) #airmass, karsten & young (1989)
        else:
                fSkythick = fTropoHeigth/(math.cos(fPi/2)+0.50572*pow(6.07995,-1.6364))
        

        fR=255*pow(fRvaim,fSkythick/fRvaim_l)
        fG=255*pow(fGvaim,fSkythick/fGvaim_l)
        fB=255*pow(fBvaim,fSkythick/fBvaim_l)
        print fR,fG,fB
        x,y,bri=XYColor(255-int(fR),255-int(fG),255-int(fB))
        if fSunHeigth<0:
                bri=bri*(fSunHeigth+10.0)/10.0
        if fSunHeigth<-10:
                bri=0
        return(x,y,bri)

def SkyPosVariXY(fSunHeigth,fTropoHeigth,skypos): 
        #fTropoHeigth=fTropoHeigth*0.5
        P=950
        T=0
        fSunHeigth=float(fSunHeigth)
        skypos=float(skypos)
        
        etaau=1/pow(abs(fSunHeigth-skypos)+1,.25)
        et=math.sin(skypos*fPi/180)
        et=et*et*et
        if fSunHeigth==0:
                merkki=1
        else:
                merkki=fSunHeigth/abs(fSunHeigth)
        varjonpaikka=-merkki*(90-abs(fSunHeigth))/5.5
        varjokerroin=1-merkki*(varjonpaikka-et)
        on=True
        if varjokerroin>1:
                varjokerroin=1
        if varjokerroin<0:
                varjokerroin=0
                on=False
        #print varjokerroin, et, varjonpaikka, merkki

        
        sh=90-abs(fSunHeigth)
        fSunHeigth=sh+P/(273+T)*(0.1594+0.0196*sh+0.00002*sh*sh)/(1+0.505*sh+0.0845*sh*sh) #Ilmakehan refraktio


        fRvaim= float(1)/1.1 #per 300 km
        fGvaim= float(1)/2 #per 200 km
        fBvaim = float (1)/2 #per 10 km

        fRvaim_l=float(247)#(87)
        fGvaim_l=float(85)#(77)#(153)
        fBvaim_l=float(29)#(19)

        if fSunHeigth>0:
                fSkythick = fTropoHeigth/(math.cos(fPi/2-fSunHeigth/180*fPi)+0.50572*pow(6.07995+fSunHeigth,-1.6364)) #airmass, karsten & young (1989)
        else:
                fSkythick = fTropoHeigth/(math.cos(fPi/2)+0.50572*pow(6.07995,-1.6364))
        

        fRs=255*pow(fRvaim,fSkythick/fRvaim_l)
        fGs=255*pow(fGvaim,fSkythick/fGvaim_l)
        fBs=255*pow(fBvaim,fSkythick/fBvaim_l)

        #st=fSkythick
        
        sh=90-abs(skypos)
        skypos=sh+P/(273+T)*(0.1594+0.0196*sh+0.00002*sh*sh)/(1+0.505*sh+0.0845*sh*sh) #Ilmakehan refraktio

        if skypos>0:
                fSkythick = fTropoHeigth/(math.cos(fPi/2-skypos/180*fPi)+0.50572*pow(6.07995+skypos,-1.6364)) #airmass, karsten & young (1989)
        else:
                fSkythick = fTropoHeigth/(math.cos(fPi/2)+0.50572*pow(6.07995,-1.6364))

        #st=(st+fSkythick)/fTropoHeigth/2
        
        fR=(255-fRs)*fRs/255+(fSkythick*fRs)/70.0*etaau*varjokerroin
        fG=(255-fGs)*fRs/255+(fSkythick*fGs)/70.0*etaau*varjokerroin
        fB=(255-fBs)*fRs/255+(fSkythick*fBs)/70.0*etaau*varjokerroin


        if (fR>=fG)&(fR>=fB):
                r=255
                g=fG*255/fR
                b=fB*255/fR
        if (fG>fR)&(fG>=fB):
                g=255
                r=fR*255/fG
                b=fB*255/fG
        if (fB>fR)&(fB>fG):
                b=255
                r=fR*255/fB
                g=fG*255/fB

        
        fR=r
        fG=g
        fB=b
                                
        #print "Taivas",int(255-fR),int(255-fG),int(255-fB)
        #return(int(fR),int(fG),int(fB))
        x,y,bri=XYColor(int(fR),int(fG),int(fB))
        bri=bri*varjokerroin
        return(x,y,bri,on)

        
########## daymemory read and write     

def SaveLightMemory(filtsu,id,x,y,bri):
        f = open(filtsu, 'w')
        for i in range(len(id)):
                f.write(id[i]+", "+str(x[i])+", "+str(y[i])+", "+str(bri[i])+"\n") 
        f.close()
 
def ReadLightMemory(filtsu,id,x,y,bri):
        f = open(filtsu, 'r')
        for line in f:
                #print line
                pilkku=line.find(",")
                id_r=line[0:pilkku]
                pilkkuold=pilkku
                pilkku=line.find(",",pilkku+1)
                x_r=line[pilkkuold+1:pilkku]
                pilkkuold=pilkku
                pilkku=line.find(",",pilkku+1)
                y_r=line[pilkkuold+1:pilkku]
                pilkkuold=pilkku
                pilkku=line.find("\n",pilkku+1)
                bri_r=line[pilkkuold+1:pilkku]  
                #getx[i]=float(xy[0:xy.find(",")])
                #print id_r,x_r,y_r,bri_r
                #5, 0.4448, 0.4066, 213.0
                try:
                        id_i=id.index(id_r)
                        x[id_i]=float(x_r)
                        y[id_i]=float(y_r)
                        bri[id_i]=float(bri_r)
                        #print id_r,"found"
                except ValueError:
                        if False:
                                print id_r,"skipped"
        f.close()
        
##############################################################
def GetFMIWeatherData(stored_query_id,parameters):  
    apikey="f0baf379-ec38-4946-b49f-8b6403253775"
    SERVER_URL = "http://data.fmi.fi/fmi-apikey/"+apikey+"/wfs";
    REQUEST="request=getFeature"
    FMIconnection = urllib2.urlopen(SERVER_URL+"?"+REQUEST+stored_query_id+parameters)
    data=FMIconnection.read();
    return(data)                  


def GetFMIWeatherForecast(place):
    stored_query_id="&storedquery_id=fmi::forecast::hirlam::surface::point::multipointcoverage&place="+place 
    parameters="Temperature,MaximumWind,WindGust"
    parameters=parameters+",PrecipitationAmount,Precipitation1h"
    parameters=parameters+",LowCloudCover,MediumCloudCover,HighCloudCover,TotalCloudCover"
    #parameters=parameters+",Humidity,DewPoint,Pressure"
    parameters="&parameters="+parameters


    data=GetFMIWeatherData(stored_query_id,parameters)
    
    #&param=Pressure,GeopHeight,Temperature,DewPoint,\
    #Humidity,WindUMS,WindVMS,PrecipitationAmount,TotalCloudCover,\
    #LowCloudCover,MediumCloudCover,HighCloudCover,RadiationNetTopAtmLW,\
    #RadiationLW,RadiationGlobal,Precipitation1h,MaximumWind,WindGust\
    #&origintime=2013-06-06T18:00:00Z\
    #&starttime=2013-06-06T18:00:00Z\
    #&endtime=2013-06-09T00:00:00Z\

    #print data
    
    w_i=data.find("<gml:name>")
    w_i=data.find(">",w_i)
    w_e=data.find("</gml:name>",w_i)
    weather_obs=data[w_i+1:w_e]
    print weather_obs

    w_i=data.find("<gml:pos>")
    w_i=data.find(">",w_i)
    w_e=data.find("</gml:pos>",w_i)
    weather_pos_txt=data[w_i+1:w_e]
    weather_pos=[float(weather_pos_txt[0:weather_pos_txt.find(" ")]),float(weather_pos_txt[weather_pos_txt.find(" ")+1:len(weather_pos_txt)])]
    print weather_pos_txt


    w_i=data.find("<gml:beginPosition>")
    w_i=data.find(">",w_i)
    w_e=data.find("</gml:beginPosition>")
    weather_time=data[w_i+1:w_e]
    print weather_time

    print parameters


    w_i=data.find("<gml:doubleOrNilReasonTupleList>")
    w_i=data.find(">",w_i)
    w_e=data.find("</gml:doubleOrNilReasonTupleList>",w_i)
    w_e=data.find("\n",w_i,w_e)
    w_e=data.find("\n",w_e+1)
    #w_i=data.rfind("\n",w_i,w_e)
    wwdata=data[w_i+1:w_e]
    wdata=wwdata.split()
    weatherdata=[0.0]*len(wdata)
    for i in range(len(wdata)):
        weatherdata[i]=float(wdata[i])
    #wdata_latest=wdata[len(wdata)-11:len(wdata)]
    return(weatherdata, weather_pos, weather_obs)

    


def GetFMIWeatherObservation(place):
    stored_query_id="&storedquery_id=fmi::observations::weather::multipointcoverage&place="+place
    parameters=""
    data=GetFMIWeatherData(stored_query_id,parameters)

    w_i=data.find("<gml:name>")
    w_i=data.find(">",w_i)
    w_e=data.find("</gml:name>",w_i)
    weather_obs=data[w_i+1:w_e]
    print weather_obs

    w_i=data.find("<gml:pos>")
    w_i=data.find(">",w_i)
    w_e=data.find("</gml:pos>",w_i)
    weather_pos=data[w_i+1:w_e]
    print weather_pos


    w_i=data.find("<gml:endPosition>")
    w_i=data.find(">",w_i)
    w_e=data.find("</gml:endPosition>")
    weather_time=data[w_i+1:w_e]
    print weather_time

    w_i=data.find("<gml:doubleOrNilReasonTupleList>")
    w_i=data.find(">",w_i)
    w_e=data.find("</gml:doubleOrNilReasonTupleList>",w_i)
    w_e=data.rfind("\n",w_i,w_e)
    w_i=data.rfind("\n",w_i,w_e)
    wwdata=data[w_i+1:w_e]
    wdata=wwdata.split()
    weatherdata=[0.0]*len(wdata)
    for i in range(len(wdata)):
        weatherdata[i]=float(wdata[i])
    #wdata_latest=wdata[len(wdata)-11:len(wdata)]
    
    return(weatherdata)
#Instantaneous Weather Observations (fmi::observations::weather::multipointcoverage)
#Real time weather observations from weather stations. Default set contains temperature, wind speed,
#direction, gust,  relative humidity, dew point, pressure reduced to sea level,
#one hour precipitation amount, visibility and cloud cover. By default, the data is returned
#from last 12 hour. At least one location parameter (geoid/place/fmisid/wmo/bbox) has to be given.
#The data is returned as a multi point coverage format. 
    
###############################################
def CloudRandom(ap,kp,yp, returnweights, brightmode):
        ap=float(ap)/100
        kp=float(kp)/100
        yp=float(yp)/100
        w_au=1
        w_sk=1

        l=0.6
        h=0.95

        #if brightmode:
        #        h=1.0
        #        l=0.95

        tn_sk=(1-ap)*(1-kp)*(1-yp)

        wau_ypah=h
        wau_ypal=wau_ypah*l
        wsk_ypah=h
        wsk_ypal=wsk_ypah*l
        tn_ypah=yp*(1-yp)
        tn_ypal=yp*yp
        tnx_yp=(1-kp)*(1-ap)

        wau_kpVh=tn_ypah*wau_ypah + tn_ypal*wau_ypal
        wau_kpVl=wau_kpVh*l
        wau_kpah=h+wau_kpVh
        wau_kpal=wau_kpah*l
        wsk_kpVh=(1-yp)*h + tn_ypah*wsk_ypah + tn_ypal*wsk_ypal
        wsk_kpVl=wsk_kpVh*l
        wsk_kpah=wsk_kpVh
        wsk_kpal=wsk_kpah*l
        tn_kpVh=kp*yp*(1-kp)
        tn_kpVl=kp*yp*kp
        tn_kpah=kp*(1-yp)*(1-kp)
        tn_kpal=kp*(1-yp)*kp
        tnx_kp=(1-ap)


        wau_apVh = (1-kp)*wau_kpVh + tn_kpVh*wau_kpVh + tn_kpVl*wau_kpVl + tn_kpah*wau_kpah +tn_kpal*wau_kpal
        wau_apVl=wau_apVh*l
        wau_apah=h+wau_apVh
        wau_apal=wau_apah*l
        wsk_apVh =  (1-kp)*wsk_kpVh + tn_kpVh*wsk_kpVh + tn_kpVl*wsk_kpVl + tn_kpah*wsk_kpah +tn_kpal*wsk_kpal
        wsk_apVl = wsk_apVh*l
        wsk_apah=wsk_apVh
        wsk_apal=wsk_apah*l
        tn_apVh=ap*(kp+(1-kp)*yp)*(1-ap)
        tn_apVl=ap*(kp+(1-kp)*yp)*ap
        tn_apah=ap*(1-kp)*(1-yp)*(1-ap)
        tn_apal=ap*(1-kp)*(1-yp)*ap
        tnx_ap=1


        printtaa=False #True
        if printtaa:
                print "Taivas/aurinko"
                print "sk", tn_sk, w_sk, w_au
                print "Ylapilvet"
                print "ypah", tn_ypah*tnx_yp, wsk_ypah, wau_ypah
                print "ypal", tn_ypal*tnx_yp, wsk_ypal, wau_ypal
                print "Keskipilvet"
                print "kpVh", tn_kpVh*tnx_kp, wsk_kpVh, wau_kpVh
                print "kpVl", tn_kpVl*tnx_kp, wsk_kpVl, wau_kpVl
                print "kpah", tn_kpah*tnx_kp, wsk_kpah, wau_kpah
                print "kpal", tn_kpal*tnx_kp, wsk_kpal, wau_kpal
                print "Alapilvet"                
                print "apVh", tn_apVh*tnx_ap, wsk_apVh, wau_apVh
                print "apVl", tn_apVl*tnx_ap, wsk_apVl, wau_apVl
                print "apah", tn_apah*tnx_ap, wsk_apah, wau_apah
                print "apal", tn_apal*tnx_ap, wsk_apal, wau_apal
                tntot=tn_sk+tn_ypah*tnx_yp+tn_ypal*tnx_yp
                tntot=tntot+ tn_kpVh*tnx_kp +tn_kpVl*tnx_kp +tn_kpal*tnx_kp +tn_kpah*tnx_kp
                tntot=tntot+tn_apVh+tn_apVl+tn_apal+tn_apah
                print "Yhteensa", tntot               
        if returnweights:
                weights_sk=[0, w_sk, wsk_ypah, wsk_ypal, wsk_kpVh,wsk_kpVl, wsk_kpah, wsk_kpal, wsk_apVh, wsk_apVl, wsk_apah, wsk_apal]
                weights_au=[w_au, 0, wau_ypah, wau_ypal, wau_kpVh,wau_kpVl, wau_kpah, wau_kpal, wau_apVh, wau_apVl, wau_apah, wau_apal]
                tn_pil =[tn_sk,tn_sk, tn_ypah*tnx_yp, tn_ypal*tnx_yp, tn_kpVh*tnx_kp, tn_kpVl*tnx_kp, tn_kpah*tnx_kp, tn_kpal*tnx_kp]
                tn_pil=tn_pil +[tn_apVh*tnx_ap, tn_apVl*tnx_ap, tn_apah*tnx_ap, tn_apal*tnx_ap]

                return(weights_sk, weights_au, tn_pil)
               
               
        #randomise cloud level
        pilvi= random.random()
        #print pilvi
        
        tn=tn_sk
        if pilvi<tn:
                return(w_au,w_sk,"sk")


        tn=tn+tn_ypah*tnx_yp
        if pilvi<tn:
                return(wau_ypah,wsk_ypah,"ypah")
        tn=tn+tn_ypal*tnx_yp
        if pilvi<tn:
                return(wau_ypal,wsk_ypal,"ypal")



        tn=tn+tn_kpVh*tnx_kp
        if pilvi<tn:
                return(wau_kpVh,wsk_kpVh,"kpVh")
        tn=tn+tn_kpVl*tnx_kp
        if pilvi<tn:
                return(wau_kpVl,wsk_kpVl,"kpVl")
        tn=tn+tn_kpah*tnx_kp
        if pilvi<tn:
                return(wau_kpah,wsk_kpah,"kpah")
        tn=tn+tn_kpal*tnx_kp
        if pilvi<tn:
                return(wau_kpal,wsk_kpal,"kpal")



        tn=tn+tn_apVh*tnx_ap
        if pilvi<tn:
                return(wau_apVh,wsk_apVh,"apVh")
        tn=tn+tn_apVl*tnx_ap
        if pilvi<tn:
                return(wau_apVl,wsk_apVl,"apVl")
        tn=tn+tn_apah*tnx_ap
        if pilvi<tn:
                return(wau_apah,wsk_apah,"apah")
        tn=tn+tn_apal*tnx_ap
        if pilvi<tn:
                return(wau_apal,wsk_apal,"apal")

        print "Vikaa pilviarvonnassa?", tn, pilvi
        return(w_au,w_sk,"sk")



#################  KAYTTOLIITTYMA ###########################3        
from Tkinter import *

class Application(Frame):
        def muokkaamuutos(self):
                self.infoteksti.set("Kohta paasee muokkaamaan")
                self.muokkaa.set(True)
                self.breakloop.set(True)
                #print self.demomode.get()==True

        def lopetaohjelma(self):
                self.infoteksti.set("Kohta loppuu")
                self.lopeta.set(True)
                self.breakloop.set(True)
                #print self.demomode.get()==True

        def nousulasku(self, event):
                nousu,lasku=AuNousuLasku(self.vuodenpaiva.get(),self.leveyspiiri.get()) ####Huom leveyspiiri fiksattu
                if nousu==-1:
                        self.nousulaskuteksti.set("Kaamos")
                if nousu==-2:
                        self.nousulaskuteksti.set("Yoton yo")
                if nousu>0:
                        nousu=nousu+float(self.hshift.get())/60.0
                        if nousu<0:
                                nousu=24+nousu
                        nousuh=int(nousu)
                        nousu=int((nousu-float(nousuh))*60)
                        nousustr=str(nousu+100)
                        nousustr=str(nousuh)+":"+nousustr[1:3]

                        lasku=lasku+float(self.hshift.get())/60.0
                        if lasku>24:
                                lasku=lasku-24
                        laskuh=int(lasku)
                        lasku=int((lasku-float(laskuh))*60)
                        laskustr=str(lasku+100)
                        laskustr=str(laskuh)+":"+laskustr[1:3]
                        self.nousulaskuteksti.set("Nousu: "+nousustr+", Lasku: "+laskustr+" "+str(self.hshift.get()))
        
        def tallennamuistiin(self):
                self.infoteksti.set("Tallennetaan "+self.vuorokaudenaika.get()+"valaistus " + self.daymemoryFile.get())
                self.muokkaa.set(True)
                self.tallennapaivamuisti.set(True)
                self.quit()

                #self.lopeta.set(True)
                #print self.demomode.get()==True

        def luemuisti(self):
                self.infoteksti.set("Luetaan "+self.daymemoryFile.get())
                self.muokkaa.set(True)
                self.luepaivamuisti.set(True)
                self.breakloop.set(True)
                self.quit()

                #self.lopeta.set(True)
                #print self.demomode.get()==True

        def pilvistyvartti(self):
                self.realweather.set(False)
                a=self.ylapilvi.get()
                a=a+self.keskipilvi.get()
                a=a+self.alapilvi.get()
                a=a/3
                self.pilvistylaskuri.set(a)
                self.ylapilvi.set(a)
                self.keskipilvi.set(a)
                self.alapilvi.set(a)
                self.infoteksti.set(self.infoteksti.get()+" Pilvistyy")

        def kirkastu(self):
                self.realweather.set(False)
                self.breakloop.set(True)
                self.ylapilvi.set(0)
                self.keskipilvi.set(0)
                self.alapilvi.set(0)
                self.pilvistylaskuri.set(100)

        def pilvisty(self):
                self.realweather.set(False)
                self.breakloop.set(True)
                self.ylapilvi.set(100)
                self.keskipilvi.set(100)
                self.alapilvi.set(100)
                self.pilvistylaskuri.set(100)

        def neonvari(self,event):
                
                R,G,B=RGBColor(float(self.xneonau.get())/100,float(self.yneonau.get())/100,255)
                Rh=hex(R+256)
                Gh=hex(G+256)
                Bh=hex(B+256)
                aucolor="#"+Rh[3:len(Rh)]+Gh[3:len(Gh)]+Bh[3:len(Bh)]
                #print aucolor, Rh, Gh, Bh
                self.xneonauScale["bg"]=aucolor
                self.yneonauScale["bg"]=aucolor

                R,G,B=RGBColor(float(self.xneonsk.get())/100,float(self.yneonsk.get())/100,255)
                Rh=hex(R+256)
                Gh=hex(G+256)
                Bh=hex(B+256)
                skcolor="#"+Rh[3:len(Rh)]+Gh[3:len(Gh)]+Bh[3:len(Bh)]
                self.xneonskScale["bg"]=skcolor
                self.yneonskScale["bg"]=skcolor

                #self.lopeta.set(True)
                #print self.demomode.get()==True

	
        def createWidgets(self):
                self.breakloop=BooleanVar()
                self.breakloop.set(False)

                self.alaFrame=Frame(self)
                self.alaFrame.pack({"side":"bottom","fill":"x"})

                self.vasenFrame=Frame(self)
                #self.vasenFrame["bg"]="#11FFFF"
                self.vasenFrame.pack({"side":"left"})
                
                #Aikamaaritykset
                
                self.datetimeFrame=Frame(self.vasenFrame)
                #self.datetimeFrame["bg"]="#11FFFF"
                self.datetimeFrame.pack()

                self.datetimeLabel=Label(self.datetimeFrame)
                self.datetimeLabel["text"]="Aika-asetukset"
                self.datetimeLabel.pack({"fill":"x"})           
                
                self.datepresetButton=Checkbutton(self.datetimeFrame)
                self.datepresetButton["text"]="Esiasetettu vuodenpaiva ja paikka"
                self.datepresetButton.pack()
                
                self.datepreset=BooleanVar()
                self.datepreset.set(False)
                self.datepresetButton["onvalue"]=True
                self.datepresetButton["offvalue"]=False
                self.datepresetButton["variable"]=self.datepreset
                
                self.dateactualButton=Checkbutton(self.datetimeFrame)
                self.dateactualButton["text"]="Nykyinen vuodenpaiva kaytossa"
                self.dateactualButton.pack()
                
                self.dateactual=BooleanVar()
                self.dateactual.set(False)
                self.dateactualButton["onvalue"]=True
                self.dateactualButton["offvalue"]=False
                self.dateactualButton["variable"]=self.dateactual
                

                self.vuodenpaiva=IntVar()
                self.vuodenpaivaScale =Scale(self.datetimeFrame, from_=1, to=365, orient=HORIZONTAL,length=150)
                self.vuodenpaivaScale["label"]="Vuodenpaiva"
                self.vuodenpaivaScale["variable"]=self.vuodenpaiva
                self.vuodenpaivaScale.bind('<B1-Motion>',self.nousulasku)
                self.vuodenpaivaScale.pack({"side":"left"})
                
                self.hshift=IntVar()
                self.hshiftScale =Scale(self.datetimeFrame, from_=-300, to=300, orient=HORIZONTAL, length=200)
                self.hshiftScale["label"]="Keskipaivan siirto aurinkomallissa, min"
                self.hshiftScale["variable"]=self.hshift
                self.hshiftScale.bind('<B1-Motion>',self.nousulasku)
                self.hshiftScale.pack({"side":"left"})

                self.leveyspiiri=DoubleVar()
                self.leveyspiiri.set(65)
                self.nousulaskuteksti=StringVar()
                self.nousulaskuteksti.set("Ei laskettu")
                self.nousulasku("initial")
                self.nousulaskuLabel=Label(self.vasenFrame)
                self.nousulaskuLabel["textvariable"]=self.nousulaskuteksti
                self.nousulaskuLabel.pack()    
               

                self.airuskoFrame=Frame(self.vasenFrame)
                self.airuskoFrame.pack()        
                self.airuskoLabel=Label(self.airuskoFrame)
                self.airuskoLabel["text"]="\nAinon ilta/aamurusko"
                self.airuskoLabel.pack({"fill":"x"})    
                        
                self.ainukkuu_h_Scale =Scale(self.airuskoFrame, from_=0, to=24, orient=HORIZONTAL)
                self.ainukkuu_h_Scale["label"]="Arki-ilta: tunti"
                self.ainukkuu_h=IntVar()
                self.ainukkuu_h_Scale["variable"]=self.ainukkuu_h
                self.ainukkuu_h_Scale.pack({"side":"left"})
                self.ainukkuu_min_Scale =Scale(self.airuskoFrame, from_=0, to=60, orient=HORIZONTAL)
                self.ainukkuu_min=IntVar()
                self.ainukkuu_min_Scale["variable"]=self.ainukkuu_min
                self.ainukkuu_min_Scale["label"]="minuutti"
                self.ainukkuu_min_Scale.pack({"side":"left"})
                self.aiheraa_h_Scale =Scale(self.airuskoFrame, from_=0, to=24, orient=HORIZONTAL)
                self.aiheraa_h=IntVar()
                self.aiheraa_h_Scale["variable"]=self.aiheraa_h
                self.aiheraa_h_Scale["label"]="Heratys: tunti"
                self.aiheraa_h_Scale.pack({"side":"left"})
                self.aiheraa_min_Scale =Scale(self.airuskoFrame, from_=0, to=60, orient=HORIZONTAL)
                self.aiheraa_min=IntVar()
                self.aiheraa_min_Scale["variable"]=self.aiheraa_min
                self.aiheraa_min_Scale["label"]="minuutti"
                self.aiheraa_min_Scale.pack({"side":"left"})

                self.airuskovFrame=Frame(self.vasenFrame)
                self.airuskovFrame.pack()        
                #self.airuskoLabel=Label(self.airuskoFrame)
                #self.airuskoLabel["text"]="Ainon ilta/aamurusko"
                #self.airuskoLabel.pack({"fill":"x"})    
                        
                self.ainukkuuv_h_Scale =Scale(self.airuskovFrame, from_=0, to=24, orient=HORIZONTAL)
                self.ainukkuuv_h_Scale["label"]="Viikonloppu: tunti"
                self.ainukkuuv_h=IntVar()
                self.ainukkuuv_h_Scale["variable"]=self.ainukkuuv_h
                self.ainukkuuv_h_Scale.pack({"side":"left"})
                self.ainukkuuv_min_Scale =Scale(self.airuskovFrame, from_=0, to=60, orient=HORIZONTAL)
                self.ainukkuuv_min=IntVar()
                self.ainukkuuv_min_Scale["variable"]=self.ainukkuuv_min
                self.ainukkuuv_min_Scale["label"]="minuutti"
                self.ainukkuuv_min_Scale.pack({"side":"left"})
                self.aiheraav_h_Scale =Scale(self.airuskovFrame, from_=0, to=24, orient=HORIZONTAL)
                self.aiheraav_h=IntVar()
                self.aiheraav_h_Scale["variable"]=self.aiheraav_h
                self.aiheraav_h_Scale["label"]="heratys: tunti"
                self.aiheraav_h_Scale.pack({"side":"left"})
                self.aiheraav_min_Scale =Scale(self.airuskovFrame, from_=0, to=60, orient=HORIZONTAL)
                self.aiheraav_min=IntVar()
                self.aiheraav_min_Scale["variable"]=self.aiheraav_min
                self.aiheraav_min_Scale["label"]="minuutti"
                self.aiheraav_min_Scale.pack({"side":"left"})


                self.juruskoFrame=Frame(self.vasenFrame)
                self.juruskoFrame.pack()        
                self.juruskoLabel=Label(self.juruskoFrame)
                self.juruskoLabel["text"]="\nJuhon ilta/aamurusko"
                self.juruskoLabel.pack({"side":"top", "fill":"x"})      
                        
                self.junukkuu_h_Scale =Scale(self.juruskoFrame, from_=0, to=24, orient=HORIZONTAL)
                self.junukkuu_h_Scale["label"]="Arki-ilta: tunti"
                self.junukkuu_h=IntVar()
                self.junukkuu_h_Scale["variable"]=self.junukkuu_h
                self.junukkuu_h_Scale.pack({"side":"left"})
                self.junukkuu_min_Scale =Scale(self.juruskoFrame, from_=0, to=60, orient=HORIZONTAL)
                self.junukkuu_min=IntVar()
                self.junukkuu_min_Scale["variable"]=self.junukkuu_min
                self.junukkuu_min_Scale["label"]="minuutti"
                self.junukkuu_min_Scale.pack({"side":"left"})
                self.juheraa_h_Scale =Scale(self.juruskoFrame, from_=0, to=24, orient=HORIZONTAL)
                self.juheraa_h=IntVar()
                self.juheraa_h_Scale["variable"]=self.juheraa_h
                self.juheraa_h_Scale["label"]="Juho heratys: tunti"
                self.juheraa_h_Scale.pack({"side":"left"})
                self.juheraa_min_Scale =Scale(self.juruskoFrame, from_=0, to=60, orient=HORIZONTAL)
                self.juheraa_min=IntVar()
                self.juheraa_min_Scale["variable"]=self.juheraa_min
                self.juheraa_min_Scale["label"]="minuutti"
                self.juheraa_min_Scale.pack({"side":"left"})

                self.juruskovFrame=Frame(self.vasenFrame)
                self.juruskovFrame.pack()        
                #self.juruskovLabel=Label(self.juruskoFrame)
                #self.juruskovLabel["text"]="\nJuhon ilta/aamurusko"
                #self.juruskovLabel.pack({"side":"top", "fill":"x"})      
                        
                self.junukkuuv_h_Scale =Scale(self.juruskovFrame, from_=0, to=24, orient=HORIZONTAL)
                self.junukkuuv_h_Scale["label"]="Viikonloppu ilta: tunti"
                self.junukkuuv_h=IntVar()
                self.junukkuuv_h_Scale["variable"]=self.junukkuuv_h
                self.junukkuuv_h_Scale.pack({"side":"left"})
                self.junukkuuv_min_Scale =Scale(self.juruskovFrame, from_=0, to=60, orient=HORIZONTAL)
                self.junukkuuv_min=IntVar()
                self.junukkuuv_min_Scale["variable"]=self.junukkuuv_min
                self.junukkuuv_min_Scale["label"]="minuutti"
                self.junukkuuv_min_Scale.pack({"side":"left"})
                self.juheraav_h_Scale =Scale(self.juruskovFrame, from_=0, to=24, orient=HORIZONTAL)
                self.juheraav_h=IntVar()
                self.juheraav_h_Scale["variable"]=self.juheraav_h
                self.juheraav_h_Scale["label"]="Juho heratys: tunti"
                self.juheraav_h_Scale.pack({"side":"left"})
                self.juheraav_min_Scale =Scale(self.juruskovFrame, from_=0, to=60, orient=HORIZONTAL)
                self.juheraav_min=IntVar()
                self.juheraav_min_Scale["variable"]=self.juheraav_min
                self.juheraav_min_Scale["label"]="minuutti"
                self.juheraav_min_Scale.pack({"side":"left"})


                
                #Muistiasetukset
                self.memoryFrame=Frame(self.vasenFrame)
                self.memoryFrame.pack({"fill":"x"}) 

                self.memoryLabel=Label(self.memoryFrame)
                self.memoryLabel["text"]="Muistiasetukset"
                self.memoryLabel.pack({"fill":"x"})             

                self.memoryFrameAla=Frame(self.memoryFrame)
                self.memoryFrameAla.pack({"side":"bottom","fill":"x"}) 

                self.memoryFrameVasen=Frame(self.memoryFrame)
                self.memoryFrameVasen.pack({"side":"left","fill":"x"}) 

                self.memoryFrameOikea=Frame(self.memoryFrame)
                self.memoryFrameOikea.pack({"side":"left","fill":"x"})

                self.ainooffButton=Checkbutton(self.memoryFrameVasen)
                self.ainooffButton["text"]="Aino offline"
                self.ainooffButton.pack({"anchor":"w"})#{"side":"left"})
                
                self.ainooff=BooleanVar()
                self.ainooff.set(True)
                self.ainooffButton["onvalue"]=True
                self.ainooffButton["offvalue"]=False
                self.ainooffButton["variable"]=self.ainooff

                self.juhooffButton=Checkbutton(self.memoryFrameVasen)
                self.juhooffButton["text"]="Juho offline"
                self.juhooffButton.pack({"anchor":"w"})#{"side":"left"})
                
                self.juhooff=BooleanVar()
                self.juhooff.set(True)
                self.juhooffButton["onvalue"]=True
                self.juhooffButton["offvalue"]=False
                self.juhooffButton["variable"]=self.juhooff


                self.darkmodeButton=Checkbutton(self.memoryFrameVasen)
                self.darkmodeButton["text"]="Sailyta nykyinen valaistus pohjana"
                self.darkmodeButton.pack()#{"side":"left"})
                
                self.darkmode=BooleanVar()
                self.darkmode.set(True)
                self.darkmodeButton["onvalue"]=False ###
                self.darkmodeButton["offvalue"]=True ###
                self.darkmodeButton["variable"]=self.darkmode
               

                self.daymemoryButton=Checkbutton(self.memoryFrameVasen)
                self.daymemoryButton["text"]="Paiva/Ilta/Aamu/Yo \n Valaistukset muistista"
                self.daymemoryButton.pack({"anchor":"w"})#{"side":"left"})
                
                self.daymemory=BooleanVar()
                self.daymemory.set(False)
                self.daymemoryButton["onvalue"]=True
                self.daymemoryButton["offvalue"]=False
                self.daymemoryButton["variable"]=self.daymemory
                
                
  
                self.vuorokaudenaika=StringVar()
                self.vuorokaudenaika.set("Paiva")

                self.memoryFrameOikeaAamu=Frame(self.memoryFrameOikea)
                self.memoryFrameOikeaAamu.pack({"anchor":"w"})
                self.memoryFrameOikeaPaiva=Frame(self.memoryFrameOikea)
                self.memoryFrameOikeaPaiva.pack({"anchor":"w"})
                self.memoryFrameOikeaIlta=Frame(self.memoryFrameOikea)
                self.memoryFrameOikeaIlta.pack({"anchor":"w"})
                self.memoryFrameOikeaYo=Frame(self.memoryFrameOikea)
                self.memoryFrameOikeaYo.pack({"anchor":"w"})

                self.vuorokaudenaikaRadiobutton=Radiobutton(self.memoryFrameOikeaAamu)
                self.vuorokaudenaikaRadiobutton["text"]="Aamu"
                self.vuorokaudenaikaRadiobutton["variable"]=self.vuorokaudenaika
                self.vuorokaudenaikaRadiobutton["value"]="Aamu"
                self.vuorokaudenaikaRadiobutton.pack({"side":"left"})

                self.aamuScale =Scale(self.memoryFrameOikeaAamu, from_=0, to=24, orient=HORIZONTAL)
                self.aamu=IntVar()
                self.aamuScale["variable"]=self.aamu
                #self.aamuScale["label"]="Sade x0.1mm"
                self.aamuScale.pack({"side":"left"})

                                                     
                self.vuorokaudenaikaRadiobutton=Radiobutton(self.memoryFrameOikeaPaiva)
                self.vuorokaudenaikaRadiobutton["text"]="Paiva"
                self.vuorokaudenaikaRadiobutton["variable"]=self.vuorokaudenaika
                self.vuorokaudenaikaRadiobutton["value"]="Paiva"
                self.vuorokaudenaikaRadiobutton.pack({"side":"left"})

                self.paivaScale =Scale(self.memoryFrameOikeaPaiva, from_=0, to=24, orient=HORIZONTAL)
                self.paiva=IntVar()
                self.paivaScale["variable"]=self.paiva
                #self.aamuScale["label"]="Sade x0.1mm"
                self.paivaScale.pack({"side":"left"})

                self.vuorokaudenaikaRadiobutton=Radiobutton(self.memoryFrameOikeaIlta)
                self.vuorokaudenaikaRadiobutton["text"]="Ilta"
                self.vuorokaudenaikaRadiobutton["variable"]=self.vuorokaudenaika
                self.vuorokaudenaikaRadiobutton["value"]="Ilta"
                self.vuorokaudenaikaRadiobutton.pack({"side":"left"})

                self.iltaScale =Scale(self.memoryFrameOikeaIlta, from_=0, to=24, orient=HORIZONTAL)
                self.ilta=IntVar()
                self.iltaScale["variable"]=self.ilta
                #self.aamuScale["label"]="Sade x0.1mm"
                self.iltaScale.pack({"side":"left"})

                self.vuorokaudenaikaRadiobutton=Radiobutton(self.memoryFrameOikeaYo)
                self.vuorokaudenaikaRadiobutton["text"]="Yo"
                self.vuorokaudenaikaRadiobutton["variable"]=self.vuorokaudenaika
                self.vuorokaudenaikaRadiobutton["value"]="Yo"
                self.vuorokaudenaikaRadiobutton.pack({"side":"left"})

                self.yoScale =Scale(self.memoryFrameOikeaYo, from_=0, to=24, orient=HORIZONTAL)
                self.yo=IntVar()
                self.yoScale["variable"]=self.yo
                #self.aamuScale["label"]="Sade x0.1mm"
                self.yoScale.pack({"side":"left"})

                self.daymemoryFile=StringVar()
                self.daymemoryFile.set("Paivamuisti")

                self.daymemoryFileEntry=Entry(self.memoryFrameVasen)
                #self.daymemoryFileEntry["label"]="Paivamuistitiedosto"
                self.daymemoryFileEntry["textvariable"]=self.daymemoryFile
                self.daymemoryFileEntry.pack()

                self.daymemoryladattuFile=StringVar()
                self.daymemoryladattuFile.set("Ei ladattu")
                self.daymemoryladattuLabel=Label(self.memoryFrameVasen)
                #self.daymemoryFileEntry["label"]="Paivamuistitiedosto"
                self.daymemoryladattuLabel["textvariable"]=self.daymemoryladattuFile
                self.daymemoryladattuLabel.pack()

                self.tallennapaivamuisti=BooleanVar()
                self.tallennapaivamuisti.set("False")
                self.tallennamuistiinButton =Button(self.memoryFrameVasen)
                self.tallennamuistiinButton["text"]="Tallenna"
                self.tallennamuistiinButton["command"]=self.tallennamuistiin
                self.tallennamuistiinButton.pack({"side":"left"})

                self.luepaivamuisti=BooleanVar()
                self.luepaivamuisti.set("False")
                self.luepaivamuistiButton =Button(self.memoryFrameVasen)
                self.luepaivamuistiButton["text"]="Lataa"
                self.luepaivamuistiButton["command"]=self.luemuisti
                self.luepaivamuistiButton.pack({"side":"left"})

                
                #Saamaaritykset
                self.weatherFrame=Frame(self)
                self.weatherFrame.pack({"side":"left","fill":"y"})      

                self.weatherLabel=Label(self.weatherFrame)
                self.weatherLabel["text"]="Saa-asetukset"
                self.weatherLabel.pack({"fill":"x"})            

                self.walaFrame=Frame(self.weatherFrame)
                self.walaFrame.pack({"side":"bottom","fill":"both"})  
                self.wvasenFrame=Frame(self.weatherFrame)
                self.wvasenFrame.pack({"side":"top"})   


                self.sunButton=Checkbutton(self.wvasenFrame)
                self.sunButton["text"]="Aurinko/Taivas-efektit kaytossa"
                self.sunButton.pack({"anchor":"w"})
                
                self.sun=BooleanVar()
                self.sun.set(True)
                self.sunButton["onvalue"]=True
                self.sunButton["offvalue"]=False
                self.sunButton["variable"]=self.sun
                
                
                self.weathereffectButton=Checkbutton(self.wvasenFrame)
                self.weathereffectButton["text"]="Saaefektit kaytossa"
                self.weathereffectButton.pack({"anchor":"w"})
                
                self.weathereffect=BooleanVar()
                self.weathereffect.set(True)
                self.weathereffectButton["onvalue"]=True
                self.weathereffectButton["offvalue"]=False
                self.weathereffectButton["variable"]=self.weathereffect
                
                
                self.realweatherButton=Checkbutton(self.wvasenFrame)
                self.realweatherButton["text"]="Todellinen saatila kaytossa (Ilmatieteenlaitos)"
                self.realweatherButton.pack({"anchor":"w"})
                
                self.realweather=BooleanVar()
                self.realweather.set(True)
                self.realweatherButton["onvalue"]=True
                self.realweatherButton["offvalue"]=False
                self.realweatherButton["variable"]=self.realweather
                
                
                self.sadezeroButton=Checkbutton(self.wvasenFrame)
                self.sadezeroButton["text"]="Sade-efekti kaytossa"
                self.sadezeroButton.pack({"anchor":"w"})
                
                self.sadezero=BooleanVar()
                self.sadezero.set(True)
                self.sadezeroButton["onvalue"]=False
                self.sadezeroButton["offvalue"]=True
                self.sadezeroButton["variable"]=self.sadezero


                self.woikeaFrame=Frame(self.wvasenFrame)
                self.woikeaFrame.pack({"side":"right"}) 

                self.sadetuuliFrame=Frame(self.wvasenFrame)
                self.sadetuuliFrame.pack({"side":"right"})


                self.lampotilaScale =Scale(self.sadetuuliFrame, from_=-40, to=30, orient=HORIZONTAL)
                self.lampotila=IntVar()
                self.lampotilaScale["variable"]=self.lampotila
                self.lampotilaScale["label"]="Lampotila"
                self.lampotilaScale.pack({"side":"top"})

                self.sadeScale =Scale(self.sadetuuliFrame, from_=0, to=20, orient=HORIZONTAL)
                self.sade=IntVar()
                self.sadeScale["variable"]=self.sade
                self.sadeScale["label"]="Sade x0.1mm"
                self.sadeScale.pack({"side":"top"})

                self.TuuliScale =Scale(self.sadetuuliFrame, from_=0, to=30, orient=HORIZONTAL)
                self.tuuli=IntVar()
                self.TuuliScale["variable"]=self.tuuli
                self.TuuliScale["label"]="Tuuli m/s"
                self.TuuliScale.pack({"side":"top"})


                
                self.ylapilviScale =Scale(self.woikeaFrame, from_=0, to=100, orient=HORIZONTAL)
                self.ylapilvi=IntVar()
                self.ylapilviScale["variable"]=self.ylapilvi
                self.ylapilviScale["label"]="Ylapilvi %"
                self.ylapilviScale.pack()
                self.keskipilviScale =Scale(self.woikeaFrame, from_=0, to=100, orient=HORIZONTAL)
                self.keskipilvi=IntVar()
                self.keskipilviScale["variable"]=self.keskipilvi
                self.keskipilviScale["label"]="Keskipilvi %"
                self.keskipilviScale.pack()
                self.alapilviScale =Scale(self.woikeaFrame, from_=0, to=100, orient=HORIZONTAL)
                self.alapilvi=IntVar()
                self.alapilviScale["variable"]=self.alapilvi
                self.alapilviScale["label"]="Alapilvi %"
                self.alapilviScale.pack()
                
                #self.ruskonpituusScale =Scale(self.wvasenFrame, from_=0, to=60, orient=VERTICAL)
                #self.ruskonpituusScale["label"]="Ruskon pituus min"
                #self.ruskonpituusScale.pack({"side":"right"})

                self.pilvivariFrame=Frame(self.walaFrame)
                self.pilvivariFrame.pack({"side":"top"})

                self.pilvivariLabel=Label(self.pilvivariFrame)
                #self.auvteksti=StringVar()
                #self.auvteksti.set("Inforuutu")
                #self.auvLabel["textvariable"]=self.infoteksti
                self.pilvivariLabel["text"]="Pilvien varit"
                self.pilvivariLabel.pack({"side":"top"})

                self.ypFrame=Frame(self.pilvivariFrame)
                self.ypFrame.pack({"side":"top"})

                self.auvLabel=Label(self.ypFrame)
                #self.auvteksti=StringVar()
                #self.auvteksti.set("Inforuutu")
                #self.auvLabel["textvariable"]=self.infoteksti
                self.auvLabel["text"]="auri"
                self.auvLabel["background"]="#CCCCCC"
                self.auvLabel.pack({"side":"left"})

                self.skyvLabel=Label(self.ypFrame)
                #self.auvteksti=StringVar()
                #self.auvteksti.set("Inforuutu")
                #self.auvLabel["textvariable"]=self.infoteksti
                self.skyvLabel["text"]="taiv"
                self.skyvLabel["background"]="#CCCCCC"
                self.skyvLabel.pack({"side":"left"})

                self.ypahLabel=Label(self.ypFrame)
                #self.auvteksti=StringVar()
                #self.auvteksti.set("Inforuutu")
                #self.auvLabel["textvariable"]=self.infoteksti
                self.ypahLabel["text"]="ypah"
                self.ypahLabel["background"]="#CCCCCC"
                self.ypahLabel.pack({"side":"left"})

                self.ypalLabel=Label(self.ypFrame)
                #self.auvteksti=StringVar()
                #self.auvteksti.set("Inforuutu")
                #self.auvLabel["textvariable"]=self.infoteksti
                self.ypalLabel["text"]="ypav"
                self.ypalLabel["background"]="#CCCCCC"
                self.ypalLabel.pack({"side":"left"})

                self.kpFrame=Frame(self.pilvivariFrame)
                self.kpFrame.pack({"side":"top"})

                self.kpvhLabel=Label(self.kpFrame)
                #self.auvteksti=StringVar()
                #self.auvteksti.set("Inforuutu")
                #self.auvLabel["textvariable"]=self.infoteksti
                self.kpvhLabel["text"]="kpvh"
                self.kpvhLabel["background"]="#CCCCCC"
                self.kpvhLabel.pack({"side":"left"})

                self.kpvlLabel=Label(self.kpFrame)
                #self.auvteksti=StringVar()
                #self.auvteksti.set("Inforuutu")
                #self.auvLabel["textvariable"]=self.infoteksti
                self.kpvlLabel["text"]="kpvl"
                self.kpvlLabel["background"]="#CCCCCC"
                self.kpvlLabel.pack({"side":"left"})

                self.kpahLabel=Label(self.kpFrame)
                #self.auvteksti=StringVar()
                #self.auvteksti.set("Inforuutu")
                #self.auvLabel["textvariable"]=self.infoteksti
                self.kpahLabel["text"]="kpah"
                self.kpahLabel["background"]="#CCCCCC"
                self.kpahLabel.pack({"side":"left"})

                self.kpalLabel=Label(self.kpFrame)
                #self.auvteksti=StringVar()
                #self.auvteksti.set("Inforuutu")
                #self.auvLabel["textvariable"]=self.infoteksti
                self.kpalLabel["text"]="kpal"
                self.kpalLabel["background"]="#CCCCCC"
                self.kpalLabel.pack({"side":"left"})

                self.apFrame=Frame(self.pilvivariFrame)
                self.apFrame.pack({"side":"top"})

                self.apvhLabel=Label(self.apFrame)
                #self.auvteksti=StringVar()
                #self.auvteksti.set("Inforuutu")
                #self.auvLabel["textvariable"]=self.infoteksti
                self.apvhLabel["text"]="apvh"
                self.apvhLabel["background"]="#CCCCCC"
                self.apvhLabel.pack({"side":"left"})

                self.apvlLabel=Label(self.apFrame)
                #self.auvteksti=StringVar()
                #self.auvteksti.set("Inforuutu")
                #self.auvLabel["textvariable"]=self.infoteksti
                self.apvlLabel["text"]="apvl"
                self.apvlLabel["background"]="#CCCCCC"
                self.apvlLabel.pack({"side":"left"})

                self.apahLabel=Label(self.apFrame)
                #self.auvteksti=StringVar()
                #self.auvteksti.set("Inforuutu")
                #self.auvLabel["textvariable"]=self.infoteksti
                self.apahLabel["text"]="apah"
                self.apahLabel["background"]="#CCCCCC"
                self.apahLabel.pack({"side":"left"})

                self.apalLabel=Label(self.apFrame)
                #self.auvteksti=StringVar()
                #self.auvteksti.set("Inforuutu")
                #self.auvLabel["textvariable"]=self.infoteksti
                self.apalLabel["text"]="apal"
                self.apalLabel["background"]="#CCCCCC"
                self.apalLabel.pack({"side":"left"})

                self.brightmodeButton=Checkbutton(self.pilvivariFrame)
                self.brightmodeButton["text"]="Kirkkaat pilvet kaytossa"
                self.brightmodeButton.pack({"anchor":"w"})
                
                self.brightmode=BooleanVar()
                self.brightmode.set(False)
                self.brightmodeButton["onvalue"]=True
                self.brightmodeButton["offvalue"]=False
                self.brightmodeButton["variable"]=self.brightmode

                self.pilvistylaskuri=IntVar()
                self.pilvistylaskuri.set(100)
                self.pilvistyButton =Button(self.pilvivariFrame)
                self.pilvistyButton["text"]="Pilvisty (15 min)"
                self.pilvistyButton["command"]=self.pilvistyvartti
                self.pilvistyButton.pack({"side":"left"})

                self.kirkastuButton =Button(self.pilvivariFrame)
                self.kirkastuButton["text"]="Kirkastu"
                self.kirkastuButton["command"]=self.kirkastu
                self.kirkastuButton.pack({"side":"left"})

                self.pilvistyhetiButton =Button(self.pilvivariFrame)
                self.pilvistyhetiButton["text"]="Pilvisty Heti"
                self.pilvistyhetiButton["command"]=self.pilvisty
                self.pilvistyhetiButton.pack({"side":"left"})


                
                #NEONSKY
                self.neonskyFrame=Frame(self.walaFrame)
                self.neonskyFrame.pack({"side":"top"})

                self.demoLabel=Label(self.neonskyFrame)
                self.demoLabel["text"]="\n\nNeonsky-moodi"
                self.demoLabel.pack({"fill":"x"})               

                self.neonskyButton=Checkbutton(self.neonskyFrame)
                self.neonskyButton["text"]="Neonsky-efekti kaytossa"
                self.neonskyButton.pack({"anchor":"w"})
                
                self.neonsky=BooleanVar()
                self.neonsky.set(False)
                self.neonskyButton["onvalue"]=True
                self.neonskyButton["offvalue"]=False
                self.neonskyButton["variable"]=self.neonsky

                self.neonskyauFrame=Frame(self.neonskyFrame)
                self.neonskyauFrame.pack()

                self.neonskyskFrame=Frame(self.neonskyFrame)
                self.neonskyskFrame.pack()
                
                self.xneonauScale =Scale(self.neonskyauFrame, from_=10, to=70, orient=HORIZONTAL)
                self.xneonau=IntVar()
                self.xneonau.set(35)
                self.xneonauScale["variable"]=self.xneonau
                self.xneonauScale["label"]="Aur.vari x/100"
                self.xneonauScale.bind('<B1-Motion>',self.neonvari)
                self.xneonauScale.pack({"side":"left"})

                self.yneonauScale =Scale(self.neonskyauFrame, from_=0, to=70, orient=HORIZONTAL)
                self.yneonau=IntVar()
                self.yneonau.set(20)
                self.yneonauScale["variable"]=self.yneonau
                self.yneonauScale["label"]="Aur.vari y/100"
                self.yneonauScale.bind('<B1-Motion>',self.neonvari)
                self.yneonauScale.pack({"side":"left"})

                self.xneonskScale =Scale(self.neonskyskFrame, from_=10, to=70, orient=HORIZONTAL)
                self.xneonsk=IntVar()
                self.xneonsk.set(25)
                self.xneonskScale["variable"]=self.xneonsk
                self.xneonskScale["label"]="Taiv.vari x/100"
                self.xneonskScale.bind('<B1-Motion>',self.neonvari)
                self.xneonskScale.pack({"side":"left"})

                self.yneonskScale =Scale(self.neonskyskFrame, from_=0, to=70, orient=HORIZONTAL)
                self.yneonsk=IntVar()
                self.yneonsk.set(50)
                self.yneonskScale["variable"]=self.yneonsk
                self.yneonskScale["label"]="Taiv.vari y/100"
                self.yneonskScale.bind('<B1-Motion>',self.neonvari)
                self.yneonskScale.pack({"side":"left"})

                self.neonvari("initial")
                
                #Demomoodi
                self.demoFrame=Frame(self.walaFrame)
                self.demoFrame.pack({"side":"bottom"})

                self.demoLabel=Label(self.demoFrame)
                self.demoLabel["text"]="Demo-moodi"
                self.demoLabel.pack({"fill":"x"})               
                
                
                
                self.demomodeButton=Checkbutton(self.demoFrame)
                self.demomodeButton["text"]="Demomoodi"
                self.demomodeButton.pack()
                
                self.demomode=BooleanVar()
                self.demomode.set(False)
                self.demomodeButton["onvalue"]=True
                self.demomodeButton["offvalue"]=False
                self.demomodeButton["variable"]=self.demomode
                
                
                
                self.QUIT = Button(self.alaFrame)
                self.QUIT["text"]="Jatka"
                #self.QUIT["fg"]="red"
                #self.QUIT["bg"]="blue"
                self.QUIT["command"]=self.quit
                
                self.QUIT.pack({"side":"right"})
                

                self.muokkaa=BooleanVar()
                self.muokkaa.set(False)
                self.muokkaaButton =Button(self.alaFrame)
                self.muokkaaButton["text"]="Muokkaa"
                self.muokkaaButton["command"]=self.muokkaamuutos
                
                self.muokkaaButton.pack({"side":"right"})


                self.lopeta=BooleanVar()
                self.lopeta.set(False)
                self.lopetaButton =Button(self.alaFrame)
                self.lopetaButton["text"]="Lopeta ohjelma"
                self.lopetaButton["command"]=self.lopetaohjelma
                
                self.lopetaButton.pack({"side":"right"})
                
                #self.tekstisyotto = Entry(self.alaFrame)
                #self.tekstisyotto.pack()
                #
                #self.teksti=StringVar()
                #self.teksti.set("Tere")
                #self.tekstisyotto["textvariable"]=self.teksti
                
                #self.tekstisyotto.bind('<Key-Return>',self.print_content)

                self.infoLabel=Label(self.alaFrame)
                self.infoteksti=StringVar()
                self.infoteksti.set("Inforuutu")
                self.infoLabel["textvariable"]=self.infoteksti
                self.infoLabel["background"]="#CCCCCC"
                self.infoLabel.pack({"anchor":"w"})
	
        def __init__(self,master=None):
                Frame.__init__(self,master)
                self.pack()
                self.createWidgets()
###########################################################
def AsetaPilvivaritUI(UIid,xau,yau,briau,xsk,ysk,brisk,wau,wsk,tncl,v_au):
        xcl=[0.0]*len(wau)
        ycl=[0.0]*len(wau)
        bricl=[0.0]*len(wau)
        clcolor=["#000000"]*len(wau)
        txt=[""]*len(wau)
        clnimet=["auri","taiv","ypah","ypal","kpvh","kpvl","kpah","kpal","apvh","apvl","apah","apal"]

        for i in range(len(wau)):
                wei=wau[i]/(wsk[i]+wau[i])
                xcl[i],ycl[i],bricl[i],scale=WeightColorXY(xau, yau, briau, xsk, ysk, brisk,wei)
                #bricl[i]=bricl[i]*(wau[i]+wsk[i])/2
                if hui.brightmode.get():
                        bricl[i]=briau
                        if briau<brisk:
                                bricl[i]=brisk
                else:
                        bricl[i]=bricl[i]*(wau[i]+wsk[i])/2
                
                bricl[0]=briau*vis_au
                bricl[1]=brisk
                if briau>brisk:
                        bricl[1]=briau
                if bricl[i]>255:
                        bricl[i]=255
                R,G,B=RGBColor(xcl[i],ycl[i],bricl[i])
                Rh=hex(R+256)
                Gh=hex(G+256)
                Bh=hex(B+256)
                clcolor[i]="#"+Rh[3:len(Rh)]+Gh[3:len(Gh)]+Bh[3:len(Bh)]

                if i<2:
                        txt[i]=txt[i]+" "*int(tncl[i]*30)
                else:
                        txt[i]=txt[i]+" "*int(tncl[i]*60)

                #print clcolor[i], bricl[i]
                #print clcolor[i], "#"+Rh[3:len(Rh)]+Gh[3:len(Gh)]+Bh[3:len(Bh)]
        
        #print clcolor, bricl
        UIid.auvLabel["background"]=clcolor[0]
        UIid.skyvLabel["background"]=clcolor[1]
        UIid.ypahLabel["background"]=clcolor[2]
        UIid.ypalLabel["background"]=clcolor[3]
        UIid.kpvhLabel["background"]=clcolor[4]
        UIid.kpvlLabel["background"]=clcolor[5]
        UIid.kpahLabel["background"]=clcolor[6]
        UIid.kpalLabel["background"]=clcolor[7]
        UIid.apvhLabel["background"]=clcolor[8]
        UIid.apvlLabel["background"]=clcolor[9]
        UIid.apahLabel["background"]=clcolor[10]
        UIid.apalLabel["background"]=clcolor[11]


        UIid.auvLabel["text"]=txt[0]
        UIid.skyvLabel["text"]=txt[1]
        UIid.ypahLabel["text"]=txt[2]
        UIid.ypalLabel["text"]=txt[3]
        UIid.kpvhLabel["text"]=txt[4]
        UIid.kpvlLabel["text"]=txt[5]
        UIid.kpahLabel["text"]=txt[6]
        UIid.kpalLabel["text"]=txt[7]
        UIid.apvhLabel["text"]=txt[8]
        UIid.apvlLabel["text"]=txt[9]
        UIid.apahLabel["text"]=txt[10]
        UIid.apalLabel["text"]=txt[11]
        

############### Varsinainen koodi alkaa ###################
#Flagit
dynamic = False
daymemory = False
sun = True
demomode = False
datepreset=True
dateactual =False
readdaymemory = True
savedaymemory = False
weathereffect=True
sadezero=True
realweather=False #True
demoahue=False #demomode
darkmode=True
nimikaskytys=False
lyhty = True
lyhtyautomatiikka = True
lyhty_x=[0.675,0.650,0.622,0.597,0.572,0.549,0.527,0.506,0.487,0.470,0.453,0.438]
lyhty_y=[0.320,0.347,0.370,0.389,0.403,0.412,0.417,0.420,0.419,0.417,0.414,0.410]
lyhty_bri =[4, 140, 160, 180, 200, 210, 220, 230, 240, 220, 200]
#lyhty_bri =[30, 100, 140, 170, 190, 205, 215, 225, 235, 245, 255]


au=True
sk=True

sky_T=float(10)
daypreset=int(99)
position=[65.0,25.46820]
place="Oulu"
hshiftpreset=1.9
day=int(99) #for fixed date mode
h=float(19.00)
hshift=1.9

weather=[-17.0,12.0,17.0,0.5,0.1,10.0,10.0,10.0,50.0] # for fixed weather mode
#weather=[0.0,12.0,12.0,0.5,0.1,10.0,10.0,10.0,90.0] # for fixed weather mode


ai_nukkuu = 21.25
ai_nukkuu_viikonloppu = 21.25
ai_ruskokesto = 7.0/60.0 #20 min
ai_heraa = 6.5
ai_heraa_viikonloppu = 7.5

ju_nukkuu = 21.25
ju_nukkuu_viikonloppu = 21.25
ju_ruskokesto = 15.0/60.0 #15 min
ju_heraa = 7.0
ju_heraa_viikonloppu = 8.25

t_aa=6.5
t_pai=9
t_il=17
t_yo=22

##################
#TESTIPÄTKÄ
#ajbutt=34

ajbutt,lastupdate=GetHueButtonevent()
#print ajbutt
#print lastupdate
#####################
        
id_au = ["5","7","8","9","6","10","11","12","17","18"] #Aurinko
id_sk = ["4","13","14","15","16"] #Taivas
id_ai = ["3"]
id_ju = ["2"]
id_ly = ["10","12","17","18","11","9","16"]

pos_au=[40,-20,10,-30,-50,70,80,60,40,50]
pos_sk=[40,89,50,50,50]

on_au=[True]*len(id_au)
on_sk=[True]*len(id_sk)

if True: #nimikaskytys:
        id_kasky =["6","2","3","5","7"]
        kasky_realname=["NoName"]*len(id_kasky)
        kasky_name=["NoName"]*len(id_kasky)
        kasky_reach=[True]*len(id_kasky)
        valotpois=False
        valothimm=False
        GetHueName(id_kasky, kasky_realname,kasky_reach)
        print kasky_realname, kasky_reach
        ainooff=False
        ainokeep=False
        juhooff=False
        juhokeep=False
        vaihtelevaa=False

#########kayttis kayntiin#######

juuri=Tk()
hui=Application(master=juuri)

hui.datepreset.set(datepreset)
hui.dateactual.set(dateactual)
time_local=time.localtime()
if dateactual:
        day=time_local.tm_yday
hoik=float(time_local.tm_hour)+(float(time_local.tm_min))/60.0


hui.vuodenpaiva.set(int(day))
hui.hshift.set(int(hshift*60))
hui.nousulasku("init")

hui.ainukkuu_h.set(int(ai_nukkuu))
hui.ainukkuu_min.set(int(60*(ai_nukkuu-float(int(ai_nukkuu)))))
hui.aiheraa_h.set(int(ai_heraa))
hui.aiheraa_min.set(int(60*(ai_heraa-float(int(ai_heraa)))))

hui.ainukkuuv_h.set(int(ai_nukkuu_viikonloppu))
hui.ainukkuuv_min.set(int(60*(ai_nukkuu_viikonloppu-float(int(ai_nukkuu_viikonloppu)))))
hui.aiheraav_h.set(int(ai_heraa_viikonloppu))
hui.aiheraav_min.set(int(60*(ai_heraa_viikonloppu-float(int(ai_heraa_viikonloppu)))))

hui.junukkuu_h.set(int(ju_nukkuu))
hui.junukkuu_min.set(int(60*(ju_nukkuu-float(int(ju_nukkuu)))))
hui.juheraa_h.set(int(ju_heraa))
hui.juheraa_min.set(int(60*(ju_heraa-float(int(ju_heraa)))))

hui.junukkuuv_h.set(int(ju_nukkuu_viikonloppu))
hui.junukkuuv_min.set(int(60*(ju_nukkuu_viikonloppu-float(int(ju_nukkuu_viikonloppu)))))
hui.juheraav_h.set(int(ju_heraa_viikonloppu))
hui.juheraav_min.set(int(60*(ju_heraa_viikonloppu-float(int(ju_heraa_viikonloppu)))))


hui.daymemory.set(daymemory)
hui.darkmode.set(darkmode)

hui.aamu.set(int(t_aa))
hui.paiva.set(int(t_pai))
hui.ilta.set(int(t_il))
hui.yo.set(int(t_yo))

hui.sun.set(sun)
hui.weathereffect.set(weathereffect)
hui.realweather.set(realweather)
hui.sadezero.set(sadezero)

weatherold=weather
if realweather:
        try:
                weather=GetFMIWeatherForecast("oulu")
        except:
                weather=weatherold
                print "%%%%%%%%%%%%%%%%\n Saata ei voinut hakea"
hui.lampotila.set(int(weather[0]))
hui.sade.set(int(weather[4]))
hui.tuuli.set(int(weather[1]))
hui.alapilvi.set(int(weather[5]))
hui.keskipilvi.set(int(weather[6]))
hui.ylapilvi.set(int(weather[7]))

hui.demomode.set(demomode)

hui.infoteksti.set(str(int(hoik))+":"+str(int((hoik-int(hoik))*60)))

sky_T=((weather[0]+40.0)/80.0*6.25+3.125) #huom korjattu mallin arvottua sirontaa vastaavaksi 5-15 km => 3-10 km
sunheight=AuKorkeus(day,hoik,float(65))

x_au,y_au,bri_au,vis_au=AuVariXY(sunheight,sky_T)
x_sk,y_sk,bri_sk=SkyVariXY(sunheight,sky_T)
if hui.neonsky.get():
        x_au=float(hui.xneonau.get())/100
        y_au=float(hui.yneonau.get())/100
        x_sk=float(hui.xneonsk.get())/100
        y_sk=float(hui.yneonsk.get())/100
                        #if bri_sk<bri_au:
                        #        bri_sk=bri_au

print day, h+hshift,sunheight #, x_au,y_au,bri_au
hui.infoteksti.set(hui.infoteksti.get()+" AUR kulma:"+str(float(int(sunheight*10))/10))

waur,wsky,cltn=CloudRandom(weather[5],weather[6],weather[7], True,hui.brightmode.get())
AsetaPilvivaritUI(hui,x_au,y_au,bri_au,x_sk,y_sk,bri_sk,waur,wsky,cltn,vis_au)



########################
xu_1,yu_1,briu_1,x_1,y_1,bri_1=InitialiseLights(id_au)
xu_2,yu_2,briu_2,x_2,y_2,bri_2=InitialiseLights(id_sk)

if darkmode:
        briu_1=[0.0]*len(id_au)
        briu_2=[0.0]*len(id_sk)
        xu_1=[.15]*len(id_au)
        xu_2=[.15]*len(id_sk)
        yu_1=[.05]*len(id_au)
        yu_2=[.05]*len(id_sk)


xold_1=[.33]*len(id_au)
yold_1=[.33]*len(id_au)
briold_1=[1.0]*len(id_au)
xold_2=[.33]*len(id_au)
yold_2=[.33]*len(id_au)
briold_2=[1.0]*len(id_au)


if True: #daymemory
        xyo_1,yyo_1,briyo_1,xpai_1,ypai_1,bripai_1=InitialiseLights(id_au)
        xyo_2,yyo_2,briyo_2,xpai_2,ypai_2,bripai_2=InitialiseLights(id_sk)
        xaa_1,yaa_1,briaa_1,xil_1,yil_1,briil_1=InitialiseLights(id_au)
        xaa_2,yaa_2,briaa_2,xil_2,yil_2,briil_2=InitialiseLights(id_sk)

        
        daymemoryFile ="Daymemory"
        notsaved= True
        
        
        if readdaymemory:
                print "Reading daymemory"
                ReadLightMemory(daymemoryFile+"Yo.txt",id_au,xyo_1,yyo_1,briyo_1)
                ReadLightMemory(daymemoryFile+"Yo.txt",id_sk,xyo_2,yyo_2,briyo_2)
                ReadLightMemory(daymemoryFile+"Aa.txt",id_au,xaa_1,yaa_1,briaa_1)
                ReadLightMemory(daymemoryFile+"Aa.txt",id_sk,xaa_2,yaa_2,briaa_2)
                ReadLightMemory(daymemoryFile+"Pai.txt",id_au,xpai_1,ypai_1,bripai_1)
                ReadLightMemory(daymemoryFile+"Pai.txt",id_sk,xpai_2,ypai_2,bripai_2)
                ReadLightMemory(daymemoryFile+"Il.txt",id_au,xil_1,yil_1,briil_1)
                ReadLightMemory(daymemoryFile+"Il.txt",id_sk,xil_2,yil_2,briil_2)
        
        #SaveLightMemory(daymemoryFile+"Yo.txt", id_au+id_sk,xyo_1+xyo_2,yyo_1+yyo_2,briyo_1+briyo_2)
        #SaveLightMemory(daymemoryFile+"Pai.txt", id_au+id_sk,xpai_1+xpai_2,ypai_1+ypai_2,bripai_1+bripai_2)
        #SaveLightMemory(daymemoryFile+"Aa.txt", id_au+id_sk,xaa_1+xaa_2,yaa_1+yaa_2,briaa_1+briaa_2)
        #SaveLightMemory(daymemoryFile+"Il.txt", id_au+id_sk,xil_1+xil_2,yil_1+yil_2,briil_1+briil_2)

hui.muokkaa.set(True)
while hui.muokkaa.get()==True:
        hui.muokkaa.set(False)
        hui.infoteksti.set("Muokkaa ja paina sitten 'Jatka'")
        hui.QUIT["bg"]="green"
        hui.mainloop()
        hui.QUIT["bg"]="gray"
        if hui.tallennapaivamuisti.get():
                print "Saving daymemory "+hui.daymemoryFile.get()+hui.vuorokaudenaika.get()
                hui.tallennapaivamuisti.set(False)
                xu_1,yu_1,briu_1,x_1,y_1,bri_1=InitialiseLights(id_au)
                xu_2,yu_2,briu_2,x_2,y_2,bri_2=InitialiseLights(id_sk)
                SaveLightMemory(hui.daymemoryFile.get()+hui.vuorokaudenaika.get()+".txt", id_au+id_sk,xu_1+xu_2,yu_1+yu_2,briu_1+briu_2)
                hui.infoteksti.set(hui.daymemoryFile.get()+hui.vuorokaudenaika.get()+".txt Tallennettu")
                hui.muokkaa.set(True)
        if hui.luepaivamuisti.get():
                print "Reading daymemory"
                hui.muokkaa.set(True)
                hui.luepaivamuisti.set(False)
                daymemoryFile=hui.daymemoryFile.get()
                hui.daymemoryladattuFile.set(daymemoryFile+" ladattu kayttoon")
                try:
                        ReadLightMemory(daymemoryFile+"Yo.txt",id_au,xyo_1,yyo_1,briyo_1)
                        ReadLightMemory(daymemoryFile+"Yo.txt",id_sk,xyo_2,yyo_2,briyo_2)
                except:
                        print daymemoryFile+"Yo.txt ei luettavissa"
                        hui.daymemoryladattuFile.set(daymemoryFile+"Yo ei luettavissa")
                try:
                        ReadLightMemory(daymemoryFile+"Aamu.txt",id_au,xaa_1,yaa_1,briaa_1)
                        ReadLightMemory(daymemoryFile+"Aamu.txt",id_sk,xaa_2,yaa_2,briaa_2)
                except:
                        print daymemoryFile+"Aamu.txt ei luettavissa"
                        hui.daymemoryladattuFile.set(daymemoryFile+"Aamu ei luettavissa")
                try:
                        ReadLightMemory(daymemoryFile+"Paiva.txt",id_au,xpai_1,ypai_1,bripai_1)
                        ReadLightMemory(daymemoryFile+"Paiva.txt",id_sk,xpai_2,ypai_2,bripai_2)
                except:
                        print daymemoryFile+"Paiva.txt ei luettavissa"
                        hui.daymemoryladattuFile.set(daymemoryFile+"Paiva ei luettavissa")
                try:
                        ReadLightMemory(daymemoryFile+"Ilta.txt",id_au,xil_1,yil_1,briil_1)
                        ReadLightMemory(daymemoryFile+"Ilta.txt",id_sk,xil_2,yil_2,briil_2)
                except:
                        print daymemoryFile+"Ilta.txt ei luettavissa"
                        hui.daymemoryladattuFile.set(daymemoryFile+"Ilta ei luettavissa")
#juuri.destroy()

demomode=hui.demomode.get()



ttime=6000
if demomode:
        ttime=70


T=0

if demomode:
        iddemo=["10","11","4","6","1","7","8","5","9"]
        HueDemo(iddemo)

        
while hui.lopeta.get()==False:
        conn = httplib.HTTPConnection(hueaddress)
        hui.breakloop.set(False)
#####
        ttime=4000
        on_au=[True]*len(id_au)
        on_sk=[True]*len(id_sk)

        if demomode:
                ttime=10 #70 ######################################

        
        if nimikaskytys:
                GetHueName(id_kasky, kasky_name,kasky_reach)
                if kasky_name[0]!=kasky_realname[0]:
                        if kasky_name[0]=="neon":
                                hui.neonsky.set(not(hui.neonsky.get()))
                        if kasky_name[0]=="lopeta":
                                hui.lopeta.set(True)
                                hui.breakloop.set(True)
                        if kasky_name[0]=="fmi":
                                hui.realweather.set(not(hui.realweather.get()))
                                hui.weathereffect.set(True)
                                hui.sun.set(True)
                                vaihtelevaa=False
                        if kasky_name[0][0:7]=="paikka:":
                                hui.realweather.set(True)
                                place=kasky_name[0][7:len(kasky_name[0])]
                                try:
                                        weather,position,place=GetFMIWeatherForecast(place)
                                except:
                                        print "ERROR: Paikka: "+place+" ei mahdollinen! Palaamme Ouluun."
                                        place="Oulu"
                                        position=[65.0,25.46820]        
                                hui.leveyspiiri.set(position[0])
                                hui.weathereffect.set(True)
                                hui.sun.set(True)
                                hui.dateactual.set(True)
                                hui.datepreset.set(False)
                                hui.breakloop.set(True)
                                vaihtelevaa=False
                        if kasky_name[0]=="esiasetus":
                                hui.datepreset.set(True)
                        if kasky_name[0]=="saa":
                                hui.weathereffect.set(not(hui.weathereffect.get()))
                                hui.sun.set(True)
                                vaihtelevaa=False
                        if kasky_name[0]=="vainsaa":
                                hui.weathereffect.set(True)
                                hui.sun.set(True)
                                hui.daymemory.set(False)
                                vaihtelevaa=False
                        if kasky_name[0]=="sun":
                                hui.sun.set(not(hui.sun.get()))
                        if kasky_name[0]=="pilveen":
                                hui.sun.set(True)
                                hui.realweather.set(False)
                                hui.weathereffect.set(True)
                                hui.pilvisty()
                                hui.breakloop.set(False)
                                vaihtelevaa=False
                        if kasky_name[0]=="vaihtelevaa":
                                hui.sun.set(True)
                                hui.realweather.set(False)
                                hui.weathereffect.set(True)
                                vaihtelevaa=not(vaihtelevaa)
                        if kasky_name[0]=="pilvisty":
                                hui.sun.set(True)
                                hui.realweather.set(False)
                                hui.weathereffect.set(True)
                                hui.pilvistyvartti()
                                hui.breakloop.set(False)
                                vaihtelevaa=False
                        if kasky_name[0]=="selkene":
                                hui.sun.set(True)
                                hui.realweather.set(False)
                                hui.weathereffect.set(True)
                                hui.kirkastu()
                                hui.breakloop.set(False)
                                vaihtelevaa=False
                        if kasky_name[0]=="kirkas":
                                hui.sun.set(True)
                                hui.weathereffect.set(True)
                                hui.brightmode.set(not(hui.brightmode.get()))
                        if kasky_name[0]=="muisti":
                                hui.daymemory.set(not(hui.daymemory.get()))
                        if kasky_name[0]=="vainmuisti":
                                hui.realweather.set(False)
                                hui.weathereffect.set(False)
                                hui.sun.set(False)
                                hui.daymemory.set(True)
                        SetHueName(id_kasky, kasky_realname)
                if kasky_reach[0]==False:
                        if valothimm==False:
                                hui.sun.set(True)
                                hui.weathereffect.set(True)
                                hui.pilvisty()
                                hui.breakloop.set(False)
                                hui.brightmode.set(False)
                                hui.daymemory.set(False)
                                valothimm=True
                else:
                        if valothimm==True:
                                hui.sun.set(True)
                                hui.weathereffect.set(True)
                                valothimm=False
                                hui.kirkastu()
                                hui.breakloop.set(False)
                                hui.brightmode.set(True)
                if kasky_reach[3]==False:
                        if kasky_reach[4]==False:
                                valotpois=True
                        else:
                                valotpois=False
                                hui.realweather.set(False)
                                hui.weathereffect.set(False)
                                hui.sun.set(False)
                                hui.daymemory.set(True)                                
                else:
                        valotpois=False
                        if kasky_reach[4]==False:
                                hui.weathereffect.set(True)
                                hui.sun.set(True)
                                hui.daymemory.set(False)

                if kasky_reach[1]==False:
                        if juhokeep==False:
                                hui.juhooff.set(not(hui.juhooff.get()))
                                SetHue([id_kasky[0]],[255], [0.7], [0.3], 1)
                                if hui.juhooff.get():
                                        print "Juhon valot poissa"        
                                else:
                                        print "Juhon valot mukana"
                        juhokeep=True
                else:
                        juhokeep=False
                        
                if kasky_reach[2]==False:
                        if ainokeep==False:
                                hui.ainooff.set(not(hui.ainooff.get()))
                                SetHue([id_kasky[0]],[255], [0.35], [0.15], 1)
                                if hui.ainooff.get():
                                        print "Ainon valot poissa"
                                else:
                                        print "Ainon valot mukana"
                        ainokeep=True
                else:
                        ainokeep=False



        while hui.muokkaa.get()==True:
                hui.muokkaa.set(False)
                hui.infoteksti.set("Muokkaa ja paina sitten 'Jatka'")
                hui.QUIT["bg"]="green"
                hui.mainloop()
                hui.QUIT["bg"]="gray"
                if hui.tallennapaivamuisti.get():
                        print "Saving daymemory "+hui.daymemoryFile.get()+hui.vuorokaudenaika.get()
                        hui.tallennapaivamuisti.set(False)
                        xu_1,yu_1,briu_1,x_1,y_1,bri_1=InitialiseLights(id_au)
                        xu_2,yu_2,briu_2,x_2,y_2,bri_2=InitialiseLights(id_sk)
                        SaveLightMemory(hui.daymemoryFile.get()+hui.vuorokaudenaika.get()+".txt", id_au+id_sk,xu_1+xu_2,yu_1+yu_2,briu_1+briu_2)
                        hui.infoteksti.set(hui.daymemoryFile.get()+hui.vuorokaudenaika.get()+".txt Tallennettu")
                        hui.muokkaa.set(True)
                if hui.luepaivamuisti.get():
                        print "Reading daymemory"
                        hui.muokkaa.set(True)
                        hui.luepaivamuisti.set(False)
                        daymemoryFile=hui.daymemoryFile.get()
                        hui.daymemoryladattuFile.set(daymemoryFile+" ladattu kayttoon")
                        try:
                                ReadLightMemory(daymemoryFile+"Yo.txt",id_au,xyo_1,yyo_1,briyo_1)
                                ReadLightMemory(daymemoryFile+"Yo.txt",id_sk,xyo_2,yyo_2,briyo_2)
                        except:
                                print daymemoryFile+"Yo.txt ei luettavissa"
                                hui.daymemoryladattuFile.set(daymemoryFile+"Yo ei luettavissa")
                        try:
                                ReadLightMemory(daymemoryFile+"Aamu.txt",id_au,xaa_1,yaa_1,briaa_1)
                                ReadLightMemory(daymemoryFile+"Aamu.txt",id_sk,xaa_2,yaa_2,briaa_2)
                        except:
                                print daymemoryFile+"Aamu.txt ei luettavissa"
                                hui.daymemoryladattuFile.set(daymemoryFile+"Aamu ei luettavissa")
                        try:
                                ReadLightMemory(daymemoryFile+"Paiva.txt",id_au,xpai_1,ypai_1,bripai_1)
                                ReadLightMemory(daymemoryFile+"Paiva.txt",id_sk,xpai_2,ypai_2,bripai_2)
                        except:
                                print daymemoryFile+"Paiva.txt ei luettavissa"
                                hui.daymemoryladattuFile.set(daymemoryFile+"Paiva ei luettavissa")
                        try:
                                ReadLightMemory(daymemoryFile+"Ilta.txt",id_au,xil_1,yil_1,briil_1)
                                ReadLightMemory(daymemoryFile+"Ilta.txt",id_sk,xil_2,yil_2,briil_2)
                        except:
                                print daymemoryFile+"Ilta.txt ei luettavissa"
                                hui.daymemoryladattuFile.set(daymemoryFile+"Ilta ei luettavissa")
                        
        #if hui.lopeta.get()==True:
        #        break
        
        datepreset=hui.datepreset.get()
        if datepreset:
                dateactual=False
                hui.vuodenpaiva.set(daypreset)
                hui.hshift.set(int(hshiftpreset*60))
                hui.dateactual.set(False)
                place="Oulu"
                position=[65.0,25.46820]
        else:
                dateactual=hui.dateactual.get()
        time_local=time.localtime()
        if dateactual:
                day=time_local.tm_yday
                hui.vuodenpaiva.set(int(day))
                hshift=AuPituuspiiriKorjaus(position[1]) #25.46820) #Oulun pituuspiiri
                hshift=hshift-AuEoTKorjaus(float(day))
                hui.hshift.set(int(hshift))
        else:
                day=hui.vuodenpaiva.get()
        hshift=float(hui.hshift.get())/60
        hui.nousulasku("hei")

        ajbutt_old = ajbutt
        lastupdate_old =lastupdate
        try:
                ajbutt, lastupdate =GetHueButtonevent()
        except:
                ajbutt = ajbutt_old
                lastupdate = lastupdate_old
                
        print ajbutt
        h=float(time_local.tm_hour)+(float(time_local.tm_min))/60.0
        if not(lastupdate == lastupdate_old):
                if h>12:
                        if ajbutt==18:
                                h=h+ai_ruskokesto
                                hui.ainukkuu_h.set(int(h))
                                hui.ainukkuu_min.set(int(60*(h-float(int(h)))))
                                hui.ainukkuuv_h.set(int(h))
                                hui.ainukkuuv_min.set(int(60*(h-float(int(h)))))
                        if ajbutt==16:
                                h=h+ju_ruskokesto
                                hui.junukkuu_h.set(int(h))
                                hui.junukkuu_min.set(int(60*(h-float(int(h)))))
                                hui.junukkuuv_h.set(int(h))
                                hui.junukkuuv_min.set(int(60*(h-float(int(h)))))
                else:
                        if ajbutt==18:
                                hui.aiheraa_h.set(int(h))
                                hui.aiheraa_min.set(int(60*(h-float(int(h)))))
                                hui.aiheraav_h.set(int(h))
                                hui.aiheraav_min.set(int(60*(h-float(int(h)))))
                        if ajbutt==16:
                                hui.juheraa_h.set(int(h))
                                hui.juheraa_min.set(int(60*(h-float(int(h)))))
                                hui.juheraav_h.set(int(h))
                                hui.juheraav_min.set(int(60*(h-float(int(h)))))
                if ajbutt==17:
                        lyhty = not(lyhty)
                        lyhtyautomatiikka = False
                if ajbutt ==34:
                        if valothimm==False:
                                hui.sun.set(True)
                                hui.weathereffect.set(True)
                                hui.pilvisty()
                                hui.breakloop.set(False)
                                hui.brightmode.set(False)
                                hui.daymemory.set(False)
                                valothimm=True
                        else:
                                hui.sun.set(True)
                                hui.weathereffect.set(True)
                                valothimm=False
                                hui.kirkastu()
                                hui.breakloop.set(False)
                                #hui.brightmode.set(True)



        ai_nukkuu=float(hui.ainukkuu_h.get())
        ai_nukkuu=ai_nukkuu+float(hui.ainukkuu_min.get())/60.0
        ai_heraa=float(hui.aiheraa_h.get())
        ai_heraa=ai_heraa+float(hui.aiheraa_min.get())/60.0

        ai_nukkuu_viikonloppu=float(hui.ainukkuuv_h.get())
        ai_nukkuu_viikonloppu=ai_nukkuu_viikonloppu+float(hui.ainukkuuv_min.get())/60.0
        ai_heraa_viikonloppu=float(hui.aiheraav_h.get())
        ai_heraa_viikonloppu=ai_heraa_viikonloppu+float(hui.aiheraav_min.get())/60.0


        ju_nukkuu=float(hui.junukkuu_h.get())
        ju_nukkuu=ju_nukkuu+float(hui.junukkuu_min.get())/60.0
        ju_heraa=float(hui.juheraa_h.get())
        ju_heraa=ju_heraa+float(hui.juheraa_min.get())/60.0

        ju_nukkuu_viikonloppu=float(hui.junukkuuv_h.get())
        ju_nukkuu_viikonloppu=ju_nukkuu_viikonloppu+float(hui.junukkuuv_min.get())/60.0
        ju_heraa_viikonloppu=float(hui.juheraav_h.get())
        ju_heraa_viikonloppu=ju_heraa_viikonloppu+float(hui.juheraav_min.get())/60.0


        daymemory=hui.daymemory.get()
        darkmode=hui.darkmode.get() #HUOM EI VAIKUTUSTA...
        if darkmode:
                briu_1=[0.0]*len(id_au)
                briu_2=[0.0]*len(id_sk)
        
        t_aa=hui.aamu.get()
        t_pai=hui.paiva.get()
        t_il=hui.ilta.get()
        t_yo=hui.yo.get()

        sun=hui.sun.get()
        weathereffect = hui.weathereffect.get()
        realweather=hui.realweather.get()
        sadezero=hui.sadezero.get()


        if not(realweather):
                weather[0]=float(hui.lampotila.get())
                weather[4]=float(hui.sade.get())
                weather[1]=float(hui.tuuli.get())
                weather[2]=float(hui.tuuli.get())
                weather[5]=float(hui.alapilvi.get())
                weather[6]=float(hui.keskipilvi.get())
                weather[7]=float(hui.ylapilvi.get())
            

        demomode=hui.demomode.get()



#####
        sade=0
        au=True
        sk=True
#        if demomode:
#                sade=0;#pow(random.random(),2)
#                weather=[0.0,0.0,0.0,0.0,sade,random.random()*100,random.random()*100,random.random()*100,random.random()*100]
#                weather[5]=40.0#*random.random()
#                weather[6]=30.0#*random.random()
#                weather[7]=10.0#*random.random()
#                print "Pilvisyys fiksattu:", weather[5], weather[6], weather[7]
#
#                print "Demo", weather 

        if weathereffect: #&(not(demomode)):
                weatherold=weather
                if realweather:
                        try:
                                weather,position,place=GetFMIWeatherForecast(place)
                                hui.leveyspiiri.set(position[0])
                        except:
                                weather=weatherold
                                print "%%%%%%%%%%%%%%%%\n Saata ei voinut hakea"
                else:
                        print "Weather fixed"
                #weather=[0.0,2.0,7.0,0.5,0.1,30.0,30.0,10.0,50.0]
                if nimikaskytys:
                        if vaihtelevaa:
                                print "Vaihtelevaa saata"
                                weather[0]=weather[0]+random.random()*4-2
                                if weather[0]<-30:
                                        weather[0]=-30
                                if weather[0]>30:
                                        weather[0]=30
                                j=[5,7]
                                for i in j:
                                        weather[i]=weather[i]+random.random()*100-50
                                        if weather[i]<0:
                                                weather[i]=0
                                        if weather[i]>100:
                                                weather[i]=100
                                        
                
                print weather
                hui.lampotila.set(int(weather[0]))
                hui.sade.set(int(weather[4]))
                hui.tuuli.set(int(weather[1]))
                hui.alapilvi.set(int(weather[5]))
                hui.keskipilvi.set(int(weather[6]))
                hui.ylapilvi.set(int(weather[7]))

                #GetWeatherObservation(observationdata,oulunsalo)       
                w_tuuli=weather[1]+(weather[2]-weather[1])*random.random()
                #w_tuuli=20
                ttime=int(float(12000)/(2*w_tuuli+0.00001))
                if ttime<150:
                        ttime=150
                if ttime>9000:
                        ttime=9000
                print "Tuuli:",w_tuuli,", ttime:", ttime
                sade=weather[4]
                if sadezero:
                        sade=0
                        print "Sade Zero"
                if sade>0:
                        if ttime>3000:
                                ttime=3000
        if demomode:
                ttime=70

        CopyList(x_1,xold_1,0,1)
        CopyList(y_1,yold_1,0,1)
        CopyList(bri_1,briold_1,0,1)

        CopyList(x_2,xold_2,0,1)
        CopyList(y_2,yold_2,0,1)
        CopyList(bri_2,briold_2,0,1)



        time_local=time.localtime()
        if dateactual:
                day=time_local.tm_yday
        if not(demomode):
                h=float(time_local.tm_hour)+(float(time_local.tm_min)+ttime/600)/60.0
        h=h-hshift
        if dynamic:
                changes1=GetHueXY_IfChanged(id_au,x_1,y_1,bri_1,xu_1,yu_1,briu_1)
                changes2=GetHueXY_IfChanged(id_sk,x_2,y_2,bri_2,xu_2,yu_2,briu_2)
        mintext=str(int((h+hshift-int(h+hshift))*60)+100)
        hui.infoteksti.set(str(int(h+hshift))+":"+mintext[1:3])
        if realweather:
                hui.infoteksti.set(place+": "+hui.infoteksti.get())

        if daymemory:
                if h+hshift < t_aa: #AAMUYO
                        hui.vuorokaudenaika.set("Yo")
                        xu_1=xyo_1
                        yu_1=yyo_1
                        briu_1=briyo_1
                        xu_2=xyo_2
                        yu_2=yyo_2
                        briu_2=briyo_2
                        #sun=False
                        au=True #False
                        sk=True
                        if h+hshift>=5:
                                au=True
                        print "Aamuyo",h+hshift
                        if notsaved:
                                if savedaymemory:
                                        print "Saving daymemory file"
                                        SaveLightMemory(daymemoryFile+"Yo.txt", id_au+id_sk,xyo_1+xyo_2,yyo_1+yyo_2,briyo_1+briyo_2)
                                        SaveLightMemory(daymemoryFile+"Pai.txt", id_au+id_sk,xpai_1+xpai_2,ypai_1+ypai_2,bripai_1+bripai_2)
                                        SaveLightMemory(daymemoryFile+"Aa.txt", id_au+id_sk,xaa_1+xaa_2,yaa_1+yaa_2,briaa_1+briaa_2)
                                        SaveLightMemory(daymemoryFile+"Il.txt", id_au+id_sk,xil_1+xil_2,yil_1+yil_2,briil_1+briil_2)
                                notsaved=False
                if (h+hshift >= t_aa)*(h+hshift < t_pai)==1: #AAMU
                        hui.vuorokaudenaika.set("Aamu")
                        xu_1=xaa_1
                        yu_1=yaa_1
                        briu_1=briaa_1
                        xu_2=xaa_2
                        yu_2=yaa_2
                        briu_2=briaa_2
                        #sun=True
                        au=True
                        sk=True
                        print "Aamu", h+hshift
                        notsaved = True
                if (h+hshift >= t_pai)*(h+hshift < t_il)==1: #PAIVA
                        hui.vuorokaudenaika.set("Paiva")
                        xu_1=xpai_1
                        yu_1=ypai_1
                        briu_1=bripai_1
                        xu_2=xpai_2
                        yu_2=ypai_2
                        briu_2=bripai_2
                        #sun=False
                        au=True
                        sk=True
                        #if h+hshift<15:
                        #        au=False
                        #       sk=False
                        print "Paiva", h+hshift
                if (h+hshift >= t_il)*(h+hshift < t_yo)==1: #ILTA
                        hui.vuorokaudenaika.set("Ilta")
                        xu_1=xil_1
                        yu_1=yil_1
                        briu_1=briil_1
                        xu_2=xil_2
                        yu_2=yil_2
                        briu_2=briil_2
                        #sun=True
                        au=True
                        sk=True
                        #if h+hshift>=21:
                        #        au=False
                        print "Ilta", h+hshift
                if h+hshift >= t_yo: #ILTAYO
                        hui.vuorokaudenaika.set("Yo")
                        xu_1=xyo_1
                        yu_1=yyo_1
                        briu_1=briyo_1
                        xu_2=xyo_2
                        yu_2=yyo_2
                        briu_2=briyo_2
                        #sun=False
                        au=True
                        sk=True
                        print "Iltayo",h+hshift
                
#perussavy pohjalle     
        CopyList(xu_1,x_1,0,1)
        CopyList(yu_1,y_1,0,1)
        CopyList(briu_1,bri_1,0,1)

        CopyList(xu_2,x_2,0,1)
        CopyList(yu_2,y_2,0,1)
        CopyList(briu_2,bri_2,0,1)

#Lisataan aurinko       
        if sun:
                sky_T=((weather[0]+40.0)/80.0*10+5) 
                sunheight=AuKorkeus(day,h,float(position[0]))

                x_au,y_au,bri_au,vis_au=AuVariXY(sunheight,sky_T)
                x_sk,y_sk,bri_sk=SkyVariXY(sunheight,sky_T)
                if hui.neonsky.get():
                        x_au=float(hui.xneonau.get())/100
                        y_au=float(hui.yneonau.get())/100
                        x_sk=float(hui.xneonsk.get())/100
                        y_sk=float(hui.yneonsk.get())/100
                        #if bri_sk<bri_au:
                        #        bri_sk=bri_au

                print day, h+hshift,sunheight #, x_au,y_au,bri_au
                hui.infoteksti.set(hui.infoteksti.get()+" AUR kulma:"+str(float(int(sunheight*10))/10))

                waur,wsky,cltn=CloudRandom(weather[5],weather[6],weather[7], True,hui.brightmode.get())
                AsetaPilvivaritUI(hui,x_au,y_au,bri_au,x_sk,y_sk,bri_sk,waur,wsky,cltn,vis_au)
                juuri.update()

                if sunheight<5:
                        iltaselk=(sunheight+3)/8
                        if iltaselk<0:
                                iltaselk=0
                        weather[5]=weather[5]*iltaselk
                        weather[6]=weather[6]*iltaselk
                        weather[7]=weather[7]*iltaselk
                        print "Yoksi selkeampaa ", int(iltaselk*100), "%"
                #nau=0       
                for i in range(len(id_au)):
                        if weathereffect:
                                w_au,w_sk,cl_type=CloudRandom(weather[5],weather[6],weather[7], False,hui.brightmode.get())
                        else:
                                cl_type="sk"
                        on_cl=True
                        alapos=sunheight-(90-abs(pos_au[i]))/6+10
                        ylapos=(90-abs(pos_au[i]))*0.8-sunheight
                        #print cl_type
                        if cl_type=="sk":
                                if (ylapos>0)&(alapos>0)&(vis_au>0):
                                        x_cl=x_au
                                        y_cl=y_au
                                        bri_cl=bri_au*vis_au
                                else:
                                        x_cl,y_cl,bri_cl,on_cl=SkyPosVariXY(90-sunheight,sky_T,pos_au[i])
                                        if (vis_au<1)&(not(hui.neonsky.get())):
                                                if random.random()>vis_au:
                                                        #x_cl,y_cl,bri_cl,on_cl=SkyPosVariXY(90-sunheight,sky_T,pos_au[i])
                                                        bri_cl=bri_cl/4
                                                #print x_cl,y_cl,bri_cl,on_cl
                                                #x_cl=x_sk
                                                #y_cl=y_sk
                                                #bri_cl=bri_au*(vis_au+1)/2
                        else:
                                wei=w_sk/(w_sk+w_au)
                                x_cl,y_cl,bri_cl,scale=WeightColorXY(x_au, y_au, bri_au, x_sk, y_sk, bri_sk,wei)

                                if hui.brightmode.get():
                                        bri_cl=bri_au
                                        if bri_au<bri_sk:
                                                bri_cl=bri_sk
                                else:
                                        bri_cl=bri_cl*(w_au+w_sk)/2*(vis_au+1)/2
                                if bri_cl>255:
                                        bri_cl=255
                        if briu_1[i]==0:
                                wei=1
                        else:
                                wei=bri_cl/briu_1[i]
                        if wei>1:
                                wei=1
                        #print "aurinko:",id_au[i],"x:",x_au,x_cl,x_sk,w_au,w_sk,cl_type #y_cl,bri_cl,wei
                        #print "aurinko:",id_au[i],x_cl,y_cl,bri_cl,cl_type,w_au,w_sk #y_cl,bri_cl,wei
                        x_1[i], y_1[i], bri_1[i],scale = WeightColorXY(xu_1[i], yu_1[i], briu_1[i],x_cl, y_cl, bri_cl,wei)
                        #print "jalkeen:", id_au[i],x_1[i], y_1[i], bri_1[i]
                        if bri_1[i]<2:
                                on_au[i]=on_cl
                        #tmp=(1-random.random()*w_tuuli/30)
                        #if tmp<.2:
                        #        tmp=.2
                        #bri_1[i]=bri_1[i]*tmp
                        #x_1[i]=x_1[i]-(1-tmp)*0.05

                for i in range(len(id_sk)):
                        if weathereffect:
                                w_au,w_sk,cl_type=CloudRandom(weather[5],weather[6],weather[7],False,hui.brightmode.get())
                        else:
                                cl_type="sk"
                        on_cl=True
                        if cl_type=="sk":
                                if not(hui.neonsky.get()):
                                        x_cl,y_cl,bri_cl,on_cl=SkyPosVariXY(90-sunheight,sky_T,pos_sk[i])
                                #print "P",x_cl,y_cl,bri_cl, on_cl
                                else:
                                        x_cl=x_sk
                                        y_cl=y_sk
                                        bri_cl=bri_sk
                                        if bri_au>bri_sk:
                                                bri_cl=bri_au
                                #if sunheight<2:
                                #        if random.random()>(abs(sunheight)/2.0*0.6+0.4):
                                #                x_cl=x_au
                                #                y_cl=y_au
                                #                bri_cl=bri_au*vis_au #+bri_sk)/2.0
                        else:
                                wei=w_sk/(w_sk+w_au)
                                x_cl,y_cl,bri_cl,scale=WeightColorXY(x_au, y_au, bri_au, x_sk, y_sk, bri_sk,wei)
                                if hui.brightmode.get():
                                        bri_cl=bri_au
                                        if bri_au<bri_sk:
                                                bri_cl=bri_sk
                                else:
                                        bri_cl=bri_cl*(w_au+w_sk)/2
                                if bri_cl>255:
                                        bri_cl=255
                        if briu_2[i]==0:
                                wei=1
                        else:
                                wei=bri_cl/briu_2[i]
                        if wei>1:
                                wei=1
                        x_2[i], y_2[i], bri_2[i],scale = WeightColorXY( xu_2[i], yu_2[i], briu_2[i],x_cl, y_cl, bri_cl,wei)
                        if bri_2[i]<2:
                                on_sk[i]=on_cl

 
        if sun:
                if sunheight<-7:
                        if sum(bri_1)<len(bri_1)*2:
                                #au=False
                                on_au=[False]*len(id_au)
                                if not(demomode):
                                        ttime=9000
                                print "Iltayo, au off, ttime:", ttime
                if sunheight<-14:
                        if sum(bri_2)<len(bri_2)*2:
                                #sk=False
                                on_sk=[False]*len(id_sk)
                                if not(demomode):
                                        ttime=9000
                                print "Keskiyo, sk off, ttime:", ttime

        #print x_2
        #print xu_2
        if hui.pilvistylaskuri.get()<100:
                a=hui.pilvistylaskuri.get()+ttime/90
                if a>100:
                        a=100
                hui.ylapilvi.set(a)
                hui.keskipilvi.set(a)
                hui.alapilvi.set(a)
                hui.pilvistylaskuri.set(a)
                hui.infoteksti.set(hui.infoteksti.get()+" Pilvistyy")



######### LYHDYT ####################

        if h+hshift>14:
                if h+hshift<15:
                        lyhtyautomatiikka = True
        if h+hshift>2:
                if h+hshift<3:
                        lyhtyautomatiikka = True

        if lyhtyautomatiikka:
                if sum(bri_1)/len(bri_1)<100:
                        lyhty = True
                else:
                        lyhty = False

                if h+hshift < 12:
                        lyhty = False


        if lyhty:
                ttime = 250
                ioff=int(24-(h+hshift))
                if ioff>19:
                        ioff=0
                if ioff>6:
                        ioff=6
                if ioff<0:
                        ioff=0
                for j in range(len(id_ly)):
                        for i in range(len(id_au)):
                                if id_ly[j]==id_au[i]:
                                        on_au[i]=True
                                        i_r=int(random.random()*5)+ioff
                                        x_1[i], y_1[i], bri_1[i],scale = SumColorXY( x_1[i], y_1[i], bri_1[i],lyhty_x[i_r], lyhty_y[i_r], lyhty_bri[i_r])
                                        #x_1[i], y_1[i], bri_1[i],scale = WeightColorXY( x_1[i], y_1[i], bri_1[i],lyhty_x[i_r], lyhty_y[i_r], lyhty_bri[i_r],0.75)
                                        #x_1[i], y_1[i], bri_1[i],scale = WeightColorXY( x_1[i], y_1[i], bri_1[i],0.53, 0.41, 240,0.75)
                        for i in range(len(id_sk)):
                                if id_ly[j]==id_sk[i]:
                                        on_sk[i]=True
                                        i_r=int(random.random()*5)+ioff
                                        x_2[i], y_2[i], bri_2[i],scale = SumColorXY( x_2[i], y_2[i], bri_2[i],lyhty_x[i_r], lyhty_y[i_r], lyhty_bri[i_r])
                                        #x_2[i], y_2[i], bri_2[i],scale = WeightColorXY( x_2[i], y_2[i], bri_2[i],lyhty_x[i_r], lyhty_y[i_r], lyhty_bri[i_r],0.75)
                                        #x_2[i], y_2[i], bri_2[i],scale = WeightColorXY( x_2[i], y_2[i], bri_2[i],0.53, 0.41, 240,0.75)
                if lyhtyautomatiikka:
                        print "Lyhdyt AUTO"
                else:
                        print "Lyhdyt"

        ##############Ainon ja Juhon iltaruskot ja aamuruskot##################

        wkday=time.strftime("%A")
        if (wkday=="Saturday")|(wkday=="Sunday"):
                ain=ai_nukkuu_viikonloppu
                aih=ai_heraa_viikonloppu
                jun=ju_nukkuu_viikonloppu
                juh=ju_heraa_viikonloppu
        else:
                ain=ai_nukkuu
                aih=ai_heraa
                jun=ju_nukkuu
                juh=ju_heraa
        ###########AINO
        if h+hshift+ai_ruskokesto > ain:
                aika_ai= (ain-(h+hshift))/ai_ruskokesto
                sunh_ai=sunheight*aika_ai + (-0.6)*(1-aika_ai)
                x_tmp,y_tmp,bri_tmp,vis_au=AuVariXY(sunh_ai,sky_T)
                bri_ai=[bri_tmp*vis_au]
                x_ai=[x_tmp]
                y_ai=[y_tmp]
                if h+hshift < ain:
                        SetHue(id_ai,bri_ai, x_ai, y_ai, ttime)
                        print "Ainon iltarusko",int(aika_ai*100), "%"
                        hui.infoteksti.set(hui.infoteksti.get()+" Ainon iltarusko")
                else:
                       SetHueUnLit(id_ai,bri_ai, x_ai, y_ai, ttime)
                       print "Aino nukkuu"
                       hui.infoteksti.set(hui.infoteksti.get()+" Aino nukkuu")
        if h+hshift < aih+ai_ruskokesto:
                aika_ai= (aih+ai_ruskokesto - (h+hshift))/ai_ruskokesto
                if not(hui.ainooff.get()):
                        sunh_ai=sunheight*(1-aika_ai) + (-0.6)*aika_ai
                else:
                        sunh_ai=5*(1-aika_ai) + (-0.6)*aika_ai                        
                x_tmp,y_tmp,bri_tmp,vis_au=AuVariXY(sunh_ai,sky_T)
                bri_ai=[bri_tmp*vis_au]
                x_ai=[x_tmp]
                y_ai=[y_tmp]
                if h+hshift > aih:
                        SetHue(id_ai,bri_ai, x_ai, y_ai, ttime)
                        print "Ainon aamurusko", int(aika_ai*100), "%"
                        hui.infoteksti.set(hui.infoteksti.get()+" Ainon aamurusko")
                else:
                       SetHueUnLit(id_ai,bri_ai, x_ai, y_ai, ttime)
                       print "Aino nukkuu"
                       hui.infoteksti.set(hui.infoteksti.get()+" Aino nukkuu")
#        else:
#                if h+hshift+ai_ruskokesto < ain:
#                        bri_ai=[bri_1[1]]
#                        x_ai=[x_1[1]]
#                        y_ai=[y_1[1]]
#                        SetHue(id_ai,bri_ai, x_ai, y_ai, ttime)
        ###########JUHO
        if h+hshift+ju_ruskokesto > jun:
                aika_ju= (jun-(h+hshift))/ju_ruskokesto
                sunh_ju=sunheight*aika_ju + (-0.6)*(1-aika_ju)
                x_tmp,y_tmp,bri_tmp,vis_au=AuVariXY(sunh_ju,sky_T)
                bri_ju=[bri_tmp*vis_au]
                x_ju=[x_tmp]
                y_ju=[y_tmp]
                if h+hshift < jun:
                        SetHue(id_ju,bri_ju, x_ju, y_ju, ttime)
                        print "Juhon iltarusko", int(aika_ju*100), "%"
                        hui.infoteksti.set(hui.infoteksti.get()+" Juhon iltarusko")
                else:
                       SetHueUnLit(id_ju,bri_ju, x_ju, y_ju, ttime)
                       print "Juho nukkuu"
                       hui.infoteksti.set(hui.infoteksti.get()+" Juho nukkuu")
        if h+hshift < juh+ju_ruskokesto:
                aika_ju= (juh+ju_ruskokesto - (h+hshift))/ju_ruskokesto
                if not(hui.juhooff.get()):
                        sunh_ju=sunheight*(1-aika_ju) + (-0.6)*aika_ju
                else:
                        sunh_ju=5*(1-aika_ju) + (-0.6)*aika_ju
                x_tmp,y_tmp,bri_tmp,vis_au=AuVariXY(sunh_ju,sky_T)
                bri_ju=[bri_tmp*vis_au]
                x_ju=[x_tmp]
                y_ju=[y_tmp]
                if h+hshift > juh:
                        SetHue(id_ju,bri_ju, x_ju, y_ju, ttime)
                        print "Juhon aamurusko", int(aika_ju*100), "%"
                        hui.infoteksti.set(hui.infoteksti.get()+" Juhon aamurusko")
                else:
                       SetHueUnLit(id_ju,bri_ju, x_ju, y_ju, ttime)
                       print "Juho nukkuu"
                       hui.infoteksti.set(hui.infoteksti.get()+" Juho nukkuu")
 #       else:
 #               if h+hshift+ju_ruskokesto < jun:
 #                       bri_ju=[bri_1[0]]
 #                       x_ju=[x_1[0]]
 #                       y_ju=[y_1[0]]
 #                       SetHue(id_ju,bri_ju, x_ju, y_ju, ttime)

        
        if nimikaskytys:
                if valotpois:
                        au=False
                        sk=False

        a=not(weathereffect)
        b=(sade==0)
        #au=False #############################################
        if a|b:
                if au:
                        bri_ju=[0]
                        x_ju=[0]
                        y_ju=[0]
                        for i in range(len(id_au)):
                                xold_1[i],yold_1[i],briold_1[i],scale=WeightColorXY(x_1[i], y_1[i], bri_1[i],xold_1[i], yold_1[i], briold_1[i], 0.5)
                                bri_ju=[bri_ju[0]+briold_1[i]+1]
                                x_ju=[x_ju[0]+xold_1[i]*float(briold_1[i]+1)]
                                y_ju=[y_ju[0]+yold_1[i]*float(briold_1[i]+1)]
                        x_ju=[x_ju[0]/float(bri_ju[0])]
                        y_ju=[y_ju[0]/float(bri_ju[0])]
                        bri_ju=[bri_ju[0]/float(len(id_au))-1]
                        
                        SetHueOn(id_au,briold_1, xold_1, yold_1, int(ttime/2),on_au)
                        if not(hui.juhooff.get()):
                                if (h+hshift > juh+ju_ruskokesto)&(h+hshift+ju_ruskokesto < jun):
                                        SetHue(id_ju,bri_ju, x_ju, y_ju, int(ttime/2))
                        if not(hui.ainooff.get()):
                                if (h+hshift > aih+ai_ruskokesto)&(h+hshift+ai_ruskokesto < jun):
                                        SetHue(id_ai,bri_ju, x_ju, y_ju, int(ttime/2))
                                
                else:
                        SetHueUnLit(id_au,bri_1, x_1, y_1, int(ttime/2))
                if sk:          
                        for i in range(len(id_sk)):
                                xold_2[i],yold_2[i],briold_2[i],scale=WeightColorXY(x_2[i], y_2[i], bri_2[i],xold_2[i], yold_2[i], briold_2[i], 0.5)        
                        SetHueOn(id_sk,briold_2, xold_2, yold_2, int(ttime/2),on_sk)
                else:
                        SetHueUnLit(id_sk,bri_2, x_2, y_2, int(ttime/2))
                tm=time.clock()
                while (time.clock()-tm)*20<ttime:
                        #time.sleep(2)
                        juuri.update()
                        if hui.breakloop.get():
                                ttime=2
                                break
                                
                        #tm=tm+20
                if au:
                        bri_ju=[0]
                        x_ju=[0]
                        y_ju=[0]
                        SetHueOn(id_au,bri_1, x_1, y_1, int(ttime/2),on_au)
                        for i in range(len(id_au)):        
                                bri_ju=[bri_ju[0]+bri_1[i]+1]
                                x_ju=[x_ju[0]+x_1[i]*float(bri_1[i]+1)]
                                y_ju=[y_ju[0]+y_1[i]*float(bri_1[i]+1)]
                        x_ju=[x_ju[0]/float(bri_ju[0])]
                        y_ju=[y_ju[0]/float(bri_ju[0])]
                        bri_ju=[bri_ju[0]/float(len(id_au))-1]
                        if not(hui.juhooff.get()):
                                if (h+hshift > juh+ju_ruskokesto)&(h+hshift+ju_ruskokesto < jun):
                                        SetHue(id_ju,bri_ju, x_ju, y_ju, int(ttime/2))
                        if not(hui.ainooff.get()):
                                if (h+hshift > aih+ai_ruskokesto)&(h+hshift+ai_ruskokesto < jun):
                                        SetHue(id_ai,bri_ju, x_ju, y_ju, int(ttime/2))
                if sk:          
                        SetHueOn(id_sk,bri_2, x_2, y_2, int(ttime/2),on_sk)
                tm=time.clock()
                while (time.clock()-tm)*20<ttime:
                        #time.sleep(2)
                        juuri.update()
                        if hui.breakloop.get():
                                break
                        #tm=tm+20
              
        else:
                tm=0.0
                wtm=6
                ttm=2

                #sade=0.6
                
                sade_impakti=sade/2
                if sade_impakti>.1:
                        sade_impakti=.1
                sade_frekvenssi=sade*2
                if sade_frekvenssi>.8:
                        sade_frekvenssi=.8
                print sade
                ttm=int(3-sade*5)+1
                #if ttm<1:
                #        ttm=1
                print sade, sade_impakti, sade_frekvenssi, ttm
                if au:
                        if sk:
                                ids=id_au+id_sk
                                bris=bri_1+bri_2
                                xs=x_1+x_2
                                ys=y_1+y_2
                                xso=xold_1+xold_2
                                yso=yold_1+yold_2
                                briso=briold_1+briold_2
                        else:
                                ids=id_au
                                bris=bri_1
                                xs=x_1
                                ys=y_1
                                xso=xold_1
                                yso=yold_1
                                briso=briold_1
                else:
                        if sk:
                                ids=id_sk
                                bris=bri_2
                                xs=x_2
                                ys=y_2
                                xso=xold_2
                                yso=yold_2
                                briso=briold_2
                                
                                               
                while (tm<ttime)&(au|sk):
                        for i in range(len(ids)):
                                #print float(tm)/float(ttime)
                                xtmp,ytmp, britmp,scale=WeightColorXY(xso[i], yso[i], briso[i],xs[i], ys[i], bris[i], float(tm)/float(ttime))
                                id_tmp=[ids[i]]
                                bri_tmp=[((1.0-sade_impakti)-sade_impakti*random.random())*britmp]
                                x_tmp=[xtmp-random.random()*sade/10]
                                y_tmp=[ytmp]
                                if random.random()<sade_frekvenssi:
                                        SetHue(id_tmp,bri_tmp, x_tmp, y_tmp, 1)
                                        bri_tmp=[britmp]
                                        time.sleep(float(1)/10)
                                        x_tmp=[xtmp]
                                        tm=tm+1
                                        SetHue(id_tmp,bri_tmp, x_tmp, y_tmp, wtm)
                                time.sleep(0.1)
                                tm=tm+1
                        juuri.update()
                        time.sleep(float(ttm+1)/10)
                        tm=tm+ttm+1
                #if not(demomode):
                #        time.sleep(20)
                        
               
        if demomode:
                h=h+.25+hshift  ####
                if h>24:
                        h=0

juuri.destroy()
