import cv2
import numpy as np
from random import shuffle
import time
import threading

def Vlen(V):
    vlen=V[0]*V[0]+V[1]*V[1]
    return np.sqrt(vlen)

def Vlen2(V):
    vlen=V[0]*V[0]+V[1]*V[1]
    return vlen

def Vangle(v):
    return np.angle(v[0]+v[1]*1j,deg = True)


def Normalize(vect):
    x=vect[0]
    y=vect[1]
    if (y==0) and (x==0):
        v=np.array([0,0])
    else:
        r=np.sqrt(x*x+y*y)
        v=np.array([x/r, y/r])
    return v

def Orthonormal(vi):
    v=Normalize(vi)
    V=v[0]+v[1]*1j
    Vo=np.exp(np.pi*0.5j)*V
    return np.array([np.real(Vo), np.imag(Vo)])

def potential(dx,dy, mode="normal", scale=1.0):
    #dx=dX[0]
    #dy=dX[1]
    r2 = dx*dx + dy*dy
    r=np.sqrt(r2)
    dX=Normalize(np.array([dx,dy]))
    if mode=="rep":
        p= -20.0/(1+r2)
    if mode=="normal":
        p= (r2/128.0-10.0)/(1.0+r2/400.0)/(r+.001)

    if mode=="grouprep":
        p= -100.0/(1+r2)
    if mode=="grouppull":
        p= (r2/128.0-10.0)/(1.0+r2/400.0)/(r+.001)
        p*=10
        if p<0: p=0
    return -p*np.array([dx,dy])*scale

def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

def PotentialSize(dX, size=10, repulsion = True,scale=1.0):
    ro = Vlen(dX)
    dx=Normalize(dX)

    towards=1.0
    if repulsion: towards = 0.0

    #nearfield
    rnf=size
    rmin=10.0
    rnf=max(rmin,rnf)
    rnsc=5.0/rnf
    pnf = -rnf/8.0

    #midfield
    rmf=(ro/rnf-0.3)
    pmf = -1.0/(.1+(rmf*rmf))+7*towards

    #farfield
    rff=7.0*rnf
    rfsc=20.0/rff
    pff = 0.5+6.5*towards

    #transition: near-fied - mid-field
    r=(ro-rnf)*rnsc
    sgm_nf=sigmoid(r)
    pnmf= (1.0-sgm_nf)*pnf + sgm_nf*pmf

    #transition: ... - far-field
    r=(ro-rff)*rfsc
    sgm_ff=sigmoid(r)
    p=(1-sgm_ff)*pnmf + sgm_ff*pff
     
    return p*dx*scale


