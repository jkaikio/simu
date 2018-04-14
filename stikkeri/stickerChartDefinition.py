from BlockChart import *
from stickerBlockFunctions import *
from stickerSources import *

global BlockSources
global MAIN_BC
global sourceDict

sourceDict ={}
#Power block###########################
FB_power=[]
data={"Round":0}
fb1=Bus(busdata=data,label="PowerBus")
sourceDict.update({"PowerBus":fb1})
FB_power.append(FunctionBlock(fb1,size=np.array([120,90]), pos=np.array([0,0])))

f=OnOff(True, label ="Mains")
FB1=FunctionBlock(f,size=np.array([120,90]), pos=np.array([0,0]))
FB_power.append(FB1)

f1=Photovoltaic(label ="Solar cell")
FB=FunctionBlock(f1,size=np.array([120,90]), pos=np.array([0,0]))
FB.bgcolor=(200,200,255)
FB_power.append(FB)

f1=NullFunc(label ="Long Term Battery")
FB=FunctionBlock(f1,size=np.array([120,90]), pos=np.array([0,99]))
FB.bgcolor=(230,230,255)
FB_power.append(FB)

f1=Supercaps(label ="Supercaps")
FB=FunctionBlock(f1,size=np.array([120,90]), pos=np.array([0,199]))
FB.bgcolor=(200,200,255)
FB_power.append(FB)

f1=NullFunc(label ="Harvester circuitry")
FB=FunctionBlock(f1,size=np.array([120,90]), pos=np.array([0,299]))
FB.bgcolor=(200,255,255)
FB_power.append(FB)

f1=NullFunc(label ="Voltage regulation")
FB=FunctionBlock(f1,size=np.array([120,90]), pos=np.array([0,399]))
FB.bgcolor=(200,255,255)
FB_power.append(FB)



#Logics block#########################
FB_logic=[]
data={"Round":0}
fb1=Bus(busdata=data,label="SensorBus")
sourceDict.update({"SensorBus":fb1})
FB_logic.append(FunctionBlock(fb1,size=np.array([120,90]), pos=np.array([0,0])))

f1=NullFunc(label ="Microcontroller")
FB=FunctionBlock(f1,size=np.array([120,90]), pos=np.array([0,0]))
FB.bgcolor=(200,255,255)
FB_logic.append(FB)

f1=NullFunc(label ="Sensors")
FB=FunctionBlock(f1,size=np.array([120,90]), pos=np.array([0,99]))
FB.bgcolor=(200,255,255)
FB_logic.append(FB)

f1=NullFunc(label ="Indicator")
FB=FunctionBlock(f1,size=np.array([120,90]), pos=np.array([0,199]))
FB.bgcolor=(200,255,255)
FB_logic.append(FB)



#Radio block##########################
FB_radio=[]
data={"Round":0}
fb1=Bus(busdata=data,label="RadioBus")
sourceDict.update({"RadioBus":fb1})
FB_radio.append(FunctionBlock(fb1,size=np.array([120,90]), pos=np.array([0,0])))

f1=NullFunc(label ="Communication radio")
FB=FunctionBlock(f1,size=np.array([120,90]), pos=np.array([0,199]))
FB.bgcolor=(200,255,255)
FB_radio.append(FB)

f1=NullFunc(label ="Positioning radio")
FB=FunctionBlock(f1,size=np.array([120,90]), pos=np.array([0,199]))
FB.bgcolor=(230,255,230)
FB_radio.append(FB)

f1=NullFunc(label ="NFC")
FB=FunctionBlock(f1,size=np.array([120,90]), pos=np.array([0,199]))
FB.bgcolor=(230,255,230)
FB_radio.append(FB)

f1=NullFunc(label ="Antenna")
FB=FunctionBlock(f1,size=np.array([120,90]), pos=np.array([0,199]))
FB.bgcolor=(200,255,255)
FB_radio.append(FB)

f1=NullFunc(label ="Posit. Antenna")
FB=FunctionBlock(f1,size=np.array([120,90]), pos=np.array([0,199]))
FB.bgcolor=(230,255,230)
FB_radio.append(FB)


FB_gateway=[]

f1=NullFunc(label ="Gateway")
FB=FunctionBlock(f1,size=np.array([120,90]), pos=np.array([0,199]))
FB.bgcolor=(200,255,255)
FB_gateway.append(FB)

data={"Round":0}
fb1=Bus(busdata=data,label="RadioChannel")
sourceDict.update({"RadioChannel":fb1})
FB_gateway.append(FunctionBlock(fb1,size=np.array([12,9]), pos=np.array([0,0])))




#Environment Block
FB_env =[]
f1=Environment(label ="Environment")
FB=FunctionBlock(f1,size=np.array([120,90]), pos=np.array([0,199]))
FB.bgcolor=(200,255,255)
FB_env.append(FB)

data={"Round":0}
fb1=Bus(busdata=data,label="EnvironmentData")
sourceDict.update({"EnvironmentData":fb1})
FB_env.append(FunctionBlock(fb1,size=np.array([12,9]), pos=np.array([0,0])))

#MAIN SECTION
FBs=[]
data={"Round":0}
fb1=Bus(busdata=data,label="MainBus")
sourceDict.update({"MainBus":fb1})
FBs.append(FunctionBlock(fb1,size=np.array([12,9]), pos=np.array([0,0])))

fb1=Monitor(label="MainMonitor")
sourceDict.update({"MainMonitor":fb1})
FBs.append(FunctionBlock(fb1,size=np.array([12,9]), pos=np.array([0,0])))


#Block charts
BC_power=BlockChart(FB_power,BlockSources,sourceDict)
BC_env=BlockChart(FB_env,BlockSources,sourceDict)
BC_logic=BlockChart(FB_logic,BlockSources,sourceDict)

BC_gateway=BlockChart(FB_gateway,BlockSources,sourceDict)
ss=SubChart(BC_gateway,label = "Gateway block")
ss.chart.bgcolor=(255,255,200)
F=FunctionBlock(ss,size=np.array([777,777]), pos=np.array([0,0]))
F.linecolor=(255,66,66)
FB_radio.append(F)

BC_radio=BlockChart(FB_radio,BlockSources,sourceDict)


ss=SubChart(BC_power,label = "Power block")
ss.chart.bgcolor=(200,240,255)
F=FunctionBlock(ss,size=np.array([777,777]), pos=np.array([0,0]))
F.linecolor=(255,66,66)
FBs.append(F)

ss=SubChart(BC_logic,label = "Logic block")
ss.chart.bgcolor=(150,255,150)
F=FunctionBlock(ss,size=np.array([777,777]), pos=np.array([0,0]))
F.linecolor=(66,66,255)
FBs.append(F)

ss=SubChart(BC_radio,label = "Radio block")
ss.chart.bgcolor=(150,255,150)
F=FunctionBlock(ss,size=np.array([777,777]), pos=np.array([0,0]))
F.linecolor=(66,255,255)
FBs.append(F)

ss=SubChart(BC_env,label = "Environment block")
ss.chart.bgcolor=(150,255,255)
F=FunctionBlock(ss,size=np.array([777,777]), pos=np.array([0,0]))
F.linecolor=(66,255,66)
FBs.append(F)


BC=BlockChart(FBs,BlockSources,sourceDict)
MAIN_BC =BC
