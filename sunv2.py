import numpy as np
import time
fPi=355.0/113.0

############## Aurinkofunktiot

def AuKorkeus(vuodenpaiva,kellonaika,leveyspiiri):
        fLeveyspiiri=float(leveyspiiri)
        fAkselinkallistus=23.43
        fAkselinkallistus_Nyt=np.cos(float(vuodenpaiva+10)/365*2*fPi)*fAkselinkallistus
        fSunHeigth=-np.cos(float(kellonaika)/24*fPi*2)*(90-fLeveyspiiri)-fAkselinkallistus_Nyt
        return(fSunHeigth)

def AuNousuLasku(vuodenpaiva,leveyspiiri):
        fLeveyspiiri=float(leveyspiiri)
        fAkselinkallistus=23.43
        fAkselinkallistus_Nyt=np.cos(float(vuodenpaiva+10)/365*2*fPi)*fAkselinkallistus

        MaxHeigth=90-(fLeveyspiiri+fAkselinkallistus_Nyt)
        MinHeigth=(fLeveyspiiri-fAkselinkallistus_Nyt)-90
        #print MaxHeigth, MinHeigth

        ValoisaAika=float(0)
        if MaxHeigth > 0:
                if MinHeigth < 0:
                        fAlpha_apu=np.arcsin(np.tan(fLeveyspiiri/180*fPi)*np.tan(fAkselinkallistus_Nyt/180*fPi))*180/fPi
                        ValoisaAika=(90-fAlpha_apu+1)/180*24
                        return(12-ValoisaAika/2,12+ValoisaAika/2)
        if MaxHeigth < 0:
            ValoisaAika =0
            return(-1,-1)
        if MinHeigth > 0:
            ValoisaAika =24
            return(-2,-2)
        
def AuNousuLaskuTarkka(vuodenpaiva=111,leveyspiiri=65,pituuspiiri=25.46820, nyt=False): #Oulun koordinaatit
    if nyt:
        t=time.localtime()
        vuodenpaiva=t.tm_yday
    
    Nh,Lh = AuNousuLasku(vuodenpaiva,leveyspiiri)

    pkmin = AuPituuspiiriKorjaus(pituuspiiri)
    ellmin = AuEoTKorjaus(vuodenpaiva)
    korjh= (pkmin-ellmin)/60
    
    #nousu
    n=np.arange(Nh-0.5,Nh+0.5,1.0/120)
    AKR=[]
    for N in n:
        AK=AuKorkeus(vuodenpaiva,N,leveyspiiri)
        AKR.append(AuKorkeusRefraktio(AK,P=950,T=0))
    zero_crossings = np.where(np.diff(np.sign(AKR)))[0]
    if list(zero_crossings) == []:
        Nth=None
    else:
        Nth=float(n[zero_crossings+1])+korjh
    
    #lasku
    n=np.arange(Lh-0.5,Lh+0.5,1.0/120)
    AKR=[]
    for N in n:
        AK=AuKorkeus(vuodenpaiva,N,leveyspiiri)
        AKR.append(AuKorkeusRefraktio(AK,P=950,T=0))
    zero_crossings = np.where(np.diff(np.sign(AKR)))[0]
    if list(zero_crossings) == []:
        Lth=None
    else:
        Lth=float(n[zero_crossings])+korjh

    return Nth,Lth    
       
def AuKorkeusRefraktio(fSunHeigth,P=950,T=0):        
        sh=fSunHeigth
        fSunHeigth=sh+P/(273+T)*(0.1594+0.0196*sh+0.00002*sh*sh)/(1+0.505*sh+0.0845*sh*sh) #Ilmakeh�n refraktio
        return fSunHeigth

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
        #print("Pituuspiirikorjaus: "+str(int(mn))+" min")
        return(int(mn))

def AuEoTKorjaus(vuodenpaiva):
        M=6.24+0.01720197*vuodenpaiva #Suurinpiirtein
        EoTkorjaus=-7.659*np.sin(M)+9.863*np.sin(2*M+3.5932) #Equation of time - maan radan ellipsisyys
        #print("Ajantasaus: "+str(int(EoTkorjaus)))
        return (int(EoTkorjaus))
        