class node():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.cargo = {}
        self.color = (0,0,0)
        self.tontinrajat=[]
        self.BB =np.array([0,0,0,0])
        self.image = None
        self.pot=np.array([0.0,0.0])
        self.highlighted = False
        self.maximized=False
        self.label = ""
        self.size =20
        self.fixed = False

    def BoundingBoxSet(self):
        BB=np.array([999999999,-999999999,999999999,-999999999])
        if self.tontinrajat == []:
            BB[0]=self.x-self.size
            BB[1]=self.x+self.size
            BB[2]=self.y-self.size
            BB[3]=self.y+self.size
            self.BB = BB
            return self.BB

        for P in self.tontinrajat:
            if BB[0] > P[0]: BB[0] = P[0]
            if BB[1] < P[0]: BB[1] = P[0]
            if BB[2] > P[1]: BB[2] = P[1]
            if BB[3] < P[1]: BB[3] = P[1]
        self.BB=BB
        return self.BB

    def BBinImage(self,scale=1,cent=np.array([0,0])):
        BBi = self.BoundingBoxSet()
        BBi[0] = int((BBi[0]-cent[0])*scale)
        BBi[1] = int((BBi[1]-cent[0])*scale)
        BBi[2] = int((BBi[2]-cent[1])*scale)
        BBi[3] = int((BBi[3]-cent[1])*scale)
        return BBi

    def update(self):
        self.runCargoFun(self.cargo["Function"], self.cargo["Args"])
        pass
    
    def runCargoFun(self,CargoFun,args):
        if CargoFun is not None:
            self.cargo["Args"]= CargoFun((args), node = self)

    def drawNode(self,im, r=5, scale=1, cent=np.array([0,0]),label=False, logo=True):
        x= int((self.x-cent[0])*scale)
        y= int((self.y-cent[1])*scale)

        cv2.circle(im, (x,y),r,self.color,1)
        
        
        if logo and (self.image is not None) and not self.maximized:        
            size=(8*int(r),8*int(r))
            f = np.zeros((size[1],size[0],4), np.uint8)
            f4 = np.zeros((size[1],size[0]), np.uint8)
            sz=size
            scx=size[0]/(len(self.image[0]))
            scy=size[1]/(len(self.image))
            sca=max(scx,scy)
            sz=(int(sca*len(self.image[0]))+1,int(sca*len(self.image))+1)
            addedim=cv2.resize(self.image, sz)
            addedimage=addedim[:size[1],:size[0],:]
            f[:,:,:3] =addedimage
            #f4=self.DrawRajat(f4, scale=sc, cent = ci, mask=True)
            ci=int(size[0]/2)
            cv2.circle(f4, (ci,ci),ci,255,-1)
            f[:,:,3]=f4
            l=size[1]
            w=size[0]
            
            if x+ci>len(im[0]): X0=len(im[0])-w-1
            elif x-ci<0: X0=0
            else: X0=x-ci

            if y+ci>len(im): X1=len(im)-l-1
            elif y-ci<0: X1=0
            else: X1=y-ci

            #print(X0,X1,l,w)
            crop = im[X1:X1+l,X0:X0+w].copy()
            #if not fullpict:
            im[X1:X1+l,X0:X0+w] = blend_transparent(crop, f)
            #else:
            #    img[X1:X1+l,X0:X0+w] = addedimage
            #    cv2.rectangle(img, (X0,X1),(X0+w,X1+l),self.color,2)
        if self.maximized and (self.image is not None):
            size=(int(len(im[0])/2),int(len(im)/2))
            scy=size[0]/(len(self.image[0]))
            scx=size[1]/(len(self.image))
            sca=min(scx,scy)
            sz=(int(sca*len(self.image[0])),int(sca*len(self.image)))
            addedim=cv2.resize(self.image, sz)
            X1=y 
            X0=x
            if X0+len(addedim[0]) > len(im[0]): X0-=len(addedim[0])
            if X1+ len(addedim) > len(im): X1-=len(addedim)
            l=len(addedim)
            w=len(addedim[0])
            im[X1:X1+l,X0:X0+w] = addedim
            cv2.rectangle(im,(X0,X1),(X0+w,X1+l),(230,200,200),2)
            x0 = (x-5, y-5)
            x1 = (x+5, y+5)
            cv2.rectangle(im,x0,x1,(130,100,100),-1)
            cv2.rectangle(im,x0,x1,(230,200,200),2)


        if label:
            BBi=self.BBinImage(scale=scale,cent=cent)
            ts=cv2.getTextSize(self.label,cv2.FONT_HERSHEY_PLAIN,1.2,3)
            x=int((BBi[0]+BBi[1]-ts[0][0])/2)
            y=int((BBi[2]+BBi[3]+3*ts[0][1])/2)
            if x+ts[0][0]>len(im[0]):
                x=len(im[0])-ts[0][0]
            if x<0:
                x=0
            cv2.putText(im,self.label,(x,y),cv2.FONT_HERSHEY_PLAIN,1.2,(255,255,255),3)
            cv2.putText(im,self.label,(x,y),cv2.FONT_HERSHEY_PLAIN,1.2,(0,0,0),2)

    
    def CenterLine(self,other):
        n1= self
        n2= other
        X1= np.array([n1.x,n1.y])
        X2= np.array([n2.x,n2.y])

        eX = (X1+X2)/2
        eV = Orthonormal(X1-X2)
        return eX, eV

    def drawCenterLine(self, other, im,scale=1,ln=10,cent=np.array([0,0])):
        n1= self
        n2= other
        colorconn=(int(n1.color[0]/2+n2.color[0]/2),\
            int(n1.color[1]/2+n2.color[1]/2),\
            int(n1.color[2]/2+n2.color[2]/2))
        
        eX,eV =self.CenterLine(other)

        Cstart= eX-ln/2*eV
        Cend  = eX+ln/2*eV
        
        x1= int((Cstart[0]-cent[0])*scale)
        y1= int((Cstart[1]-cent[1])*scale)
        x2= int((Cend[0]-cent[0])*scale)
        y2= int((Cend[1]-cent[1])*scale)

        cv2.line(im,(x1,y1),(x2,y2),colorconn,1)
    
    def arrangerajat(self): 
        i=0
        tr=[]
        for t in self.tontinrajat[:-1]:
            i+=1
            dupl = False
            for tt in self.tontinrajat[i:]:
                if (t[0]-.001<tt[0]<t[0]+.001) and (t[1]-.001<tt[1]<t[1]+.001):
                   dupl=True
            if not dupl:
                tr.append(t)
        tr.append(self.tontinrajat[-1])
        
        ta=[]
        ttr=[]
        for t in tr:
            ta.append(Vangle(t-np.array([self.x,self.y])))
        tind=list(np.arange(len(tr)))   
        tind=[x for _,x in sorted(zip(ta,tind))]
        for i in tind:
            ttr.append(tr[i])
        self.tontinrajat = ttr

    
    def DrawRajat(self,im, r=5, scale=1, cent=np.array([0,0]), mask=False,borders=False):
        tr=[]
        for t in self.tontinrajat:
            tr.append((t-cent)*scale)
        if mask:
            cv2.fillPoly(im, np.int32([tr]),255,cv2.LINE_AA)
        elif borders:
            cv2.polylines(im, np.int32([tr]),True,self.color,2,cv2.LINE_AA)
        else:
            cv2.fillPoly(im, np.int32([tr]),self.color,cv2.LINE_AA)
            cv2.polylines(im, np.int32([tr]),True,(0,0,0),2,cv2.LINE_AA)
            self.drawNode(im, r=r, scale=scale, cent=cent)
        return im

    def liitaKuva(self,img, sc=1,c=np.array([0,0]), fullpict=False, aspectlock=True):
        
        BBi=self.BBinImage(scale=sc,cent=c)
        size=(BBi[1]-BBi[0],BBi[3]-BBi[2])
        
        BBn=self.BoundingBoxSet()
        ci=np.array([BBn[0],BBn[2]])
        
        f = np.zeros((size[1],size[0],4), np.uint8)
        f4 = np.zeros((size[1],size[0]), np.uint8)
        sz=size
        if aspectlock:
            #if self.image is not None:
            scx=size[0]/(len(self.image[0]))
            scy=size[1]/(len(self.image))
            sca=max(scx,scy)
            sz=(int(sca*len(self.image[0]))+1,int(sca*len(self.image))+1)
            addedim=cv2.resize(self.image, sz)
            addedimage=addedim[:size[1],:size[0],:]
        else:
            addedimage=cv2.resize(self.image, size) #n
        f[:,:,:3] =addedimage
        f4=self.DrawRajat(f4, scale=sc, cent = ci, mask=True)

        f[:,:,3]=f4
        l=size[1]
        w=size[0]
        X1=BBi[2]
        X0=BBi[0]
        #print(X0,X1,l,w)
        crop = img[X1:X1+l,X0:X0+w].copy()
        if not fullpict:
            img[X1:X1+l,X0:X0+w] = blend_transparent(crop, f)
        else:
            img[X1:X1+l,X0:X0+w] = addedimage
            cv2.rectangle(img, (X0,X1),(X0+w,X1+l),self.color,2)
        return img

    #def mouseaction(self,event, x,y,flags,param):
        #GR = param
        #print("Hello")
    #    if event == cv2.EVENT_LBUTTONDOWN:
    #        self.LBUTTONDOWN(x,y)
    #    
    #    if event == cv2.EVENT_RBUTTONDOWN:
    #        self.RBUTTONDOWN(x,y)    

        '''
        if event == cv2.EVENT_LBUTTONUP:
            self.LBUTTONUP(x,y)

        if event == cv2.EVENT_MOUSEMOVE:
            self.MOUSEMOVE(x,y)
        '''

    #def LBUTTONDOWN(self,x,y):
    #    pass
    #
    #def RBUTTONDOWN(self,x,y):
    #    self.maximized = False
    #    cv2.destroyWindow("Maximized")
    #    cv2.waitKey(1)

            


                   
            

 

