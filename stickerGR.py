from nodefun import *

IMAGES={
    #Power block
    "MainSwitch":"onoff.jpg",
    "SolarCell":None,
    "LongTermBattery":None,
    "SuperCaps":None,
    "HarvesterCircuits":None,
    "VoltageRegulation":None,
    "PowerMonitor": None,
    
    #Logics block
    "Microcontroller":None,
    "Sensors":None,
    "Indicator":None,
    
    #Radio block
    "CommunicationRadio":None,
    "PositioningAntenna":None,
    "NFC":None,
    "PositioningRadio":None,
    "CommunicationAntenna":None,
    "RadioChannel":None,
    
    #Gateway block
    "Gateway":None,
    "Internet":None,
    
    #Environment block
    "Environment":None,
    
}


ARGS={
    #Power block
    "MainSwitch":["OnState_Main"],
    "SolarCell":["V_PV","P_PV_Out","Lightness","P_Tot_Out"],
    "LongTermBattery":["E_Batt","V_Batt","P_Batt","P_Tot_Out","E_SC"],
    "SuperCaps":["V_SC","E_SC","P_SC_Out","P_SC_In","P_SC_Out_Req","V_PV"],
    "HarvesterCircuits":["OnState_Main","V_PV","P_PV_Out","E_Batt","V_Batt","P_Batt",\
                         "V_SC","E_SC","P_SC_Out","P_SC_Out_Req","P_SC_In","P_To_Reg",\
                         "V_To_Reg","TotalEnergy","PowerLowAlert","PowerShuttingDown"],
    "VoltageRegulation":["P_To_Reg","V_To_Reg","P_Tot_Out","V_Tot_Out"],
    "PowerMonitor": ["V_PV","E_SC","E_Batt"],
    
    #Logics block
    "Microcontroller":["TotalEnergy","PowerLowAlert","PowerShuttingDown","P_Tot_Out",\
                       "V_Tot_Out","P_Sensors","Data_Sensors","OnState_Sensors",\
                       "P_Indicator","OnState_indicator","OnState_Radio","PositioningRadio",\
                       "RadioMessagePush","RadioMessagePull","NFC"],
    "Sensors":["P_Sensors","Data_Sensors","OnState_Sensors"],
    "Indicator":["P_indicator","OnState_indicator"],
    
    #Radio block
    "CommunicationRadio":["OnState_Radio","RadioMessagePush","RadioMessagePull",\
                          "P_Radio","Message_To_Antenna","Message_From_Antenna"],
    "PositioningAntenna":["PositioningAntenna"],
    "NFC":["NFC"],
    "PositioningRadio":["PositioningRadio","PositioningAntenna","P_Positioning_Radio"],
    "CommunicationAntenna":["Message_To_Antenna","Message_From_Antenna","Message_To_Gateway","Message_From_Gateway"],
    "RadioChannel":["Message_To_Gateway","Message_From_Gateway"],
    
    #Gateway block
    "Gateway":["Message_To_Gateway","Message_From_Gateway","ServiceRequest_From_Gateway","Service_To_Gateway"],
    "Internet":["ServiceRequest_From_Gateway","Service_To_Gateway"],
    
    #Environment block
    "Environment":["Lightness"]
}

CARGOFUN={ #
    #Power block
    "MainSwitch":None,
    "SolarCell":NF_SolarCell,
    "LongTermBattery":NF_Batt,
    "SuperCaps":NF_Supercap,
    "HarvesterCircuits":None,
    "VoltageRegulation":None,
    "PowerMonitor": NF_Monitor,
    
    #Logics block
    "Microcontroller":NF_Monitor,
    "Sensors":NF_Monitor,
    "Indicator":None,
    
    #Radio block
    "CommunicationRadio":None,
    "PositioningAntenna":None,
    "NFC":None,
    "PositioningRadio":None,
    "CommunicationAntenna":None,
    "RadioChannel":None,
    
    #Gateway block
    "Gateway":None,
    "Internet":None,
    
    #Environment block
    "Environment":NF_Environment
}

ARGVALUES={'Data_Sensors': None,
 'E_Batt': 5000.0,
 'E_SC': 0.0,
 'Lightness': 0.0,
 'Message_From_Antenna': "",
 'Message_From_Gateway': "",
 'Message_To_Antenna': "",
 'Message_To_Gateway': "",
 'NFC': None,
 'OnState_Main': False,
 'OnState_Radio': False,
 'OnState_Sensors': False,
 'OnState_indicator': False,
 'P_Batt': 0.0,
 'P_Indicator': 0.0,
 'P_PV_Out': 0.0,
 'P_Positioning_Radio': None,
 'P_Radio': 0.0,
 'P_SC_In': 0.0,
 'P_SC_Out': 0.0,
 'P_SC_Out_Req': 0.0,
 'P_Sensors': 0.0,
 'P_To_Reg': 0.0,
 'P_Tot_Out': 0.02,
 'P_indicator': 0.0,
 'PositioningAntenna': None,
 'PositioningRadio': None,
 'PowerLowAlert': False,
 'PowerShuttingDown': False,
 'RadioMessagePull': "",
 'RadioMessagePush': "",
 'ServiceRequest_From_Gateway': "",
 'Service_To_Gateway': "",
 'TotalEnergy': 0.0,
 'V_Batt': 3.3,
 'V_PV': 0.0,
 'V_SC': 0.0,
 'V_To_Reg': 0.0,
 'V_Tot_Out': 0.0}

rx=800
ry=600

GRAAFI={"Nodes":{},"Edges":[]}
DICTfromCARGOFUN(CARGOFUN, ARGS, ARGVALUES, GRAAFI)
IMAGEStoDICT(IMAGES, GRAAFI)
#GR=GRfromDICT(GRAAFI,rx,ry, colorscheme = "oppositesrnd", color = (128,64,0))
#GR=GRfromDICT(GRAAFI,rx,ry, colorscheme = "colorful", color = (128,64,0))
GR=GRfromDICT(GRAAFI,rx,ry,colorscheme = "random")
#colorBranches(GR,order=5,sat=0.05, inv=True)
GR.bgcolor=(45,11,11)

'''
#USE:
from stickerGR import *
GR.RunThreaded(video=False)
'''