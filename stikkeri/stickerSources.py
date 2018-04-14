from BlockChart import datasource

global BlockSources

######### main, energy, and environment ####
BlockSources ={\
    "MainBus":{\
        "In":[datasource(sourcelabel = "MainBus",sdata={"Self":True})],\
        "Out":[datasource(sourcelabel = "MainBus",sdata={"Self":True})]\
    },\
    "MainMonitor":{\
        "In":[datasource(sourcelabel = "EnvironmentData",sdata={"Lightness":0.0}),\
             datasource(sourcelabel = "PowerBus",sdata={"E_SC":0.0,"V_PV_Out":0.0,"VBatt":3.0})],\
        "Out":[datasource(sourcelabel = "MainBus",sdata={"Monitor":True})]\
    },\
    "PowerBus":{\
        "In":[datasource(sourcelabel = "PowerBus",sdata={"Self":True})],\
        "Out":[datasource(sourcelabel = "PowerBus",sdata={"Self":True})]\
    },\
    "Mains":{\
        "In":[datasource(sourcelabel = "PowerBus",sdata={"Self":True})],\
        "Out":[datasource(sourcelabel = "PowerBus",sdata={"Onstate":False})]\
    },\
    "Solar cell":{\
        "In":[datasource(sourcelabel = "EnvironmentData",sdata={"Lightness":0.0})],\
        "Out":[datasource(sourcelabel = "PowerBus",sdata={"P_PV_Out":0.0,"V_PV_Out":0.0})]\
    },\
    "Long Term Battery":{\
        "In":[datasource(sourcelabel = "EnvironmentData",sdata={"Temperature":10.0})],\
        "Out":[datasource(sourcelabel = "PowerBus",sdata={"VBatt":3.1})]\
    },\
    "Supercaps":{\
        "In":[datasource(sourcelabel = "PowerBus",sdata={"P_SC_Req":0.0,"P_In_SC":0.0,"V_PV_Out":0.0})],\
        "Out":[datasource(sourcelabel = "PowerBus",sdata={"E_SC":0.0,"P_Out_SC":0.0})]\
                },\
    "Harvester circuitry":{\
        "In":[datasource(sourcelabel = "PowerBus",\
                            sdata={\
                                    "V_SC":0.0,"P_Out_SC":0.0,\
                                    "VBatt":3.1,"Onstate":False,\
                                    "P_PV_Out":0.0,"V_PV_Out":0.0\
                                    }),\
               datasource(sourcelabel = "MainBus",\
                            sdata={\
                                    "PeakPowerRequest":False,\
                                   "PowerLowAlert":False,
                                    })],\
        "Out":[datasource(sourcelabel = "PowerBus",\
                            sdata={\
                                    "P_SC_Req":0.0,"P_In_SC":0.0,\
                                   "P_To_Reg":0.0, "V_to_Reg":0.0\
                                    }),
               datasource(sourcelabel = "MainBus",\
                            sdata={\
                                    "PowerCapacity":0.0,"PowerLowAlert":False,\
                                   "PowerShuttingDown":False\
                                    })]\
    },\
        "Voltage regulation":{\
        "In":[datasource(sourcelabel = "PowerBus",sdata={"P_To_Reg":0.0, "V_to_Reg":0.0})],\
        "Out":[datasource(sourcelabel = "PowerBus",sdata={"V_SC":0.0,"P_Out_SC":0.0}),\
               datasource(sourcelabel = "MainBus",sdata={"P_TOT_Out":0.0,"V_TOT_Out":False})]\
    },\
        "Power block":{\
        "In":[datasource(sourcelabel = "PowerBus",sdata={"Block":"PowerBlock"})],\
        "Out":[datasource(sourcelabel = "PowerBus",sdata={"Block":"PowerBlock"})]\
    },\
    "EnvironmentData":{\
        "In":[datasource(sourcelabel = "EnvironmentData",sdata={"Self":True})],\
        "Out":[datasource(sourcelabel = "EnvironmentData",sdata={"Self":True})]\
    },\
        "Environment":{\
        "In":[datasource(sourcelabel = "EnvironmentData",sdata={"Temperature":5.0})],\
        "Out":[datasource(sourcelabel = "EnvironmentData",sdata={"Temperature":5.0,"Lightness":0.0})]\
    },\
        "Environment block":{\
        "In":[datasource(sourcelabel = "EnvironmentData",sdata={"Block":"EnvironmentBlock"})],\
        "Out":[datasource(sourcelabel = "EnvironmentData",sdata={"Block":"EnvironmentBlock"})]\
    }}