class edge():
    def __init__(self,node1,node2):
        self.node1 = node1
        self.node2 = node2
        self.label = ""
        self.labelpos = 0

    def update(self): #SIMPLE SWITCH FOR NOW... ei toimi useamman noden ryppäissä...
        n1a = [None,0]
        n2a = [None,0]
        if self.label in self.node1.cargo["Args"]:
            n1a=self.node1.cargo["Args"][self.label]
        if self.label in self.node1.cargo["Args"]:
            n2a=self.node2.cargo["Args"][self.label]
        if n1a[1]>n2a[1]: n2a=n1a
        else: n1a=n2a

        self.node1.cargo["Args"][self.label]=n2a
        self.node2.cargo["Args"][self.label]=n1a
        

    def drawEdge(self,im,scale=1,cent=np.array([0,0]), label=False):
        n1= self.node1
        n2= self.node2
        colorconn=(int(n1.color[0]/2+n2.color[0]/2),\
            int(n1.color[1]/2+n2.color[1]/2),\
            int(n1.color[2]/2+n2.color[2]/2))
        #print(colorconn)
        x1= int((n1.x-cent[0])*scale)
        y1= int((n1.y-cent[1])*scale)
        x2= int((n2.x-cent[0])*scale)
        y2= int((n2.y-cent[1])*scale)

        cv2.line(im,(x1,y1),(x2,y2),colorconn,1,cv2.LINE_AA)
        if label:
            if self.labelpos==0:
                self.labelpos = np.random.random()
            t=self.labelpos
            s=1-self.labelpos
            cv2.putText(im,self.label,(int(x1*t+x2*s),int(y1*t+y2*s)),cv2.FONT_HERSHEY_PLAIN,1.2,colorconn,2)

    