def T_TropoH(fTropoHeigth):
    T= 50*(-1 +np.sqrt(1-4*(1-fTropoHeigth/10)))
    return T
def TropoH_T(T):
    Th=T/10+T*T/1000+10
    return Th

def Airmass(fSunHeigth,fTropoHeigth):
    if fSunHeigth>0:
        fSkythick = fTropoHeigth/(np.cos(fPi/2-fSunHeigth/180*fPi)+0.50572*pow(6.07995+fSunHeigth,-1.6364)) #airmass, karsten & young (1989)
    else:
        fSkythick = fTropoHeigth/(np.cos(fPi/2)+0.50572*pow(6.07995,-1.6364))
    return fSkythick


def AuVariBGR(fSunHeigth,fTropoHeigth=10,altitude=0):  
        P=950
        T = T_TropoH(fTropoHeigth)

        varjosiirt=0.0
        if altitude>0:
            earth_r=6371
            varjosiirt = np.arccos(earth_r/(earth_r+altitude))/np.pi*180
            fSunHeigth +=varjosiirt
 
        fSunHeigth = AuKorkeusRefraktio(fSunHeigth,T=T)


        fRvaim= float(1)/1.1 #per 200 km
        fGvaim= float(1)/2 #per 90 km
        fBvaim = float (1)/2 #per 10 km

        fRvaim_l=float(230)#(87)
        fGvaim_l=float(77)#(77)#(153)
        fBvaim_l=float(20)#(19)

        fSkythick = Airmass(fSunHeigth,fTropoHeigth)

        fR=255*pow(fRvaim,fSkythick/fRvaim_l)
        fG=255*pow(fGvaim,fSkythick/fGvaim_l)
        fB=255*pow(fBvaim,fSkythick/fBvaim_l)

        fM= max((fR,fG,fB))
        if fM>255:
            fR=fR/fM*255
            fG=fG/fM*255
            fB=fB/fM*255
 
        visible=1.0
        varjo=1
        if fSunHeigth<0.25:
                visible=(fSunHeigth+0.25)/0.5
        if fSunHeigth<-.25:
                visible=0
        if fSunHeigth<0:
                varjo= (fSunHeigth+1.0)/1.0
        if fSunHeigth<-1:
                varjo=0
        if altitude==-1:varjo=1
        return (int(fB*varjo),int(fG*varjo),int(fR*varjo))

def SkyVariBGR(fSunHeigth,suncolor): 
    fBs, fGs, fRs = suncolor
    fB=255-fBs
    fG=255-fGs
    fR=255-fRs

    if fR>0 or fG>0 or fB>0:
        fS=max((fRs,fGs,fBs))
        fC=max((fR,fG,fB))
        fR=fR*fS/fC
        fG=fG*fS/fC
        fB=fB*fS/fC
    else:
        fR=0
        fG=0
        fB=0

    varjo=1
    if fSunHeigth<0:
        varjo=(fSunHeigth+10.0)/10.0
    if fSunHeigth<-10:
        varjo=0
    return (int(fB*varjo),int(fG*varjo),int(fR*varjo))
    

def SkyPosVariBGR(skypos, fSunHeigth,suncolor, fTropoHeigth=10, auer=0.01): 
        fBs, fGs, fRs = suncolor
        fSunHeigth=90-fSunHeigth

        #fTropoHeigth=fTropoHeigth*0.5
        fSunHeigth=float(fSunHeigth)
        skypos=float(skypos)
        
        etaau=1/pow(abs(fSunHeigth-skypos)+1,.25)

        et=np.sin(skypos*fPi/180)
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
        
        skypos=90-abs(skypos)
        T = T_TropoH(fTropoHeigth)
        skypos = AuKorkeusRefraktio(skypos,T=T)
        fSkythick = Airmass(skypos,fTropoHeigth)


        #st=(st+fSkythick)/fTropoHeigth/2
        
        fR=(255-fRs) * fRs/255 + (fSkythick*fRs)/70.0 * etaau * varjokerroin + auer*fRs
        fG=(255-fGs) * fRs/255 + (fSkythick*fGs)/70.0 * etaau * varjokerroin + auer*fGs
        fB=(255-fBs) * fRs/255 + (fSkythick*fBs)/70.0 * etaau * varjokerroin + auer*fGs


        if fR>0 or fG>0 or fB>0:
            fS=max((fRs,fGs,fBs))
            fC=max((fR,fG,fB))
            fR=fR*fS/fC
            fG=fG*fS/fC
            fB=fB*fS/fC
        else:
            fR=0
            fG=0
            fB=0
        
        return (int(fB*(varjokerroin+0.15*(1-varjokerroin))),int(fG*(varjokerroin + 0.05*(1-varjokerroin))),int(fR*varjokerroin*varjokerroin))
  