############### logics block ################################
BlockSources.update({\
        "SensorBus":{\
            "In":[datasource(sourcelabel = "SensorBus",sdata={"Self":True})],\
            "Out":[datasource(sourcelabel = "SensorBus",sdata={"Self":True})]\
        },\
        "Microcontroller":{\
            "In":[datasource(sourcelabel = "MainBus",sdata={"Self":True}),\
                datasource(sourcelabel = "RadioBus",sdata={"Self":True}),\
                datasource(sourcelabel = "SensorBus",sdata={"Self":True})],\
            "Out":[datasource(sourcelabel = "MainBus",sdata={"Self":True}),\
                datasource(sourcelabel = "RadioBus",sdata={"Self":True}),\
                datasource(sourcelabel = "SensorBus",sdata={"Self":True})]\
        },\
        "Sensors":{\
            "In":[datasource(sourcelabel = "SensorBus",sdata={"Self":True})],\
            "Out":[datasource(sourcelabel = "SensorBus",sdata={"Self":True})]\
        },\
        "Indicator":{\
            "In":[datasource(sourcelabel = "SensorBus",sdata={"Self":True})],\
            "Out":[datasource(sourcelabel = "SensorBus",sdata={"Self":True})]\
        },\
        "Logic block":{\
            "In":[datasource(sourcelabel = "SensorBus",sdata={"Self":True})],\
            "Out":[datasource(sourcelabel = "SensorBus",sdata={"Self":True})]\

    }})

    ############### radio block ################################
BlockSources.update({\
        "RadioBus":{\
            "In":[datasource(sourcelabel = "RadioBus",sdata={"Self":True})],\
            "Out":[datasource(sourcelabel = "RadioBus",sdata={"Self":True})]\
        },\
        "Communication radio":{\
            "In":[datasource(sourcelabel = "RadioBus",sdata={"Self":True}),\
                datasource(sourcelabel = "RadioChannel",sdata={"Self":True})],\
            "Out":[datasource(sourcelabel = "RadioBus",sdata={"Self":True}),\
                datasource(sourcelabel = "RadioChannel",sdata={"Self":True})]\
        },\
        "Antenna":{\
            "In":[datasource(sourcelabel = "RadioBus",sdata={"Self":True})],\
            "Out":[datasource(sourcelabel = "RadioBus",sdata={"Self":True})]\
        },\
        "Positioning radio":{\
            "In":[datasource(sourcelabel = "RadioBus",sdata={"Self":True})],\
            "Out":[datasource(sourcelabel = "RadioBus",sdata={"Self":True})]\
        },\
        "Posit. Antenna":{\
            "In":[datasource(sourcelabel = "RadioBus",sdata={"Self":True})],\
            "Out":[datasource(sourcelabel = "RadioBus",sdata={"Self":True})]\
        },\
        "NFC":{\
            "In":[datasource(sourcelabel = "RadioBus",sdata={"Self":True})],\
            "Out":[datasource(sourcelabel = "RadioBus",sdata={"Self":True})]\
        },\
        "Radio block":{\
            "In":[datasource(sourcelabel = "RadioBus",sdata={"Self":True})],\
            "Out":[datasource(sourcelabel = "RadioBus",sdata={"Self":True})]\
    }})

    ############### Gateway block ################################
BlockSources.update({\
        "RadioChannel":{\
            "In":[datasource(sourcelabel = "RadioChannel",sdata={"Self":True})],\
            "Out":[datasource(sourcelabel = "RadioChannel",sdata={"Self":True})]\
        },\
        "Gateway":{\
            "In":[datasource(sourcelabel = "RadioChannel",sdata={"Self":True})],\
            "Out":[datasource(sourcelabel = "RadioChannel",sdata={"Self":True})]\
        },\
        "Gateway block":{\
            "In":[datasource(sourcelabel = "RadioChannel",sdata={"Self":True})],\
            "Out":[datasource(sourcelabel = "RadioChannel",sdata={"Self":True})]\

    }})