class graph():
    def __init__(self,nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.imgsize = np.array([500,500,3])
        self.BB =self.BoundingBoxSet()
        self.bgcolor=(255,255,255)
        self.cols={}
        self.highlightednode =None
        self.hDx = 0
        self.hDy = 0
        self.mousememory = {}
        self.majorUPD = True
        self.controlpanelflags={"nodes":True,"logos":True,"labels":True,"edges":True,"elabels":False,
                                "labelmap":False, "rajat":False,"aspectlock":True,"color":False,"move":True,"update":True,"video":False}
        self.cpmargin =70
        self.cpgeom=[0,0]

    def BoundingBoxSet(self):
        BB=np.array([999999999.0,-999999999.0,999999999.0,-999999999.0])
        for n in self.nodes:
            if BB[0] > n.x: BB[0] = n.x
            if BB[1] < n.x: BB[1] = n.x
            if BB[2] > n.y: BB[2] = n.y
            if BB[3] < n.y: BB[3] = n.y
        self.BB=BB
        return self.BB


    def DrawGraph(self):
        img=np.ones(self.imgsize, dtype = np.uint8)*255
        
        BB=self.BoundingBoxSet()
        c=np.array([0,0])
        c[0]=BB[0]-3
        c[1]=BB[2]-3
        scx=self.imgsize[0]/(BB[1]-BB[0]+6)
        scy=self.imgsize[1]/(BB[3]-BB[2]+6)
        sc=min(scx,scy)
        
        i=0
        for n in self.nodes:
            i+=1
            n.drawNode(img,scale=sc, cent=c)
        for e in self.edges:
            e.drawEdge(img,scale=sc,cent=c)
            
        return img
    

    def DrawControlPanel(self,img):
        w=self.cpmargin
        marg=15
        hi = self.imgsize[0]
        wi = self.imgsize[1]
        cpdkeys= list(self.controlpanelflags.keys())
        nflags=len(cpdkeys)
        h= min((hi-w)/nflags,w-marg)
        colorg = (   int(self.bgcolor[0] /2)  ,  int(self.bgcolor[1] /2 + 60) ,  int( self.bgcolor[2] /2)   )
        for i in range(nflags):
            x0 = (wi-w+marg,int(i*h)+marg)
            x1 = (wi-marg,int((i+1)*h))
            if self.controlpanelflags[cpdkeys[i]]:
                cv2.rectangle(img,x0,x1,colorg,-1)
            #else:
            #    cv2.rectangle(img,x0,x1,(130,100,100),-1)
            cv2.rectangle(img,x0,x1,(230,200,200),2)
            ts=cv2.getTextSize(cpdkeys[i][0],cv2.FONT_HERSHEY_PLAIN,1.4,2)
            x=int( (x0[0]+ x1[0] - ts[0][0]) /2 )
            y=int( (x0[1]+ x1[1] + ts[0][1]) /2 )
            cv2.putText(img,cpdkeys[i][0],(x,y),cv2.FONT_HERSHEY_PLAIN,1.4,(230,200,200),2)
 
        x0 = (wi-w+marg,hi-marg)
        x1 = (wi-marg,hi-w+marg)
        cv2.rectangle(img,x0,x1,(230,200,200),2)
        ts=cv2.getTextSize("z",cv2.FONT_HERSHEY_PLAIN,1.4,2)
        x=int( (x0[0]+ x1[0] - ts[0][0]) /2 )
        y=int( (x0[1]+ x1[1] + ts[0][1]) /2 )
        cv2.putText(img,"z",(x,y),cv2.FONT_HERSHEY_PLAIN,1.4,(230,200,200),2)
 
        self.cpgeom=[h,marg]
    
    def ChangeCpInXY(self,x,y):
        cpdkeys= list(self.controlpanelflags.keys())
        h=self.cpgeom[0]
        marg=self.cpgeom[1]
        cpm=self.cpmargin
        wi = self.imgsize[1]
        i = int(np.floor(y/h))
        y = y%h
        if (marg < wi-x < cpm-marg) and (marg < y) and (i < len(cpdkeys)):
            self.controlpanelflags[cpdkeys[i]] = not self.controlpanelflags[cpdkeys[i]]
            return True
        return False


    
    def getControlPanelFlags(self):
        if "nodes" in self.controlpanelflags:
            nodes = self.controlpanelflags["nodes"]
        else: nodes = False
        if "logos" in self.controlpanelflags:
            logos = self.controlpanelflags["logos"]
        else: logos= False    
        if "labels" in self.controlpanelflags:
            labels = self.controlpanelflags["labels"]
        else: labels = False   
        if "edges" in self.controlpanelflags:
            edges = self.controlpanelflags["edges"]
        else: edges = False    
        if "elabels" in self.controlpanelflags:
            elabels = self.controlpanelflags["elabels"]
        else: elabels = False    
        if "labelmap" in self.controlpanelflags:
            labelmap = self.controlpanelflags["labelmap"]
        else: labelmap = False    
        if "rajat" in self.controlpanelflags:
            rajat = self.controlpanelflags["rajat"]
        else: rajat = False    
        if "aspectlock" in self.controlpanelflags:
            aspectlock = self.controlpanelflags["aspectlock"]
        else: aspectlock = False    
    
        return nodes,logos,labels,edges,elabels,labelmap,rajat,aspectlock

    def RunWithControlPanel(self):
        cv2.startWindowThread()
        cv2.namedWindow('Graafi')
        cv2.setMouseCallback('Graafi',self.mouseaction)
        while True:
            if "move" in self.controlpanelflags:
                if self.controlpanelflags["move"]:
                    self.MoveAll(sc=1)
            if "update" in self.controlpanelflags:
                if self.controlpanelflags["update"]:
                    self.UpdateAll()
            img = self.DrawGraph2(cp = True)#rajat=False, edges=True,labels=True, nodes =True, elabels=False, labelmap=True,logos=True)
            cv2.imshow("Graafi",img)
            inp= cv2.waitKey(1)
            if inp==27:
                break
        cv2.destroyWindow("Graafi")
        cv2.waitKey(1)
    
    

    def RunThreaded(self,video=False):
        if video: self.controlpanelflags["video"] = True
        upd=False
        mov=False
        vid=False
        cv2.startWindowThread()
        cv2.namedWindow('Graafi')
        cv2.setMouseCallback('Graafi',self.mouseaction)
        while True:
            
            if "update" in self.controlpanelflags:
                if self.controlpanelflags["update"]:
                    if not upd:
                        GRUpd=GRUpdateThread(1,self)
                        GRUpd.start()
                        upd=True
                else: upd= False
                    
            if "move" in self.controlpanelflags:
                if self.controlpanelflags["move"]:
                    self.MoveAll(sc=1)
                    #if not mov:
                    #    GRMov=GRMoveThread(2,self)
                    #    GRMov.start()
                    #    mov=True
                else: mov = False
            
            img = self.DrawGraph2(cp = True)#rajat=False, edges=True,labels=True, nodes =True, elabels=False, labelmap=True,logos=True)
            
            if "video" in self.controlpanelflags:
                if self.controlpanelflags["video"]:
                    if not vid:
                        writer = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30,(self.imgsize[1],self.imgsize[0])) 
                        vid = True
                    writer.write(img)
                    cv2.circle(img,(20,20),10,(0,0,255), -1)
                    cv2.putText(img,"REC",(35,25), cv2.FONT_HERSHEY_PLAIN,1.5,(255,255,255),2)
                else:
                    if vid:
                        writer.release()
                        vid = False

            cv2.imshow("Graafi",img)
            inp= cv2.waitKey(1)
            if inp==27:
                break
        self.controlpanelflags["move"]=False
        self.controlpanelflags["update"]=False
        cv2.destroyWindow("Graafi")
        cv2.waitKey(1)
 

    def GRImageParams(self):
        margi=50
        rightmargin = self.cpmargin
        BB=self.BoundingBoxSet()
        c=np.array([0,0])
        scx=(self.imgsize[1]-margi-rightmargin)/(BB[1]-BB[0])
        scy=(self.imgsize[0]-margi)/(BB[3]-BB[2])
        sc=min(scx,scy)
        
        BB[1]=(self.imgsize[1]-margi-rightmargin)/sc+BB[0]
        BB[3]=(self.imgsize[0]-margi)/sc+BB[2]
        margper2=margi/sc/2
        c[0]=BB[0]-margper2
        c[1]=BB[2]-margper2
        return sc,c,BB

    def DrawGraph2(self, rajat = False, nodes = True, edges=True,labels=False,elabels =False,labelmap=False,logos=True,cp=False):
        if self.controlpanelflags["color"]:
            Recolor(self,colorscheme ="random")
            self.controlpanelflags["color"]=False

        if "iszdx" in self.mousememory:
            dx = self.mousememory.pop("iszdx",None)
            if not self.controlpanelflags["video"]:
                self.imgsize[1] = self.imgsize[1] + dx
                self.majorUPD = True
            if "xi" in self.mousememory:
                self.mousememory["xi"]=self.mousememory["xi"]+dx
        if "iszdy" in self.mousememory:
            dy = self.mousememory.pop("iszdy",None)
            if not self.controlpanelflags["video"]:
                self.imgsize[0] = self.imgsize[0] + dy
                self.majorUPD = True
            if "yi" in self.mousememory:
                self.mousememory["yi"]=self.mousememory["yi"]+dy
        if cp:
           nodes,logos,labels,edges,elabels,labelmap,rajat,aspect = self.getControlPanelFlags() 
        else: aspect =False
            

        img=np.ones(self.imgsize, dtype = np.uint8)
        img[:,:,0]=self.bgcolor[0]
        img[:,:,1]=self.bgcolor[1]
        img[:,:,2]=self.bgcolor[2]

        sc,c,BB = self.GRImageParams()
        
        if rajat:
            if self.majorUPD:
                self.GRRajat()
                self.majorUPD = False   
            for n in self.nodes:
                if not (n.image is None):
                    n.liitaKuva(img, sc=sc,c=c,aspectlock = aspect)
                    n.DrawRajat(img, r=5, scale=sc, cent=c,borders=True)
                else:
                    n.DrawRajat(img, r=5, scale=sc, cent=c)
            #for n in self.nodes:
            #    if n.highlighted:
            #        if not (n.image is None):
            #            n.liitaKuva(img, sc=sc,c=c, fullpict=True)
            #        else:
            #            pass
        else:
            self.majorUPD = True

        if labelmap:
            self.DrawLabelMap(img,heatmap=True)   

        if edges:
            for e in self.edges:
                e.drawEdge(img,scale=sc, cent=c, label = elabels)
        if nodes:
            for n in self.nodes:
                if not rajat: n.tontinrajat=[]
                n.drawNode(img,scale=sc, cent=c,label=labels,logo=logos)  

        if cp: self.DrawControlPanel(img)      
        
        if not self.controlpanelflags["video"]:
            x0 = (self.imgsize[1]-60, self.imgsize[0]-60)
            x1 = (self.imgsize[1]-50, self.imgsize[0]-50)
            cv2.rectangle(img,x0,x1,(130,100,100),-1)
            cv2.rectangle(img,x0,x1,(230,200,200),2)
        return img
    
    def GRRajat(self):
        sc,c,BB = self.GRImageParams()
        for n in self.nodes:
            n.tontinrajat=[]
        #Determine Center lines between nodes
        i=0
        CLs=[]        
        for n in self.nodes[:-1]:
            i+=1
            for nn in self.nodes[i:]:
                eX,eV = n.CenterLine(nn)
                CLs.append(centerline(eX,eV,n,nn))
        #Determine end points of center lines
        i=0    
        for cl in CLs[:-1]:
            i+=1
            for cll in CLs[i:]:
                P,ko=cl.coll(cll)
                if ko and (BB[0]<=P[0]<=BB[1]) and (BB[2]<=P[1]<=BB[3]):
                    cl.endp.append(P)
                    cll.endp.append(P)
        
        #Determine image - edge end points
        ies,nodecorn =self.imgedges(BB)
        for cl in CLs:
            for ie in ies:
                P,ko=cl.coll(ie)
                if (BB[0]-1e-12<=P[0]<=BB[1]+1e-12) and (BB[2]-1e-12<=P[1]<=BB[3]+1e-12): 
                    cl.endp.append(P)
                #elif (BB[0]-.0001<=P[0]<=BB[1]) and (BB[2]-.0001<=P[1]<=BB[3]):
                #    print(P[0]-BB[0],P[1]-BB[2])
            for n in self.nodes:
                cl.NodeVsEndp(n)
        
        #Determine node area cornerpoints
        for cl in CLs:
            cl.node1.tontinrajat =cl.node1.tontinrajat + cl.endp
            cl.node2.tontinrajat= cl.node2.tontinrajat + cl.endp
        self.cornernodes(BB)
        #Arrange and clean area cornerpoints
        for n in self.nodes:
            n.arrangerajat()
           
    def EdgeLabelMap(self, resolution = 10):
        #BB=self.BoundingBoxSet()
        sc,c,BB = self.GRImageParams()
        mappxx=(BB[1]-BB[0])/resolution
        mappxy=(BB[3]-BB[2])/resolution
        bx=BB[0]
        by=BB[2]
        me =[[ [] for _ in range(resolution)] for _ in range(resolution)]
        for e in self.edges:
            i = int((e.node1.x-bx)/mappxx)
            j = int((e.node1.y-by)/mappxy)
            if (0<=i<resolution) and (0<=j<resolution):
                me[i][j].append(e.label)
            i = int((e.node2.x-bx)/mappxx)
            j = int((e.node2.y-by)/mappxy)
            if (0<=i<resolution) and (0<=j<resolution):
                me[i][j].append(e.label)
        
        for i in range(resolution):
            for j in range(resolution):
                if me[i][j] != []:
                    me[i][j]=max(me[i][j], key=me[i][j].count)
        
        return me
            
    def DrawLabelMap(self, im, resolution =10,heatmap=False):
        
        me = self.EdgeLabelMap(resolution = resolution)
        #sc,c,BB = self.GRImageParams()
        #mx=int((BB[1]-BB[0])/resolution*sc)
        #my=int((BB[3]-BB[2])/resolution*sc)
        mx=int((len(im[0])-self.cpmargin)/resolution) 
        my=int(len(im)/resolution)
        bx=int(mx/3)
        by=int(my/3)
        
        for i in range(resolution):
            for j in range(resolution):
                if me[i][j] != []:
                    if me[i][j] in self.cols:
                        col=self.cols[me[i][j]]
                    else:
                        col = (np.random.randint(255,dtype=int),np.random.randint(255,dtype=int),np.random.randint(255,dtype=int))
                        self.cols.update({me[i][j]:col})
                    cv2.rectangle(im,(i*mx,j*my),((i+1)*mx,(j+1)*my),col,-1)
                    cv2.putText(im,me[i][j],(bx+i*mx,by+j*my),cv2.FONT_HERSHEY_PLAIN,1.5,(200,180,180),2)
                else:
                    cv2.rectangle(im,(i*mx,j*my),((i+1)*mx,(j+1)*my),(0,0,0),-1)


    
    def cornernodes(self,BB):
        corners = [np.array([BB[0],BB[2]]),np.array([BB[0],BB[3]]),\
                   np.array([BB[1],BB[2]]),np.array([BB[1],BB[3]]) ] 
        cnodes= [self.nodes[0],self.nodes[0],self.nodes[0],self.nodes[0]]
        ln = [9999999999,999999999999,99999999999,9999999999]      
        for n in self.nodes:
            for i in range(4):
                ls=Vlen2(corners[i]-np.array([n.x,n.y]))
                if ls < ln[i]:
                    ln[i]=ls
                    cnodes[i]=n
        for i in range(4):
            cnodes[i].tontinrajat.append(corners[i])



    def imgedges(self,BB):
        imgEdges=[]
        iens=[]
        iens.append(node(BB[0],BB[2]))
        iens.append(node(BB[0],BB[3]))
        iens.append(node(BB[1],BB[3]))
        iens.append(node(BB[1],BB[2]))


        imgEdges.append(centerline(np.array([BB[0],BB[2]]),np.array([0,1]),iens[0],iens[1]))
        imgEdges.append(centerline(np.array([BB[0],BB[2]]),np.array([1,0]),iens[0],iens[3]))
        imgEdges.append(centerline(np.array([BB[1],BB[3]]),np.array([0,-1]),iens[2],iens[3]))
        imgEdges.append(centerline(np.array([BB[1],BB[3]]),np.array([-1,0]),iens[2],iens[1]))

        return imgEdges, iens

    def UpdateAll(self):
        for e in self.edges:
            e.update()
        for n in self.nodes:
            n.update()
    

    def MoveAll(self,  sc=1, scAuto=True):
        if scAuto:
            sc=5.0/len(self.nodes)*sc
        self.ClearPot()
        self.PotNodeSize(sc=sc)
        #self.PotNodePoints(sc=sc)
        self.StepAllPot()
        self.majorUPD=True

    def ClearPot(self):
        for n in self.nodes:
            n.pot=np.array([0.0,0.0])
    
    def ResetNodeSizes(self):
        for n in self.nodes:
            n.size=20
    
    def PotNodePoints(self, sc=1):
        i=0
        for n in self.nodes[:-1]:
            i+=1
            for nn in self.nodes[i:]:
                pot=potential(nn.x-n.x, nn.y-n.y, mode="rep", scale=sc)
                n.pot-=pot
                nn.pot+=pot
        for e in self.edges:
            n=e.node1
            nn=e.node2
            pot=potential(nn.x-n.x, nn.y-n.y, mode="normal",scale=sc)
            n.pot-=pot
            nn.pot+=pot

    def PotNodeSize(self, sc=1):
        i=0
        for n in self.nodes[:-1]:
            i+=1
            for nn in self.nodes[i:]:
                dX=np.array([nn.x-n.x, nn.y-n.y])
                pot=PotentialSize(dX, size=n.size+nn.size, repulsion = True, scale=sc)
                #pot=potential(nn.x-n.x, nn.y-n.y, mode="rep", scale=sc)
                n.pot+=pot
                nn.pot-=pot
        for e in self.edges:
            n=e.node1
            nn=e.node2
            dX=np.array([nn.x-n.x, nn.y-n.y])
            pot=PotentialSize(dX, size=n.size+nn.size, repulsion = False, scale=sc)
            #pot=potential(nn.x-n.x, nn.y-n.y, mode="normal",scale=sc)
            n.pot+=pot
            nn.pot-=pot

    def StepAllPot(self):
        for n in self.nodes:
            if not n.fixed:
                n.x+=n.pot[0]
                n.y+=n.pot[1]


    def mouseaction(self,event, x,y,flags,param):
        #GR = param
        #print("Hello")
        if event == cv2.EVENT_LBUTTONDOWN:
            if flags == 33:
                self.altLBUTTONDOWN(x,y)
            elif flags == 9:
                self.LBUTTONDBLCLK(x,y)
            else:
                self.LBUTTONDOWN(x,y)
        
        if event == cv2.EVENT_RBUTTONDOWN:
            self.RBUTTONDOWN(x,y)    

        if event == cv2.EVENT_LBUTTONDBLCLK:
            self.LBUTTONDBLCLK(x,y)     

        if event == cv2.EVENT_LBUTTONUP:
            if flags == 33:
                self.altLBUTTONUP(x,y)
            else:    
                self.LBUTTONUP(x,y)

        if event == cv2.EVENT_MOUSEMOVE:
            self.MOUSEMOVE(x,y)
        
    def altLBUTTONDOWN(self,x,y):
        found, n = self.NodeinXY(x,y)
        if found:
            sc,c,BB = self.GRImageParams()
            self.mousememory.update({"rnode":n, "xi":c[0] + x/sc ,"yi": c[1] + y/sc})
    
    def altLBUTTONUP(self,x,y):
        if "rnode" in self.mousememory:
            sc,c,BB = self.GRImageParams()
            dx = x/sc +c[0]-self.mousememory.pop("xi",None)
            dy = y/sc +c[1]-self.mousememory.pop("yi",None)
            self.mousememory["rnode"].size = np.sqrt(dx*dx + dy*dy)
            self.mousememory.pop("rnode",None)
 

    def LBUTTONDOWN(self,x,y):
        
        x0 = (self.imgsize[1]-60, self.imgsize[0]-60)
        x1 = (self.imgsize[1]-50, self.imgsize[0]-50)
        if (x0[0] <= x <= x1[0]) and (x0[1] <= y <= x1[1]):
            self.mousememory.update({"imsize":True, "xi":x ,"yi": y})
            return
        if x > self.imgsize[1]-self.cpmargin:
            if self.ChangeCpInXY(x,y):
                return
        
        found, n = self.NodeinXY(x,y)
        
        if found:
            n.highlighted = not n.highlighted
            sc,c,BB = self.GRImageParams()
            self.highlightednode = n
            self.hdx= n.x - c[0] - x/sc
            self.hdy= n.y - c[1] - y/sc 
    
    def LBUTTONDBLCLK(self,x,y):
        found, n = self.NodeinXY(x,y)
        
        if found:
            n.maximized= not n.maximized
    
    
    def LBUTTONUP(self,x,y):
        if "imsize" in self.mousememory:
            dx = x -self.mousememory.pop("xi")
            dy = y -self.mousememory.pop("yi")
            self.mousememory.update({"imsize":True, "iszdx":dx ,"iszdy": dy})
            self.mousememory.pop("imsize")
            #self.imgsize[0] = self.imgsize[0] + dx
            #self.imgsize[1] = self.imgsize[1] + dy
            return

        self.highlightednode = None      

    def RBUTTONDOWN(self,x,y):
        #print(self.highlightednode, self.hdy, self.hdx, x, y)
        if self.highlightednode is not None:
            self.highlightednode.fixed = not self.highlightednode.fixed
        self.highlightednode = None      
    

    def MOUSEMOVE(self,x,y):        
        if "imsize" in self.mousememory:
            dx = x -self.mousememory["xi"]
            dy = y -self.mousememory["yi"]
            self.mousememory.update({"imsize":True, "iszdx":dx ,"iszdy": dy})
            #self.imgsize[0] = self.imgsize[0] + dx
            #self.imgsize[1] = self.imgsize[1] + dy
            return

        if self.highlightednode is not None:
            #print(self.highlightednode, self.hdy, self.hdx, x, y)
            sc,c,BB = self.GRImageParams()
            self.highlightednode.x = c[0] + x/sc + self.hDx
            self.highlightednode.y = c[1] + y/sc + self.hDy
            self.majorUPD = True
            return False
 

    def NodeinXY(self,x,y):
        ns=[]
        sc,c,BB = self.GRImageParams()
        for n in self.nodes:
            bb=n.BBinImage(scale=sc,cent=c)
            if (bb[0]<=x<=bb[1]) and (bb[2]<=y<=bb[3]):
                ns.append(n)
       
        if len(ns)==0:
            return False, None
        if len(ns)==1:
            return True, ns[0]
        i=0 
        nx=ns[0]  
        l=99999999999    
        for n in ns:
            ln = Vlen(np.array([x,y])-np.array(  [ (n.x-c[0])*sc , (n.y-c[1])*sc ]  ))
            #print(l, ln, n, nx)
            if ln<l:
                l=ln
                nx=n
            #print(l, ln, n, nx)
        return True, nx