def CloudRandom(ap,kp,yp, returnweights=True, brightmode=False):
        ap=float(ap)/100
        kp=float(kp)/100
        yp=float(yp)/100
        w_au=1
        w_sk=1



        #if brightmode:
        #        h=1.0
        #        l=0.95

        tn_sk=(1-ap)*(1-kp)*(1-yp)

        #ylapilvet
        l=0.80
        h=0.95

        #keskipilvet
        l=0.60
        h=0.95

        wau_ypah=h
        wau_ypal=wau_ypah*l
        wsk_ypah=h
        wsk_ypal=wsk_ypah*l
        tn_ypah=yp*(1-yp)
        tn_ypal=yp*yp
        tnx_yp=(1-kp)*(1-ap)

        #alapilvet
        l=0.50
        h=0.95

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
                print( "Taivas/aurinko")
                print( "sk", tn_sk, w_sk, w_au)
                print( "Ylapilvet")
                print( "ypah", tn_ypah*tnx_yp, wsk_ypah, wau_ypah)
                print( "ypal", tn_ypal*tnx_yp, wsk_ypal, wau_ypal)
                print( "Keskipilvet")
                print( "kpVh", tn_kpVh*tnx_kp, wsk_kpVh, wau_kpVh)
                print( "kpVl", tn_kpVl*tnx_kp, wsk_kpVl, wau_kpVl)
                print( "kpah", tn_kpah*tnx_kp, wsk_kpah, wau_kpah)
                print( "kpal", tn_kpal*tnx_kp, wsk_kpal, wau_kpal)
                print( "Alapilvet" )               
                print( "apVh", tn_apVh*tnx_ap, wsk_apVh, wau_apVh)
                print( "apVl", tn_apVl*tnx_ap, wsk_apVl, wau_apVl)
                print( "apah", tn_apah*tnx_ap, wsk_apah, wau_apah)
                print( "apal", tn_apal*tnx_ap, wsk_apal, wau_apal)
                tntot=tn_sk+tn_ypah*tnx_yp+tn_ypal*tnx_yp
                tntot=tntot+ tn_kpVh*tnx_kp +tn_kpVl*tnx_kp +tn_kpal*tnx_kp +tn_kpah*tnx_kp
                tntot=tntot+tn_apVh+tn_apVl+tn_apal+tn_apah
                print( "Yhteensa", tntot )              
        if returnweights:
                weights_sk=[0, w_sk, wsk_ypah, wsk_ypal, wsk_kpVh,wsk_kpVl, wsk_kpah, wsk_kpal, wsk_apVh, wsk_apVl, wsk_apah, wsk_apal]
                weights_au=[w_au, 0, wau_ypah, wau_ypal, wau_kpVh,wau_kpVl, wau_kpah, wau_kpal, wau_apVh, wau_apVl, wau_apah, wau_apal]
                tn_pil =[tn_sk,tn_sk, tn_ypah*tnx_yp, tn_ypal*tnx_yp, tn_kpVh*tnx_kp, tn_kpVl*tnx_kp, tn_kpah*tnx_kp, tn_kpal*tnx_kp]
                tn_pil=tn_pil +[tn_apVh*tnx_ap, tn_apVl*tnx_ap, tn_apah*tnx_ap, tn_apal*tnx_ap]

                return(weights_sk, weights_au, tn_pil)
               
               
        #randomise cloud level
        pilvi= np.random.random()
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

        print( "Vikaa pilviarvonnassa?", tn, pilvi)
        return(w_au,w_sk,"sk")





#Varifunkitoita

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
                print( "HUOM!Bri > 255")
        if BRI<0:
                print( "HUOM!Bri < 0")
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
                print( "Bri <0")
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