class GRUpdateThread(threading.Thread):
    def __init__(self,threadID,GR,name="UpdateGR"):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name=name
        self.GR = GR
    
    def run(self):
        print("starting upd")
        while True:
            if "update" in self.GR.controlpanelflags:
                if self.GR.controlpanelflags["update"]:
                    self.GR.UpdateAll()
                else:
                    print("ending upd") 
                    return
            else: 
                print("ending upd") 
                return

class GRMoveThread(threading.Thread):
    def __init__(self,threadID,GR,name="MoveGR"):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name=name
        self.GR = GR
    
    def run(self):
        print("Starting mov")
        while True:
            if "move" in self.GR.controlpanelflags:
                if self.GR.controlpanelflags["move"]:
                    self.GR.MoveAll(sc=1)
                else:
                    print("Ending mov") 
                    return
            else:
                print("Ending mov")  
                return


 

class centerline():
    def __init__(self,eX,eV,node1,node2):
        self.eX = eX
        self.eV = eV
        self.node1=node1
        self.node2=node2
        self.endp=[]

    def coll(self,other):
        B=self.eV
        A=self.eX-other.eX
        C=other.eV
        p=C[1]*B[0]-B[1]*C[0]
        if p==0:
            return False, np.array([999999,99999])
        t=(A[1]*B[0]-A[0]*B[1])/p
        s=(A[1]*C[0]-A[0]*C[1])/p
        P=self.eX+s*B
        #coll=(0<t<1)&(0<s<1)

        ls=Vlen2(P-np.array([self.node1.x,self.node1.y]))
        lo=Vlen2(P-np.array([other.node1.x,other.node1.y]))
        coll = -.001*ls<(ls-lo)<.001*ls

        return P, coll 
    
    def NodeVsEndp(self,onode):
        if (onode == self.node1) or (onode==self.node2): return
        #print(self.endp)
        endp=[]
        for P in self.endp:
            ls=Vlen2(P-np.array([self.node1.x,self.node1.y]))
            lo=Vlen2(P-np.array([onode.x,onode.y]))
            #print(lo,ls)
            if (lo>=ls*0.999): 
                endp.append(P)
        self.endp = endp
                

    
    def DrawCL(self, im,scale=1,cent=np.array([0,0]),r=3):
        n1= self.node1
        n2= self.node2
        colorconn=(int(n1.color[0]/2+n2.color[0]/2),\
                int(n1.color[1]/2+n2.color[1]/2),\
                int(n1.color[2]/2+n2.color[2]/2))
        i=0
        for ep in self.endp[:-1]:
            i+=1
            epp=self.endp[i]
            x1= int((ep[0]-cent[0])*scale)
            y1= int((ep[1]-cent[1])*scale)
            x2= int((epp[0]-cent[0])*scale)
            y2= int((epp[1]-cent[1])*scale)

            cv2.line(im,(x1,y1),(x2,y2),colorconn,1)
            cv2.circle(im, (x1,y1),r,colorconn,-1)
            cv2.circle(im, (x2,y2),r,colorconn,-1)


def blend_transparent(face_img, overlay_t_img):
    # Split out the transparency mask from the colour info
    overlay_img = overlay_t_img[:,:,:3] # Grab the BRG planes
    overlay_mask = overlay_t_img[:,:,3:]  # And the alpha plane

    # Again calculate the inverse mask
    background_mask = 255 - overlay_mask

    # Turn the masks into three channel, so we can use them as weights
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    # Create a masked out face image, and masked out overlay
    # We convert the images to floating point in range 0.0 - 1.0
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    # And finally just add them together, and rescale it back to an 8bit integer image    
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))

def DICTfromKEYWDS(KEYWDS, GRAAFI):
    NodeNames=list(KEYWDS.keys())
    i=0
    for nn in NodeNames:
        GRAAFI["Nodes"][nn]={"Keywords":KEYWDS[nn]}
    for nn in NodeNames[:-1]:
        i+=1
        for nnn in NodeNames[i:]:
            for kw in KEYWDS[nn]:
                for kww in KEYWDS[nnn]:
                    if kw == kww:
                        GRAAFI["Edges"].append([nn,nnn,kw])
    return GRAAFI

def IMAGEStoDICT(IMAGES, GRAAFI):
    NodeNames=list(IMAGES.keys())
    for nn in NodeNames:
        GRAAFI["Nodes"][nn]["image"]=IMAGES[nn]
    return GRAAFI


def DICTfromCARGOFUN(CARGOFUN,ARGS,ARGVALUES,GRAAFI):
    NodeNames=list(ARGS.keys())
    i=0
    for nn in NodeNames:
        GRAAFI["Nodes"][nn]={"Args":{}}
        for a in ARGS[nn]:
            GRAAFI["Nodes"][nn]["Args"][a]=timedArg(ARGVALUES[a])
        GRAAFI["Nodes"][nn]["Function"]=CARGOFUN[nn]        
    for nn in NodeNames[:-1]:
        i+=1
        for nnn in NodeNames[i:]:
            for kw in ARGS[nn]:
                for kww in ARGS[nnn]:
                    if kw == kww:
                        GRAAFI["Edges"].append([nn,nnn,kw])
    return GRAAFI


def GRfromDICT(GRAAFI,rx,ry, colorscheme = "BW", color = (128,100,100)):
    nodes=[]
    NodeNames=list(GRAAFI["Nodes"].keys())
    for nn in NodeNames:
        n=node(np.random.random()*rx,np.random.random()*ry)
        n.label = nn
        n.image=cv2.imread(GRAAFI["Nodes"][nn]["image"])
        n.cargo = GRAAFI["Nodes"][nn]
        GRAAFI["Nodes"][nn].update({"node":n})
        nodes.append(n)
    edges=[]
    for e in GRAAFI["Edges"]:
        n1=GRAAFI["Nodes"][e[0]]["node"]
        n2=GRAAFI["Nodes"][e[1]]["node"]     
        ed=edge(n1,n2)
        if len(e)>2: ed.label =e[2]
        edges.append(ed)
        n1.size=n1.size+5.0
        n2.size=n2.size+5.0
    GR=graph(nodes,edges)
    Recolor(GR, colorscheme, color)
    GR.imgsize=np.array([ry,rx,3])
    return GR

def Recolor(GR,colorscheme = "BW", color = (128,100,100),balance=0.66,branch=False):
    if colorscheme == "random":
        schemes=["color","opposites","oppositesrnd","triangle","colorrnd","BW","colorful"]
        colorscheme=schemes[np.random.randint(len(schemes))]
        color =(np.random.randint(255,dtype=int),np.random.randint(255,dtype=int),np.random.randint(255,dtype=int))
        balance=np.random.random()
        branch=np.random.randint(2)

    
    for n in GR.nodes:
        if colorscheme == "color":
            n.color=color
        if colorscheme == "opposites":
            col = color
            if np.random.random()>balance:
                col = (255 - color[0],255 - color[1],255-color[2])
            n.color = col
        if colorscheme == "oppositesrnd":
            col = color
            if np.random.random()>balance:
                cmx=max(color)
                col= (cmx - color[0],cmx - color[1],cmx-color[2])
            c=np.random.random()
            cc=np.random.random()*(1-c)
            #cc=cc*cc*cc
            col = (int(c*col[0]+cc*255),int(c*col[1]+cc*255),int(c*col[2]+cc*255))
            n.color = col
        if colorscheme == "triangle":
            col = color
            if np.random.random()>balance:
                col= (col[2],col[0],col[1])
                if np.random.random()>balance:
                    col= (col[2],col[0],col[1])
            c=np.random.random()
            cc=np.random.random()*(1-c)
            #cc=cc*cc*cc
            col = (int(c*col[0]+cc*255),int(c*col[1]+cc*255),int(c*col[2]+cc*255))
            n.color = col
        if colorscheme == "colorrnd":
            col = color
            c=np.random.random()
            cc=np.random.random()*(1-c)
            #cc=cc*cc*cc
            col = (int(c*col[0]+cc*255),int(c*col[1]+cc*255),int(c*col[2]+cc*255))
            n.color = col
        if colorscheme == "BW":
            col=np.random.randint(255,dtype=int)
            n.color=(col,col,col)
        if colorscheme == "colorful":
            n.color=(np.random.randint(255,dtype=int),np.random.randint(255,dtype=int),np.random.randint(255,dtype=int))
        if branch:
            colorBranches(GR)



def colorBranches(GR,order=3, sat = 0.1, inv=True):
    for j in range(order):
        for e in GR.edges:
            c1=np.array(e.node1.color)
            c2=np.array(e.node2.color)        
            s1=e.node1.size
            s2=e.node2.size
            if inv:
                s1=1/s1
                s2=1/s2
            c=np.array([0,0,0])
            c=(c1*s1 +c2*s2)/(s1+s2)
            c1=(c/2+c1/2)
            c2=(c/2+c2/2)
            if sat:
                m1=max(c1)
                c1=c1-min(c1)*sat
                c1=c1/max(c1)*m1
                m2=max(c2)
                c2=c2-min(c2)*sat
                c2=c2/max(c2)*m2

            e.node1.color=(int(c1[0]),int(c1[1]), int(c1[2])  )
            e.node2.color=(int(c2[0]),int(c2[1]), int(c2[2])  )

def ALTEdgesfromKEYWDS(KEYWDS,GRAAFI):
    NodeNames=list(KEYWDS.keys())
    i=0
    #for nn in NodeNames:
    #    GRAAFI["Nodes"].update({nn:{"Keywords":KEYWDS[nn]}})
    GRF={"Edges":[]}
    for nn in NodeNames[:-1]:
        i+=1
        for nnn in NodeNames[i:]:
            for kw in KEYWDS[nn]:
                for kww in KEYWDS[nnn]:
                    if kw == kww:
                        GRF["Edges"].append([nn,nnn,kw])

    edges=[]
    for e in GRF["Edges"]:
        n1=GRAAFI["Nodes"][e[0]]["node"]
        n2=GRAAFI["Nodes"][e[1]]["node"]     
        ed=edge(n1,n2)
        if len(e)>2: ed.label =e[2]
        edges.append(ed)
        n1.size=n1.size+5.0
        n2.size=n2.size+5.0
    return edges

def createARGLIST(ARGS,ARGLIST):
    NodeNames=list(ARGS.keys())
    for nn in NodeNames:
        for a in ARGS[nn]:
            ARGLIST.update({a:None})
            
def createNODELIST(ANYLIST,NODELIST):
    NodeNames=list(ANYLIST.keys())
    for nn in NodeNames:
        NODELIST.update({nn:None})

def timedArg( a ):
    return [a,time.time()]

''' EXAMPLE OF IMAGES, KEYWDS, ALTKEYWDS
IMAGES={
    "kuu":"kuu.jpg",
    "konna":"konna.jpg",
    "silma":"SILMA.jpg",
    "janne":"Janne.jpg",
    "kerpsu":"kerpsu.jpg",
    "mokki":"mokki.jpg",
    "sorsa":"sorsa.jpg"
}

KEYWDS={
    "kuu":["pimea","maisema","kuu","rakennus"],
    "konna":["elain","silma","luonto","konna"],
    "silma":["silma","maisema","ihminen"],
    "janne":["silma","ihminen"],
    "kerpsu":["elain"],
    "mokki":["rakennus","luonto"],
    "sorsa":["elain","luonto"]
}

ALTKEYWDS={
    "kuu":["musta","sininen","oranssi"],
    "konna":["keltainen"],
    "silma":["sininen","harmaa","vihrea","valkoinen"],
    "janne":["sininen","valkoinen"],
    "kerpsu":["musta"],
    "mokki":["harmaa","sininen","vihrea"],
    "sorsa":["keltainen","sininen","punainen","vihrea"]
}
'''