# This is QuantumENDEC, devloped by ApatheticDELL alongside Aaron and BunnyTub
QuantumENDEC_Version = "QuantumENDEC v5 source"

XMLhistory_Folder = "./history" 
XMLqueue_Folder = "./queue"
Assets_Folder = "./assets" # contains all webserver files (html, css) and audio files for EAS
Tmp_Folder = "./assets/tmp"
Config_File = "./config.json"

QuantumStatus = 0
# 0 = Normal
# 1 = Restart
# 2 = Shutdown

def QEinterrupt():
    global QuantumStatus
    if QuantumStatus != 0: return True
    return False

try: import pythoncom
except: pass

import re
import pyttsx3
import requests
import shutil
import time
import socket
import threading
import json
import os
import argparse
import base64
import subprocess
import importlib
import signal

import sounddevice as sd
from scipy.io import wavfile
from datetime import datetime, timezone, timedelta
from urllib.request import Request, urlopen
from pydub import AudioSegment
from EASGen import EASGen
from EAS2Text import EAS2Text

try:
    import matplotlib
    import matplotlib.pyplot as plt
    #from mpl_toolkits.basemap import Basemap
    from matplotlib.patches import Polygon
    from matplotlib.lines import Line2D
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import cartopy.io.shapereader as shpreader
    MapGenAvil = True
except Exception as e:
    print("Alert map generation will not be available due to an import error: ", e)
    MapGenAvil = False

import smtplib
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import random
import string
import sys
import queue
import wave
import contextlib
import ffmpeg

import soundfile as sf
from scipy.fft import *
import numpy
assert numpy

from flask import Flask, request, jsonify, send_from_directory, redirect, url_for, make_response, session
import hashlib, secrets, logging

CapCatToSameOrg = { "Met": "WXR", "Admin": "EAS", "Other": "CIV", }
SameOrgToCapCat = { "WXR":"Met", "EAS":"Admin", "CIV":"Other" }
CapEventToSameEvent = {
    "911Service": "TOE",
    "accident": "CDW",
    "admin":"ADR",
    "aircraftCras":"LAE",
    "airportClose":"ADR",
    "airQuality":"SPS",
    "airspaceClos":"ADR",
    "amber":"CAE",
    "ambulance":"LAE",
    "animalDang":"CDW",
    "animalDiseas":"CDW",
    "animalFeed":"CEM",
    "animalHealth":"CEM",
    "arcticOut":"SVS",
    "avalanche":"AVW",
    "aviation":"LAE",
    "biological":"BHW",
    "blizzard":"BZW",
    "bloodSupply":"LAE",
    "blowingSnow":"WSW",
    "bridgeClose":"LAE",
    "cable":"ADR",
    "chemical":"CHW",
    "civil":"CEM",
    "civilEmerg":"CEM",
    "civilEvent":"CEM",
    "cold":"SVS",
    "coldWave":"SVS",
    "crime":"CDW",
    "damBreach":"DBW",
    "damOverflow":"DBW",
    "dangerPerson":"CDW",
    "diesel":"LAE",
    "drinkingWate":"CWW",
    "dustStorm":"DSW",
    "earthquake":"EQW",
    "electric":"POS",
    "emergFacil":"CEM",
    "emergSupport":"CEM",
    "explosive":"HMW",
    "facility":"CEM",
    "fallObject":"HMW",
    "fire":"FRW",
    "flashFlood":"FFW",
    "flashFreeze":"FSW",
    "flood":"FLW",
    "fog":"SPS",
    "foodSupply":"LAE",
    "forestFire":"WFW",
    "freezeDrzl":"WSW",
    "freezeRain":"WSW",
    "freezngSpray":"WSW",
    "frost":"SPS",
    "galeWind":"HWW",
    "gasoline":"LAE",
    "geophyiscal":"CEM",
    "hazmat":"BHW",
    "health":"BHW",
    "heat":"SVS",
    "heatHumidity":"SVS",
    "heatingOil":"LAE",
    "heatWave":"SVS",
    "highWater":"SVS",
    "homeCrime":"CEM",
    "hospital":"LAE",
    "hurricane":"HUW",
    "hurricFrcWnd":"HUW",
    "ice":"SPS",
    "iceberg":"IBW",
    "icePressure":"SPS",
    "industCrime":"CEM",
    "industryFire":"IFW",
    "infectious":"DEW",
    "internet":"ADR",
    "lahar":"VOW",
    "landslide":"LSW",
    "lavaFlow":"VOW",
    "magnetStorm":"CDW",
    "marine":"SMW",
    "marineSecure":"SMW",
    "meteor":"CDW",
    "missingPer":"MEP",
    "missingVPer":"MEP",
    "naturalGas":"LAE",
    "nautical":"ADR",
    "notam":"ADR",
    "other":"CEM",
    "overflood":"FLW",
    "plant":"LAE",
    "plantInfect":"LAE",
    "product":"LAE",
    "publicServic":"LAE",
    "pyroclasFlow":"VOW",
    "pyroclaSurge":"VOW",
    "radiological":"RHW",
    "railway":"LAE",
    "rainfall":"SPS",
    "rdCondition":"LAE",
    "reminder":"CEM",
    "rescue":"CEM",
    "retailCrime":"CEM",
    "road":"LAE",
    "roadClose":"ADR",
    "roadDelay":"ADR",
    "roadUsage":"ADR",
    "rpdCloseLead":"ADR",
    "satellite":"ADR",
    "schoolBus":"ADR",
    "schoolClose":"ADR",
    "schoolLock":"CDW",
    "sewer":"LAE",
    "silver":"CEM",
    "snowfall":"WSW",
    "snowSquall":"WSW",
    "spclIce":"SPS",
    "spclMarine":"SMW",
    "squall":"SMW",
    "storm":"SVS",
    "stormFrcWnd":"SVS",
    "stormSurge":"SSW",
    "strongWind":"HWW",
    "telephone":"LAE",
    "temperature":"SPS",
    "terrorism":"CDW",
    "testMessage":"DMO",
    "thunderstorm":"SVR",
    "tornado":"TOR",
    "traffic":"ADR",
    "train":"ADR",
    "transit":"ADR",
    "tropStorm":"TRW",
    "tsunami":"TSW",
    "urbanFire":"FRW",
    "utility":"ADR",
    "vehicleCrime":"CEM",
    "volcanicAsh":"VOW",
    "volcano":"VOW",
    "volunteer":"ADR",
    "waste":"ADR",
    "water":"ADR",
    "waterspout":"SMW",
    "weather":"SPS",
    "wildFire":"FRW",
    "wind":"HWW",
    "windchill":"SPS",
    "winterStorm":"WSW"
}

def CheckFolder(dir, Clear=False):
    if not os.path.exists(dir): os.makedirs(dir)
    else:
        if Clear is True:
            for f in os.listdir(dir): os.remove(os.path.join(dir, f))

def CheckConfigVersion(InputConfig):
    try:
        if InputConfig['version'] == QuantumENDEC_Version: return True
        else: return False
    except: return False

def createDefaultConfig():
    NewConfig = {
        "version": QuantumENDEC_Version,
        "WebserverHost": "0.0.0.0",
        "WebserverPort": "8050",
        "PlayoutNoSAME": False,
        "relay_en": True,
        "relay_fr": False,
        "Force120": False,
        "AttentionTone": "AttnCAN.wav",
        "Attn_BasedOnCountry": False,
        "SAME_callsign": "QUANTUM0",
        "SAME_ORGallowed": [],
        "SAME_EVENTallowed": [],
        "SAME_EVENTblocked": [],
        "SAME_FIPSfilter": [],
        "CGENcolor_warning": "ff2a2a",
        "CGENcolor_watch": "ffcc00",
        "CGENcolor_advisory": "00aa00",
        "CGEN_ClearAfterAlert": False,
        "ProduceImages": False,
        "enable_discord_webhook": False,
        "webhook_author_name": "",
        "webhook_author_URL": "",
        "webhook_author_iconURL": "",
        "webhook_URL": "",
        "webhook_sendAudio": False,
        "enable_email": False,
        "FancyHTML": False,
        "email_server": "",
        "email_server_port": "587",
        "email_user": "",
        "email_user_pass": "",
        "email_sendto": [],
        "enable_LogToTxt": True,
        "UseSpecified_AudioOutput": False,
        "Specified_AudioOutput": "",
        "EnablePassThru": False,
        "UseSpecified_Passthrough_AudioInput": False,
        "Passthrough_AudioInput": "",
        "UseDefaultVoices": True,
        "TTS_Service": "pyttsx3",
        "VoiceEN": "",
        "VoiceFR": "",
        "FliteVoice_EN": "",
        "FliteVoice_FR": "",
        "statusTest": True,
        "statusActual": True,
        "messagetypeAlert": True,
        "messagetypeUpdate": True,
        "messagetypeCancel": True,
        "messagetypeTest": True,
        "severityExtreme": True,
        "severitySevere": True,
        "severityModerate": True,
        "severityMinor": True,
        "severityUnknown": True,
        "urgencyImmediate": True,
        "urgencyExpected": True,
        "urgencyFuture": True,
        "urgencyPast": True,
        "urgencyUnknown": True,
        "AllowedLocations_Geocodes": [],
        "TCP": False,
        "TCP1": "streaming1.naad-adna.pelmorex.com:8080",
        "TCP2": "streaming2.naad-adna.pelmorex.com:8080",
        "HTTP_CAP": False,
        "HTTP_CAP_ADDR": "",
        "HTTP_CAP_ADDR1": "",
        "HTTP_CAP_ADDR2": "",
        "HTTP_CAP_ADDR3": "",
        "HTTP_CAP_ADDR4": "",
        "Enable_NWSCAP": False,
        "NWSCAP_AtomLink": "https://api.weather.gov/alerts/active.atom",
        "SAME-AudioDevice-Monitor": False,
        "SAME_AudioStream_Monitors": False,
        "SAME-AudioStream-Monitor1": "",
        "SAME-AudioStream-Monitor2": "",
        "SAME-AudioStream-Monitor3": "",
        "SAME-AudioStream-Monitor4": ""
    }

    try:
        with open(Config_File, 'w') as json_file: json.dump(NewConfig, json_file, indent=2)
    except: return False
    return True

def DuplicateSAME(ZCZC):
    """Returns True if there is a Duplicate SAME header (if header was already transmitted)"""
    file = f"{Tmp_Folder}/SameHistory.txt"
    try:
        with open(file, "r") as f:
            content = f.read()
            if ZCZC in content: return True
    except:
        with open(file, "a") as f: f.write(f"ZXZX-STARTER-\n")
    with open(file, "a") as f: f.write(f"{ZCZC}\n")
    return False

def Setup():
    CheckFolder(XMLhistory_Folder, True)
    CheckFolder(XMLqueue_Folder, True)
    CheckFolder(Assets_Folder, False)
    CheckFolder(Tmp_Folder, True)
    CheckFolder(f"{Assets_Folder}/stats", True)
    UpdateCGEN("000000", "EMERGENCY ALERT DETAILS", "", False)
    
    if os.path.isfile(f"{Assets_Folder}/alertlog.txt") is True: pass
    else:
        with open(f"{Assets_Folder}/alertlog.txt", "w", encoding='utf-8') as f: f.write("")
        
    with open(f"{Tmp_Folder}/SameHistory.txt", "w") as f: f.write(f"ZXZX-STARTER-\n")

    if os.path.isfile(Config_File) is True:
        with open(Config_File, "r") as JCfile: config = JCfile.read()
        ConfigData = json.loads(config)
        if CheckConfigVersion(ConfigData) is False: print(f"<<ATTENTION!>> Your configuration file is out of date! Go to the web interface and save (overwrite) a new one, or delete the current configuration file ({Config_File}).")
    else:
        if createDefaultConfig() is True: pass
        else: print("Error, failed to create default config file, QuantumENDEC can't run without a config file!"); exit()

    if os.path.isfile(f"./{Assets_Folder}/GeoToCLC.csv") is True: pass
    else: print("The GeoToCLC CSV file is missing, you don't have to worry about this if you're not using Canada's CAP and relaying in S.A.M.E. If you are using Canada's CAP and relaying in S.A.M.E, all CAP-CP alerts will have a 000000 location (FIPS/CLC) code.")

def UpdateStatus(service, content):
    try:
        with open(f"{Assets_Folder}/stats/{service}_status.txt", "w") as f: f.write(content)
    except: pass

def DeconstructSAME(SAMEheader):
    try:
        SAME = SAMEheader.split("+")
        Section1 = SAME[0].split("-", 3)
        Section2 = SAME[1].split("-")
        OrginatorCode = Section1[1]
        EventCode = Section1[2]
        LocationCodes = Section1[3].split("-")
        PurgeTime = Section2[0]
        date = Section2[1][:3]
        hour = Section2[1][3:5]
        minute = Section2[1][5:]
        IssueDate = {"date":date, "hour":hour, "minute":minute}
        Callsign = Section2[2]
        SAMEdata = {
            "OrginatorCode":OrginatorCode,
            "EventCode":EventCode,
            "LocationCodes":LocationCodes,
            "PurgeTime":PurgeTime,
            "Issue":IssueDate,
            "Callsign":Callsign }
        return SAMEdata
    except: return None

def Plugins_Run(mode=None, ZCZC=None, BROADCASTTEXT=None, XML=None):
    """Run modes: startup, beforeRelay, afterRelay"""
    # Execute plugin with: GeneratedHeader, BroadcastText, InfoXML
    pluginFolder = "plugins"
    ZCZC = str(ZCZC).replace("\n","")
    BROADCASTTEXT = str(BROADCASTTEXT).replace("\n"," ")
    XML = str(XML).replace("\n"," ")

    if os.path.exists(pluginFolder) and mode is not None:
        print("Attempting to run plugins...")
        pluginList = os.listdir(pluginFolder)
        for plug in pluginList:
            if ".py" in plug:
                plug = plug.replace(".py", "")
                plug = f"{pluginFolder}.{plug}"
                try:
                    print("Running plugin: ", plug)
                    module = importlib.import_module(plug)
                    if mode == "beforeRelay": module.ExecutePlugin_BeforeRelay(ZCZC, BROADCASTTEXT, XML)
                    elif mode == "afterRelay": module.ExecutePlugin_AfterRelay(ZCZC, BROADCASTTEXT, XML)
                    elif mode == "startup": module.ExecutePlugin_OnStart()
                except Exception as e: print(f"{plug} has failed to run.", e)

def GetAlertLevelColor(ConfigData, ZCZC=None):
    colEvtlist = {
        "AVA": 1,
        "CFA": 1,
        "FFA": 1,
        "FLA": 1,
        "HUA": 1,
        "HWA": 1,
        "SSA": 1,
        "SVA": 1,
        "TOA": 1,
        "TRA": 1,
        "TSA": 1,
        "WSA": 1,
        "DBA": 1,
        "EVA": 1,
        "WFA": 1,
        "AVW": 0,
        "BLU": 0,
        "BZW": 0,
        "CDW": 0,
        "CEM": 0,
        "CFW": 0,
        "DSW": 0,
        "EAN": 0,
        "EQW": 0,
        "EVI": 0,
        "EWW": 0,
        "FFW": 0,
        "FLW": 0,
        "FRW": 0,
        "FSW": 0,
        "FZW": 0,
        "HMW": 0,
        "HUW": 0,
        "HWW": 0,
        "LEW": 0,
        "NUW": 0,
        "RHW": 0,
        "SMW": 0,
        "SPW": 0,
        "SQW": 0,
        "SSW": 0,
        "SVR": 0,
        "TOR": 0,
        "TRW": 0,
        "TSW": 0,
        "VOW": 0,
        "WSW": 0,
        "BHW": 0,
        "BWW": 0,
        "CHW": 0,
        "CWW": 0,
        "DBW": 0,
        "DEW": 0,
        "FCW": 0,
        "IBW": 0,
        "IFW": 0,
        "LSW": 0,
        "WFW": 0,
        "MEP": 0
    }

    if ZCZC is not None:
        try:
            ZCZC = ZCZC.split("-")
            evnt = ZCZC[2]
            if evnt in colEvtlist:
                if colEvtlist[evnt] == 0: embed_color = ConfigData["CGENcolor_warning"]
                elif colEvtlist[evnt] == 1: embed_color = ConfigData["CGENcolor_watch"]
            else: embed_color = ConfigData["CGENcolor_advisory"]
        except: embed_color = ConfigData["CGENcolor_warning"]
    else: embed_color = ConfigData["CGENcolor_warning"]
    return embed_color

def FilterCheck_CAP(InputConfig, AlertInfo):
    # Returns True if passed
    Urgency = re.search(r'<urgency>\s*(.*?)\s*</urgency>', AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
    Severity = re.search(r'<severity>\s*(.*?)\s*</severity>', AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
    
    try:
        current_time = datetime.now(timezone.utc)
        Expires = re.search(r'<expires>\s*(.*?)\s*</expires>', AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
        Expires = datetime.fromisoformat(datetime.fromisoformat(Expires).astimezone(timezone.utc).isoformat())
        if current_time > Expires: Expired = True
        else: Expired = False
    except: Expired = False

    try: Broadcast_Immediately = re.search(r'<valueName>layer:SOREM:1.0:Broadcast_Immediately</valueName>\s*<value>\s*(.*?)\s*</value>', AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
    except: Broadcast_Immediately = "no"
    if "yes" in Broadcast_Immediately.lower(): Broadcast_Immediately = True
    else: Broadcast_Immediately = False

    # To check the 'CAP-CP Geocodes' - not for FIPS/CLC
    if len(InputConfig['AllowedLocations_Geocodes']) == 0: GecodeResult = True
    else:
        GecodeResult = False
        try:
            GeocodeList = re.findall(r'<geocode>\s*<valueName>profile:CAP-CP:Location:0.3</valueName>\s*<value>\s*(.*?)\s*</value>', AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL)
            for i in GeocodeList:
                if i[:2] in InputConfig['AllowedLocations_Geocodes']: GecodeResult = True
                if i[:3] in InputConfig['AllowedLocations_Geocodes']: GecodeResult = True
                if i[:4] in InputConfig['AllowedLocations_Geocodes']: GecodeResult = True
                if i in InputConfig['AllowedLocations_Geocodes']: GecodeResult = True
        except: GecodeResult = True

    try:
        Language = re.search(r'<language>\s*(.*?)\s*</language>', AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
        Language = Language.lower()
        if "fr-ca" in Language: Language = "fr"
        elif "en-ca" in Language or "en-us" in Language: Language = "en"
        else: Language = "NOT_SUPPORTED"
        Language_Result = ConfigData[f"relay_{Language}"]
    except:
        Language_Result = False

    print("<< Filter Check (CAP) >>")
    print("Severity: ", InputConfig[f"severity{Severity}"])
    print("Urgency: ", InputConfig[f"urgency{Urgency}"])
    print("Broadcat Immedately (CAP-CP only): ", Broadcast_Immediately)
    print("Geocode result (CAP-CP only): ", GecodeResult)
    print("Language result: ", Language_Result)
    print("Expired: ", Expired)

    if ((InputConfig[f"severity{Severity}"] and InputConfig[f"urgency{Urgency}"]) or Broadcast_Immediately) and GecodeResult and Language_Result and not Expired: print("Final result: Pass")
    else: print("Final result: Failed... alert will be skipped.")

    return ((InputConfig[f"severity{Severity}"] and InputConfig[f"urgency{Urgency}"]) or Broadcast_Immediately) and GecodeResult and Language_Result and not Expired

def FilterCheck_SAME(ConfigData, ZCZC):
    """Returns True if the filter matches alert"""
    SAME_DICT = DeconstructSAME(ZCZC)
    EVENT = SAME_DICT['EventCode']
    
    if "EAN" in EVENT or "NIC" in EVENT or "NPT" in EVENT or "RMT" in EVENT or "RWT" in EVENT:
        EventAllowed = True
        EventBlocked = False # EventBlocked will be True if an event is blocked
    else:
        if len(ConfigData['SAME_EVENTblocked']) == 0: EventBlocked = False
        else:
            if EVENT in ConfigData['SAME_EVENTblocked']: EventBlocked = True
            else: EventBlocked = False
        
        if len(ConfigData['SAME_EVENTallowed']) == 0: EventAllowed = True
        else:
            if EVENT in ConfigData['SAME_EVENTallowed']: EventAllowed = True
            else: EventAllowed = False

    if len(ConfigData['SAME_ORGallowed']) == 0: OrgiResult = True
    else:
        if SAME_DICT['OrginatorCode'] in ConfigData['SAME_ORGallowed']: OrgiResult = True
        else: OrgiResult = False

    if len(ConfigData['SAME_FIPSfilter']) == 0: LocationResult = True
    else:
        LocationResult = False
        for i in SAME_DICT['LocationCodes']:
            # Partial county wildcard filter
            partial = "*" + i[1:]
            if partial[:2] in ConfigData['SAME_FIPSfilter']: LocationResult = True
            if partial[:3] in ConfigData['SAME_FIPSfilter']: LocationResult = True
            if partial[:4] in ConfigData['SAME_FIPSfilter']: LocationResult = True
            if partial in ConfigData['SAME_FIPSfilter']: LocationResult = True

            if i[:2] in ConfigData['SAME_FIPSfilter']: LocationResult = True
            if i[:3] in ConfigData['SAME_FIPSfilter']: LocationResult = True
            if i[:4] in ConfigData['SAME_FIPSfilter']: LocationResult = True
            if i in ConfigData['SAME_FIPSfilter']: LocationResult = True

    print("<< Filter check (S.A.M.E) >>")
    print("Originator result: ", OrgiResult)
    print("Location code result: ", LocationResult)
    print("Event code allowed: ", EventAllowed)
    print("Event code blocked: ", EventBlocked)

    if (OrgiResult and LocationResult and EventAllowed) and not EventBlocked: print("Final result: pass")
    else: print("Final result: fail... alert will be skipped.")

    return (OrgiResult and LocationResult and EventAllowed) and not EventBlocked

def WatchNotify(ListenFolder, HistoryFolder):
    print(f"Waiting for an alert...")
    while QEinterrupt() is False:
        ExitTicket = False
        QueueList = os.listdir(f"{ListenFolder}")
        for file in QueueList:
            with open(f"{ListenFolder}/{file}", "r", encoding='UTF-8') as f: RelayXML = f.read()
            AlertListXML = re.findall(r'<alert\s*(.*?)\s*</alert>', RelayXML, re.MULTILINE | re.IGNORECASE | re.DOTALL)
            if len(AlertListXML) > 1:
                print("WHY THE F*** IS THERE 2 ALERT ELEMENTS IN A SINGLE XML FILE?!!?")
                AlertCount = 0
                for AlertXML in AlertListXML:
                    AlertCount = AlertCount + 1
                    print("Alert", AlertCount)
                    Sent = re.search(r'<sent>\s*(.*?)\s*</sent>', AlertXML, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1).replace("-", "_").replace("+", "p").replace(":", "_").replace("\n", "")
                    Ident = re.search(r'<identifier>\s*(.*?)\s*</identifier>', AlertXML, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1).replace("-", "_").replace("+", "p").replace(":", "_").replace("\n", "")
                    NAADsFilename = f"{Sent}I{Ident}.xml"
                    AlertXML = f"<alert {AlertXML}</alert>"
                    with open(f"{ListenFolder}/{NAADsFilename}", 'w', encoding='utf-8') as f: f.write(AlertXML)
                os.remove(f"{ListenFolder}/{file}")
            elif file in os.listdir(f"{HistoryFolder}"):
                print("No relay: watch folder files matched.")
                os.remove(f"{ListenFolder}/{file}")
                ExitTicket = False
            else:
                ExitTicket = True
                break
        if ExitTicket is True: break
        else: time.sleep(1) # Wait a little bit between looking for new files
    if QEinterrupt() is False: return file

def Heartbeat(References, QueueFolder, HistoryFolder):
    print("Downloading (Pelmorex NAADs) alerts from received heartbeat...")
    RefList = References.split(" ")
    for i in RefList:
        j = re.sub(r'^.*?,', '', i)
        j = j.split(",")
        sent = j[1]
        sentDT = sent.split("T", 1)[0]
        sent = sent.replace("-","_").replace("+", "p").replace(":","_")
        identifier = j[0]
        identifier = identifier.replace("-","_").replace("+", "p").replace(":","_")
        Dom1 = 'capcp1.naad-adna.pelmorex.com'
        Dom2 = 'capcp2.naad-adna.pelmorex.com'
        Output = f"{QueueFolder}/{sent}I{identifier}.xml"
        if f"{sent}I{identifier}.xml" in os.listdir(f"{HistoryFolder}"):
            print("Heartbeat, no download: Files matched.")
        else:
            print(f"Downloading: {sent}I{identifier}.xml...")
            req1 = Request(url = f'http://{Dom1}/{sentDT}/{sent}I{identifier}.xml', headers={'User-Agent': 'Mozilla/5.0'})
            req2 = Request(url = f'http://{Dom2}/{sentDT}/{sent}I{identifier}.xml', headers={'User-Agent': 'Mozilla/5.0'})
            try: xml = urlopen(req1).read()
            except:
                try: xml = urlopen(req2).read()
                except: pass
            try:
                with open(Output, "wb") as f: f.write(xml)
            except: print("Heartbeat, download aborted: a general exception occurred, it could be that the URLs are temporarily unavailable.")

def UpdateCGEN(color="000000", headline="", text="", stat=True):
    try:
        CGEN_Dict = { "color": color, "headline": headline, "text": text, "alertStat": stat }
        with open(f"{Assets_Folder}/AlertText.json", 'w') as json_file: json.dump(CGEN_Dict, json_file, indent=2)
    except: pass

def ConvertAudioFormat(inputAudio, outputAudio):
    result = subprocess.run(["ffmpeg", "-y", "-i", inputAudio, outputAudio], capture_output=True, text=True)
    if result.returncode == 0: print(f"{inputAudio} --> {outputAudio} ... Conversion successful!")
    else: print(f"{inputAudio} --> {outputAudio} ... Conversion failed: {result.stderr}")

def LoudenAudio(inputAudio, outputAudio):
    result = subprocess.run(["ffmpeg", "-y", "-i", inputAudio, "-filter:a", "volume=2.5", outputAudio], capture_output=True, text=True)
    if result.returncode == 0: print(f"Filter loudening success.")
    else: print(f"Filter loudening failure: {result.stderr}")

def GenerateTTS(Output, InputConfig=None, InputText=None, Language="EN"):
    # This function will generate TTS and output it to an audio file.
    try: os.remove(Output)
    except: pass
    try: pythoncom.CoInitialize()
    except: pass

    if InputConfig["TTS_Service"] == "pyttsx3":
        engine = pyttsx3.init()
        if InputConfig["UseDefaultVoices"] is False:
            if Language == "FR": ActiveVoice = InputConfig["VoiceFR"]
            else: ActiveVoice = InputConfig["VoiceEN"]
            voices = engine.getProperty('voices')
            ActiveVoice = next((voice for voice in voices if voice.name == ActiveVoice), None)
            if ActiveVoice: engine.setProperty('voice', ActiveVoice.id)
        engine.save_to_file(str(InputText), Output)
        engine.runAndWait()

    # i don't like the execution of this... maybe let the end user just setup a custom TTS in plugins!
    elif InputConfig["TTS_Service"] == "flite":
        InputText = InputText.replace("\n", " ")
        
        if InputConfig["UseDefaultVoices"] is False:
            if Language == "FR": ActiveVoice = InputConfig["FliteVoice_FR"]
            else: ActiveVoice = InputConfig["FliteVoice_EN"]
            subprocess.run(["flite", "-t", InputText, "-voice", ActiveVoice, "-o", Output], capture_output=True, text=True)
        
        else: subprocess.run(["flite", "-t", InputText, "-o", Output], capture_output=True, text=True)

def EventSuffix(EventIn):
    target_words = {"test", "watch", "warning", "alert", "emergency", "notification"}
    words = EventIn.split()
    if words:
        last_word = words[-1].lower()
        return last_word in target_words
    return False

def TrimAudio(input_file, max_duration_ms=120000):
    # For broadcast audio
    output_file = input_file + ".trimmed"
    audio = AudioSegment.from_file(input_file)
    duration_ms = len(audio)
    if duration_ms > max_duration_ms:
        trimmed_audio = audio[:max_duration_ms]
        trimmed_audio.export(output_file, format="wav")
        print(f"Broadcast Audio trimmed to {max_duration_ms / 1000} seconds.")
        shutil.move(output_file, input_file)
    else: pass

# Actual, Update, Cancel, Test
MsgTypeConv = {
    "EN":{ "Alert":"has issued", "Update":"has updated", "Cancel":"has ended", "Test":"has issued" },
    "FR":{ "Alert":"a émis", "Update":"a mis à jour", "Cancel":"est terminé", "Test":"a émis" }
}

def GeoToCLC(InfoXML):
    GeocodeList = re.findall(r'<geocode>\s*<valueName>profile:CAP-CP:Location:0.3</valueName>\s*<value>\s*(.*?)\s*</value>', InfoXML, re.MULTILINE | re.IGNORECASE | re.DOTALL)
    filepath = f"{Assets_Folder}/GeoToCLC.csv"
    SameDict = {}

    try:
        with open(filepath) as fp:
            line = fp.readline()
            cnt = 1
            while line:
                line = line.replace('\n', '')
                SAMESPLIT = line.split(",")
                SameDict[SAMESPLIT[0]] = SAMESPLIT[1]
                line = fp.readline()
                cnt += 1
    except: return "000000"

    CLC = ""
    for i in GeocodeList:
        try: C = SameDict[i]
        except: C = ""
        if C == "": pass
        else: CLC = f"{CLC}" + f"{C},"
    
    # Aaron i know you're kinda gonna cringe at this, but we need it
    CLC = "".join(CLC.rsplit(",",1))
    CLC = CLC.split(",")
    CLC = "-".join(CLC)
    CLC = CLC.split("-")
    CLC = list(set(CLC))
    CLC = "-".join(CLC)
    return CLC

def GetMedia(InputSource, OutputAudio, DecodeType):
    if DecodeType == 1:
        print("Decoding media from BASE64...")
        with open(OutputAudio, "wb") as fh: fh.write(base64.decodebytes(InputSource))
    elif DecodeType == 0:
        print("Downloading media...")
        r = requests.get(InputSource)
        with open(OutputAudio, 'wb') as f: f.write(r.content)

def GetAlertRegion(XML):
    # Get the alert region of CAP XML
    try:
        CODE = re.findall(r'<code>\s*(.*?)\s*</code>', XML, re.MULTILINE | re.IGNORECASE | re.DOTALL)
        if "profile:CAP-CP:0.4" in str(CODE): CODE = "CANADA"
        elif "IPAWSv1.0" in str(CODE): CODE = "USA"
        else: CODE = None
        return CODE
    except: return None

def CreateSAMEmonitorXML(SAME, audioInput, monitorName):
    try:
        SAME = SAME.replace("\n", "")
        oof = EAS2Text(SAME)
        
        sent = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S-00:00')
        sent_rp = sent.replace("-","").replace(":","")
        ident_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        ident = f"{sent_rp}{ident_code}"
        output = f"{XMLqueue_Folder}/{monitorName}-{sent_rp}I{ident}.xml"
        current_time = datetime.strptime(sent, "%Y-%m-%dT%H:%M:%S-00:00")
        
        try: hours, minutes = map(int, oof.purge)
        except: hours, minutes = map(int, ['01','30'])
        expiry_time = current_time + timedelta(hours=hours, minutes=minutes)
        expiry_timestamp = expiry_time.strftime("%Y-%m-%dT%H:%M:%S-00:00")
        
        monitorName = monitorName.replace("\n", "")
        try: Cate = SameOrgToCapCat[oof.org]
        except: Cate = "Other"
        FIPs = "-".join(oof.FIPS)

        try:
            with open(audioInput, 'rb') as wav_file: wav_data = wav_file.read()
            encoded_data = base64.b64encode(wav_data).decode('utf-8')
            embedded_audio = f"""
            <resource>
                <resourceDesc>broadcast audio</resourceDesc>
                <mimeType>audio/wave</mimeType>
                <derefUri>{encoded_data}</derefUri>
            </resource>
            """
        except: embedded_audio = ""

        XML = f"""
        <alert>
            <identifier>{ident}</identifier>
            <sender>{monitorName}</sender>
            <sent>{sent}</sent>
            <status>Actual</status>
            <msgType>Alert</msgType>
            <source>QuantumENDEC Internal Monitor</source>
            <scope>Public</scope>
            <info>
                <language>en-US</language>
                <category>{Cate}</category>
                <event>{oof.evntText}</event>
                <responseType>Monitor</responseType>
                <urgency>Immediate</urgency>
                <severity>Extreme</severity>
                <certainty>Observed</certainty>
                <eventCode><valueName>SAME</valueName><value>{oof.evnt}</value></eventCode>
                <effective>{sent}</effective>
                <expires>{expiry_timestamp}</expires>
                <senderName>{oof.orgText}</senderName>
                <headline>{oof.evntText}</headline>
                <description>From {oof.callsign}</description>
                {embedded_audio}
                <parameter><valueName>EAS-ORG</valueName><value>{oof.org}</value></parameter>
                <area><areaDesc>{oof.strFIPS}</areaDesc><geocode><valueName>SAME</valueName><value>{FIPs}</value></geocode></area>
            </info>
        </alert>
        """

        with open(output, "w") as f: f.write(XML)
    except: pass

def GetPlatform():
    if sys.platform == "win32": platform = "win"
    else: platform = "other"
    return platform

def get_len(fname):
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration

def freq(file, start_time, end_time):
    sr, data = wavfile.read(file)
    if data.ndim > 1: data = data[:, 0]
    else: pass
    dataToRead = data[int(start_time * sr / 1000) : int(end_time * sr / 1000) + 1]
    N = len(dataToRead)
    yf = rfft(dataToRead)
    xf = rfftfreq(N, 1 / sr)
    idx = numpy.argmax(numpy.abs(yf)) # Get the most dominant frequency and return it
    freq = xf[idx]
    return freq

def RemoveEOMpATTN(AudioFile):
    try:
        # Remove END (EOMs)
        # audio = AudioSegment.from_file(f"Audio/tmp/{moniName}out.wav")
        audio = AudioSegment.from_file(AudioFile)
        lengthaudio = len(audio)
        start = 0
        threshold = lengthaudio - 1200
        end = 0
        counter = 0
        end += threshold
        chunk = audio[start:end]
        filename = f"{AudioFile}.rmend"
        chunk.export(filename, format="wav")
        counter +=1
        start += threshold
    except: pass
    
    try:
        # Remove attention tone
        timelist = []
        freqlist = []
        ATTNCUT = 0
        file_length = get_len(f"{AudioFile}.rmend")
        if file_length < 23: file_length = round(file_length)
        else: file_length = 80
        cnt = 0
        for e in range(file_length):
            cnt = cnt + 1
            val = 300
            start = e * val
            offset = start + val
            timelist.append(start)
            frequency = freq(f"{AudioFile}.rmend", start, offset)
            freqlist.append(frequency)
        freqlist = list(freqlist)
        mainlen = len(freqlist)
        found = False
        for e in range(len(freqlist)):
            if found == False:
                if 810 < round(int(freqlist[e])) < 1070:
                    if 810 < round(int(freqlist[e + 1])) < 1070 and 810 < round(int(freqlist[e + 2])) < 1070:
                        found = True
            elif found == True:
                if freqlist[e] < 810 or freqlist[e] > 1070:
                    if e + 5 < mainlen:
                        if freqlist[e + 1] < 810 or freqlist[e + 1] > 1070 and freqlist[e + 2] < 810 or freqlist[e + 2] > 1070 and freqlist[e + 3] < 810 or freqlist[e + 3] > 1070 and freqlist[e + 4] < 810 or freqlist[e + 4] > 1070 and freqlist[e + 5] < 810 or freqlist[e + 5] > 1070:
                            end_point = e
                            found = None
        if(found == None): pass
        else:
            gl = round(get_len(f"{AudioFile}.rmend"))
            if(gl > 4): end_point = 17 #5 seconds
            else: end_point = gl // 2
        audio = AudioSegment.from_file(f"{AudioFile}.rmend")
        lengthaudio = len(audio)
        cut = 300 * end_point
        start = cut
        threshold = lengthaudio - cut
        end = lengthaudio
        counter = 0
        shutil.move(AudioFile, f"{AudioFile}.backup")
        while start < len(audio):
            end += threshold
            chunk = audio[start:end]
            chunk.export(AudioFile, format="wav")
            counter +=1
            start += threshold
        os.remove(f"{AudioFile}.backup")
    except Exception as e:
        print("Error in removing the attention tone or EOM header: ", e)
        shutil.move(f"{AudioFile}.backup", AudioFile)

def ZCZC_test(inp):
    inp = inp.split("-")
    num = len(inp) - 6
    if len(inp[num + 3]) != 7: return False
    elif len(inp[num + 4]) != 8: return False
    elif len(inp[0]) != 4: return False #ZCZC
    elif len(inp[1]) != 3: return False #"EAS"
    elif len(inp[2]) != 3: return False #"DMO"
    if num == 1 and len(inp[3]) == 11: return True
    elif num > 1:
        for e in range(num):
            if (e + 1) == num:
                if len(inp[e+3]) == 11: return True
                else: return False
            elif len(inp[e+3]) != 6: return False
    else: return False

class Webserver:
    def __init__(self):
        self.QEWEB_flaskapp = Flask(__name__)
        self.setup_routes()
        self.QEWEB_flaskapp.secret_key = secrets.token_hex(16)
        self.PASSWORD_FILE = './password.json'
        self.SESSION_COOKIE_NAME = 'session_id'
        self.SESSIONS = {}
        self.DEFAULT_PASSWORD_HASH = hashlib.sha256('hackme'.encode()).hexdigest()

    def save_password(self, password_hash):
        with open(self.PASSWORD_FILE, 'w') as file: json.dump({'password': password_hash}, file)

    def get_audio_devices(self):
        devices = sd.query_devices()
        output_devices = [device for device in devices if device['max_output_channels'] > 0]
        return [f"{device['name']}, {sd.query_hostapis()[device['hostapi']]['name']}" for device in output_devices]

    def get_audio_inputs(self):
        devices = sd.query_devices()
        input_devices = [device for device in devices if device['max_input_channels'] > 0]
        return [f"{device['name']}, {sd.query_hostapis()[device['hostapi']]['name']}" for device in input_devices]

    def list_tts_voices(self):
        try:
            try: pythoncom.CoInitialize()
            except: pass
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            return [voice.name for voice in voices]
        except Exception as e: print("[Webserver]: Exception getting the list of TTS voices (pyttsx3): ", e)

    def load_config(self):
        try:
            with open(Config_File, 'r') as file: return json.load(file)
        except FileNotFoundError: return {}

    def save_config(self, config):
        config['version'] = QuantumENDEC_Version
        with open(Config_File, 'w') as file: json.dump(config, file, indent=4)

    # Load the password from a file or use a default
    def load_password(self):
        try:
            with open('password.json', 'r') as file:
                data = json.load(file)
                return data.get('password', self.DEFAULT_PASSWORD_HASH)
        except FileNotFoundError: return self.DEFAULT_PASSWORD_HASH

    # Check if the user is authenticated
    def is_authenticated(self):
        session_id = request.cookies.get(self.SESSION_COOKIE_NAME)
        return session_id in self.SESSIONS

    # Create a new session
    def create_session(self):
        session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        self.SESSIONS[session_id] = True
        return session_id

    def GetActiveAlerts(self):
        try:
            with open(Config_File, "r") as JCfile: config = JCfile.read()
            ConfigData = json.loads(config)
            ActiveAlerts = []
            XMLhistory = os.listdir(XMLhistory_Folder)
            current_time = datetime.now(timezone.utc)
            for i in XMLhistory:
                try:
                    with open(f"{XMLhistory_Folder}/{i}", "r", encoding='utf-8') as f: XML = f.read()
                    Sent = re.search(r'<sent>\s*(.*?)\s*</sent>', XML, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                    MessageType = re.search(r'<msgType>\s*(.*?)\s*</msgType>', XML, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                    Status = re.search(r'<status>\s*(.*?)\s*</status>', XML, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                    XML = re.findall(r'<info>\s*(.*?)\s*</info>', XML, re.MULTILINE | re.IGNORECASE | re.DOTALL)
                    InfoProc = 0
                    ExpireProc = 0

                    for InfoEN in XML:
                        InfoProc = InfoProc + 1
                        InfoEN = f"<info>{InfoEN}</info>"
                        try:
                            Expires = datetime.fromisoformat(datetime.fromisoformat(re.search(r'<expires>\s*(.*?)\s*</expires>', InfoEN, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)).astimezone(timezone.utc).isoformat())
                            if current_time > Expires:
                                ExpireProc = ExpireProc + 1
                                continue
                        except:
                            ExpireProc = ExpireProc + 1
                            continue
                        
                        try:
                            if "fr" in re.search(r'<language>\s*(.*?)\s*</language>', InfoEN, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1): lang = "fr"
                            elif "es" in re.search(r'<language>\s*(.*?)\s*</language>', InfoEN, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1): lang = "es"
                            else: lang = "en"
                        except: lang = "en"
                        try:
                            if ConfigData[f'relay_{lang}'] is False: continue
                        except: continue

                        Urgency = re.search(r'<urgency>\s*(.*?)\s*</urgency>', InfoEN, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                        Severity = re.search(r'<severity>\s*(.*?)\s*</severity>', InfoEN, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                        Sent = Sent.replace("T"," ")
                        expire = re.search(r'<expires>\s*(.*?)\s*</expires>', InfoEN, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1).replace("T"," ") 
                        senderName = re.search(r'<senderName>\s*(.*?)\s*</senderName>', InfoEN, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                        Description = re.search(r'<description>\s*(.*?)\s*</description>', InfoEN, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                        event = re.search(r'<event>\s*(.*?)\s*</event>', InfoEN, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                        if Description == "###": continue
                        ActiveAlerts.append(f"CAP from {senderName}\n Sent: {Sent}\n Expires: {expire}\n{Status}, {MessageType}\n {Urgency}, {Severity}\n Event: {event}\n\n {Description}")
                    if InfoProc == ExpireProc:
                        try: os.remove(f"{XMLhistory_Folder}/{i}")
                        except: pass
                except: continue
            return ActiveAlerts
        except: return []

    # ... FLASK THINGS ...
    def setup_routes(self):
        @self.QEWEB_flaskapp.route('/activeAlerts')
        def activeAlerts():
            try:
                ActiveAlerts = self.GetActiveAlerts()
                if not ActiveAlerts: return jsonify(["No alerts"])
                return jsonify(ActiveAlerts)
            except: return jsonify(["Error fetching alerts"])

        @self.QEWEB_flaskapp.route('/config')
        def config_page():
            if not self.is_authenticated(): return redirect(url_for('login_page'))
            return send_from_directory(Assets_Folder, 'config.html')

        @self.QEWEB_flaskapp.route('/audio_devices')
        def audio_devices():
            if not self.is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
            devices = self.get_audio_devices()
            return jsonify(devices)

        @self.QEWEB_flaskapp.route('/audio_inputs')
        def audio_inputs():
            if not self.is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
            devices = self.get_audio_inputs()
            return jsonify(devices)

        @self.QEWEB_flaskapp.route('/tts_voices')
        def tts_voices():
            if not self.is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
            voices = self.list_tts_voices()
            return jsonify(voices)

        @self.QEWEB_flaskapp.route('/config_data')
        def config_data():
            if not self.is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
            config = self.load_config()
            return jsonify(config)

        @self.QEWEB_flaskapp.route('/save_config', methods=['POST'])
        def save_config_data():
            if not self.is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
            config = request.json
            self.save_config(config)
            return 'Configuration saved successfully.', 200

        @self.QEWEB_flaskapp.route('/change_password', methods=['POST'])
        def change_password():
            if not self.is_authenticated(): return 'Unauthorized.', 401
            data = request.get_json()
            current_password_hash = hashlib.sha256(data['currentPassword'].encode()).hexdigest()
            new_password_hash = hashlib.sha256(data['newPassword'].encode()).hexdigest()
            if current_password_hash == self.load_password():
                self.save_password(new_password_hash)
                self.SESSIONS.clear() # Clear all sessions
                return 'Password changed successfully.', 200
            else: return 'Incorrect current password.', 403

        @self.QEWEB_flaskapp.route('/login', methods=['GET', 'POST'])
        def login_page():
            if request.method == 'POST':
                data = request.json
                password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
                if password_hash == self.load_password():
                    session_id = self.create_session()
                    response = make_response('Login successful.')
                    response.set_cookie(self.SESSION_COOKIE_NAME, session_id, httponly=True, samesite='Lax')
                    return response
                else: return 'Incorrect password.', 403
            return send_from_directory(Assets_Folder, 'login.html')
            #return send_from_directory('', 'login.html')

        @self.QEWEB_flaskapp.route('/logout', methods=['POST'])
        def logout():
            session.clear()  # Clear all session data
            response = make_response(redirect('/login.html')) # Create a response object
            response.set_cookie(self.SESSION_COOKIE_NAME, '', expires=0) # Remove the session cookie
            return response

        @self.QEWEB_flaskapp.route('/clearAlertLogTxt', methods=['POST'])
        def clearAlertlogTxt():
            try:
                with open(f"{Assets_Folder}/alertlog.txt", "w") as f: f.write("")
            except: pass
            response = make_response(redirect('/alertLog.html'))
            return response

        @self.QEWEB_flaskapp.route('/send_alert', methods=['POST'])
        def send_alert():
            data = request.json
            nowTime = datetime.now(timezone.utc)
            sent = nowTime.strftime('%Y-%m-%dT%H:%M:%S-00:00')
            expire = nowTime + timedelta(hours=1)
            expire = expire.strftime('%Y-%m-%dT%H:%M:%S-00:00')
            sentforres = nowTime.strftime('%Y%m%dT%H%M%S')
            res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            res = f"{res}{sentforres}"

            try: Cate = SameOrgToCapCat[data['ORG']]
            except: Cate = "Other"

            EVENT = data['EVE']
            EVENT = EVENT.upper()
            EVENT = EVENT[:3]

            if data['SecondaryInfo'] is True:
                try: Cate_second = SameOrgToCapCat[data['ORG_second']]
                except: Cate_second = "Other"
                EVENT_second = data['EVE_second']
                EVENT_second = EVENT_second.upper()
                EVENT_second = EVENT_second[:3]
                secondInfo = f"""
                <info>
                    <language>{data['LANGUAGE_second']}</language>
                    <category>{Cate_second}</category>
                    <event>internal</event>
                    <urgency>Unknown</urgency>
                    <severity>Unknown</severity>
                    <certainty>Unknown</certainty>
                    <effective>{sent}</effective>
                    <expires>{expire}</expires>
                    <eventCode><valueName>SAME</valueName><value>{EVENT_second}</value></eventCode>
                    <senderName>QuantumENDEC Internal</senderName>
                    <headline>{EVENT_second}</headline>
                    <description>{data['broadcastText_second']}</description>
                    <parameter><valueName>layer:SOREM:1.0:Broadcast_Text</valueName><value>{data['broadcastText_second']}</value></parameter>
                    <parameter><valueName>EAS-ORG</valueName><value>{data['ORG_second']}</value></parameter>
                    <area><areaDesc>Specified locations</areaDesc><geocode><valueName>SAME</valueName><value>{data['FIPS_second']}</value></geocode></area>
                </info>
                """
            else: secondInfo = ""

            finalXML = f"""
            <alert>
                <identifier>{res}</identifier>
                <sender>QuantumENDEC Internal</sender>
                <sent>{sent}</sent>
                <status>Actual</status>
                <msgType>Alert</msgType>
                <source>QuantumENDEC Self Alert Orginator</source>
                <scope>Public</scope>
                <info>
                    <language>{data['LANGUAGE']}</language>
                    <category>{Cate}</category>
                    <event>internal</event>
                    <urgency>Unknown</urgency>
                    <severity>Unknown</severity>
                    <certainty>Unknown</certainty>
                    <effective>{sent}</effective>
                    <expires>{expire}</expires>
                    <eventCode><valueName>SAME</valueName><value>{EVENT}</value></eventCode>
                    <senderName>QuantumENDEC Internal</senderName>
                    <headline>{EVENT}</headline>
                    <description>{data['broadcastText']}</description>
                    <parameter><valueName>layer:SOREM:1.0:Broadcast_Text</valueName><value>{data['broadcastText']}</value></parameter>
                    <parameter><valueName>EAS-ORG</valueName><value>{data['ORG']}</value></parameter>
                    <area><areaDesc>Specified locations</areaDesc><geocode><valueName>SAME</valueName><value>{data['FIPS']}</value></geocode></area>
                </info>
                {secondInfo}
            </alert>
            """

            filenameXML = f"{sent.replace(':', '_')}I{res}.xml"
            print(f"Creating alert: {filenameXML}")
            with open(f"{XMLqueue_Folder}/{filenameXML}", "w", encoding="utf-8") as file: file.write(finalXML)
            return 'Alert XML created successfully.'

        @self.QEWEB_flaskapp.before_request
        def require_login():
            public_paths = ['/login', '/login.html', '/scroll.html', '/alertText', '/fullscreen.html', '/Jstyle.html', '/tmp/alertImage.png', '/fullscreenWimage.html']
            if request.path not in public_paths:
                if not self.is_authenticated(): return redirect(url_for('login'))

        @self.QEWEB_flaskapp.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                data = request.json
                password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
                
                if password_hash == self.load_password():
                    session_id = self.create_session()
                    response = jsonify(message='Login successful.')
                    response.set_cookie(self.SESSION_COOKIE_NAME, session_id, httponly=True)
                    return response
                else: return jsonify(message='Incorrect password.'), 403
            
            return make_response(open('login.html').read()) # Render login page if GET request

        @self.QEWEB_flaskapp.route('/upload_config', methods=['POST'])
        def upload_config():
            if 'file' not in request.files: return jsonify({'error': 'No file part'}), 400
            file = request.files['file']    
            if file.filename == '': return jsonify({'error': 'No selected file'}), 400
            if not file.filename.endswith('.json'): return jsonify({'error': 'Only JSON files are accepted'}), 400
            file.save(Config_File)
            return jsonify({'success': f'File uploaded and saved as {Config_File}'}), 200

        @self.QEWEB_flaskapp.route('/upload_leadin', methods=['POST'])
        def upload_leadin():
            SAVE_PATH = f'{Assets_Folder}/pre.wav'
            if 'file' not in request.files: return jsonify({'error': 'No file part'}), 400
            file = request.files['file']    
            if file.filename == '': return jsonify({'error': 'No selected file'}), 400
            if not file.filename.endswith('.wav'): return jsonify({'error': 'Only wav files are accepted'}), 400
            file.save(SAVE_PATH)
            return jsonify({'success': 'File uploaded and saved'}), 200

        @self.QEWEB_flaskapp.route('/upload_leadout', methods=['POST'])
        def upload_leadout():
            SAVE_PATH = f'{Assets_Folder}/post.wav'
            if 'file' not in request.files: return jsonify({'error': 'No file part'}), 400
            file = request.files['file']    
            if file.filename == '': return jsonify({'error': 'No selected file'}), 400
            if not file.filename.endswith('.wav'): return jsonify({'error': 'Only wav files are accepted'}), 400
            file.save(SAVE_PATH)
            return jsonify({'success': 'File uploaded and saved'}), 200

        @self.QEWEB_flaskapp.route('/remove_Leadin', methods=['POST'])
        def removeLeadin():
            try:
                os.remove(f"{Assets_Folder}/pre.wav")
                return jsonify({'success': 'Lead in audio removed'})
            except: return jsonify({'error': 'Failed to remove Lead in audio'})
            
        @self.QEWEB_flaskapp.route('/remove_Leadout', methods=['POST'])
        def removeLeadout():
            try:
                os.remove(f"{Assets_Folder}/post.wav")
                return jsonify({'success': 'Lead out audio removed'})
            except: return jsonify({'error': 'Failed to remove Lead out audio'})

        @self.QEWEB_flaskapp.route('/alertText')
        def GetAlertText():
            try:
                with open(f"{Assets_Folder}/AlertText.json", "r") as f: alertText = json.load(f)
                return jsonify(alertText)
            except:
                nothingThing = { "nothing":True }
                return jsonify(nothingThing)
            
        @self.QEWEB_flaskapp.route('/version')
        def GetVersion():
            return QuantumENDEC_Version
        
        @self.QEWEB_flaskapp.route('/restart', methods=['GET'])
        def RestartQE():
            global QuantumStatus
            if QuantumStatus == 1:
                return "QuantumENDEC is already in the process of restarting!"

            if QuantumStatus == 2:
                return "QuantumENDEC is already in the process of shutting down!"
            
            if QuantumStatus == 0:
                QuantumStatus = 1
                return "Now restarting QuantumENDEC... Check the status tab for QuantumENDEC's condition. The restart may take a while."
        
        @self.QEWEB_flaskapp.route('/shutdown', methods=['GET'])
        def ShutdownQE():
            global QuantumStatus
            if QuantumStatus == 0:
                QuantumStatus = 2
                return """<!DOCTYPE html><html><head><style>body { background-color: #161616; color: white; font-family: sans-serif; padding: 2em; }</style></head><body><h2>Now shutting down QuantumENDEC...</h2></body></html>"""
            
            if QuantumStatus == 1:
                QuantumStatus = 2
                return """<!DOCTYPE html><html><head><style>body { background-color: #161616; color: white; font-family: sans-serif; padding: 2em; }</style></head><body><h2>QuantumENDEC was already restarting, now shutting down...</h2></body></html>"""
            
            if QuantumStatus == 2:
                return """<!DOCTYPE html><html><head><style>body { background-color: #161616; color: white; font-family: sans-serif; padding: 2em; }</style></head><body><h2>QuantumENDEC is already in the process of shutting down...</h2></body></html>"""
            
            #return """Now shutting down QuantumENDEC..."""

        @self.QEWEB_flaskapp.route('/')
        def home(): return send_from_directory(Assets_Folder, 'index.html')

        @self.QEWEB_flaskapp.after_request
        def add_header(response):
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '-1'
            return response

        @self.QEWEB_flaskapp.route('/<path:path>')
        def static_files(path): return send_from_directory(Assets_Folder, path)

    def StartServer(self, HOST="0.0.0.0", PORT="8050"):
        print("[Webserver]: Starting webserver... ", f"Port: {PORT}")
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
        self.QEWEB_flaskapp.run(host=HOST, port=PORT, debug=False)
        

class Capture:
    def SaveCAP(self, OutputFolder, InputXML, Source=None):
        CapturedSent = re.search(r'<sent>\s*(.*?)\s*</sent>', InputXML, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1).replace("-", "_").replace("+", "p").replace(":", "_")
        CapturedIdent = re.search(r'<identifier>\s*(.*?)\s*</identifier>', InputXML, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1).replace("-", "_").replace("+", "p").replace(":", "_")
        filename = f"{CapturedSent}I{CapturedIdent}.xml"
        with open(f"{OutputFolder}/{filename}", 'w', encoding='utf-8') as file: file.write(InputXML)
        print(f"[Capture]: Captured an XML, and saved it to: {OutputFolder}/{filename} | From: {Source}")

    def realTCPcapture(self, host, port, buffer=1024, delimiter="</alert>", StatName=None):
        print(f"[TCP Capture]: Connecting to: {host} at {port}")
        while QEinterrupt() is False:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.connect((host, int(port)))
                    s.settimeout(100)
                    if StatName is not None: UpdateStatus(StatName, f"Connected to {host}")
                    print(f"[TCP Capture]: Connected to {host}")
                    data_received = ""
                    try:
                        while QEinterrupt() is False:
                            chunk = str(s.recv(buffer), encoding='utf-8', errors='ignore')
                            data_received += chunk
                            if delimiter in chunk:
                                try: self.SaveCAP(XMLqueue_Folder, data_received, host)
                                except: print(f"[TCP Capture]: {StatName}, failed to save XML!")
                                data_received = ""
                    except socket.timeout:
                        print(f"[TCP Capture]: Connection timed out for {host}")
                        if StatName is not None: UpdateStatus(StatName, f"Timed out: {host}")
                except Exception as e:
                    print(f"[TCP Capture]: Something broke when connecting to {host}: {e}")
                    if StatName is not None: UpdateStatus(StatName, f"Connection error to: {host}")
        exit()

    def TCPcapture(self, host, port, buffer=1024, delimiter="</alert>", StatName=None):
        # i hate this, but it results in quicker shutdowns/restarts
        decodeThread = threading.Thread(target=self.realTCPcapture, args=(host, port, buffer, delimiter, StatName))
        decodeThread.daemon = True
        decodeThread.start()
        while QEinterrupt() is False: time.sleep(1) # keep-alive
        exit()


    def HTTPcapture(self, CAP_URL, instance=None):
        if CAP_URL is None or CAP_URL == "": UpdateStatus(f"HTTPCAPcapture{instance}", f"HTTP CAP capture {instance} disabled.")
        else:
            print(f"[HTTP Capture]: HTTP CAP Capture active! {CAP_URL}")
            while QEinterrupt() is False:
                try:
                    UpdateStatus(f"HTTPCAPcapture{instance}", f"HTTP CAP Capture {instance} is active!")
                    ReqCAP = Request(url = f'{CAP_URL}')
                    CAP = urlopen(ReqCAP).read()
                    CAP = CAP.decode('utf-8')
                    CAP = re.findall(r'<alert\s*(.*?)\s*</alert>', CAP, re.MULTILINE | re.IGNORECASE | re.DOTALL)
                    for alert in CAP:
                        alert = f"<alert {alert}</alert>"
                        try: self.SaveCAP(XMLqueue_Folder, alert, CAP_URL)
                        except: print("[Capture]: Failed to save XML!")
                    time.sleep(30)
                except Exception as e:
                    print("[HTTP Capture] Something went wrong.", e)
                    UpdateStatus(f"HTTPCAPcapture{instance}", f"HTTP CAP Capture {instance} error.")
                    time.sleep(30)

    def NWScapture(self, ATOM_LINK):
        # Goddamnit americans, you have to have every single alert source in their own goddamn way!
        # Why can't you use a centerlized TCP server?!!?!
        print("[NWS CAP Capture]: Activating NWS CAP Capture with: ", ATOM_LINK)
        while QEinterrupt() is False:
            UpdateStatus("NWSCAPcapture", "NWS CAP Capture is active.")
            try:
                req1 = Request(url = ATOM_LINK)
                xml = urlopen(req1).read()
                xml = xml.decode('utf-8')
                entries = re.findall(r'<entry>\s*(.*?)\s*</entry>', xml, re.MULTILINE | re.IGNORECASE | re.DOTALL)
                current_time = datetime.now(timezone.utc)
                for entry in entries:
                    try:
                        CAP_LINK = re.search(r'<link\s*rel="alternate"\s*href="\s*(.*?)\s*"/>', entry, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                        expires = re.search(r'<cap:expires>\s*(.*?)\s*</cap:expires>', entry, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                        expires = datetime.fromisoformat(expires).astimezone(timezone.utc).isoformat()
                        expires = datetime.fromisoformat(expires)

                        if current_time > expires: pass #print("expired")
                        else:        
                            last_slash_index = CAP_LINK.rfind('/')
                            if last_slash_index != -1: filename = CAP_LINK[last_slash_index + 1:]
                            else: filename = CAP_LINK 
                            filename = filename.replace("-", "_").replace("+", "p").replace(":", "_").replace("\n", "")
                            filename = filename + ".xml"
                            if filename in os.listdir(f"{XMLhistory_Folder}"): pass #print("already downloaded")
                            elif filename in os.listdir(f"{XMLqueue_Folder}"): pass #print("already downloaded")
                            else:
                                # print(filename, expires)
                                NWSCAP_REQUEST = Request(url = CAP_LINK)
                                NWSCAP_XML = urlopen(NWSCAP_REQUEST).read()
                                NWSCAP_XML = NWSCAP_XML.decode('utf-8')
                                with open(f"{XMLqueue_Folder}/{filename}", "w") as f: f.write(NWSCAP_XML)
                    except: pass
            except Exception as e:
                print("[NWS CAP Capture]: An error occured.", e)
                UpdateStatus("NWSCAPcapture", "An error occured.")
            time.sleep(120) # To put less strain on the network

class Monitor_Stream:
    def __init__(self, monitorName, streamURL):
        self.monitorName = monitorName
        self.streamURL = streamURL
        self.record = False

    def is_stream_online(self):
        try:
            response = requests.get(self.streamURL, stream=True, timeout=10)
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"[{self.monitorName}] Error checking stream URL: {e}")
            return False
    
    def RecordIP(self, ZCZC):
        output_file = f"{Tmp_Folder}/{self.monitorName}-audio.wav"
        try: os.remove(output_file)
        except: pass
        RecordIP = (ffmpeg .input(self.streamURL) .output(output_file, format='wav', ar='8000') .run_async(pipe_stdout=True, pipe_stderr=True))
        seconds = 0
        while QEinterrupt() is False:
            seconds = seconds + 1
            if self.record is False or seconds == 120 or seconds > 120:
                RecordIP.terminate()
                RecordIP.wait()
                print(f"[{self.monitorName}] Stopped Recording Thread")
                RemoveEOMpATTN(output_file)
                CreateSAMEmonitorXML(ZCZC, output_file, self.monitorName)
                UpdateStatus(self.monitorName, f"Alert sent.")
                print(f"[{self.monitorName}]  Alert Sent!\n\n")
                exit()
            time.sleep(1)

    def decodeStream(self):
        try:
            # Command to capture audio from IP stream and pipe it to multimon-ng
            ffmpeg_command = [
                'ffmpeg', 
                '-i', self.streamURL,         # Input stream URL
                '-f', 'wav',              # Output format
                '-ac', '1',              # Number of audio channels (1 for mono)
                '-ar', '22050',          # Audio sample rate
                '-loglevel', 'quiet',    # Suppress ffmpeg output
                '-' ]

            platform = GetPlatform()
            last = None
            self.ffmpeg_process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE)
            if platform == "win": self.source_process = subprocess.Popen(['multimon-ng-WIN32/multimon-ng.exe', '-a', 'EAS', '-q', '-t', 'raw', '-'], stdin=self.ffmpeg_process.stdout, stdout=subprocess.PIPE)
            else: self.source_process = subprocess.Popen(['multimon-ng', '-a', 'EAS', '-q', '-t', 'raw', '-'], stdin=self.ffmpeg_process.stdout, stdout=subprocess.PIPE)
            UpdateStatus(self.monitorName, f"Ready For Alerts, listening to {self.streamURL}")
            print(f"[{self.monitorName}]  Ready For Alerts, listening to {self.streamURL}\n")

            while QEinterrupt() is False:
                line = self.source_process.stdout.readline().decode("utf-8")
                if QEinterrupt() is True: break
                decode = line.replace("b'EAS: ", "").replace("\n'", "").replace("'bEnabled Demodulators: EAS", "").replace('EAS:  ', '').replace('EAS: ', '').replace('Enabled demodulators: EAS', '')
                if "ZCZC-" in decode or "NNNN" in decode: print(f"[{self.monitorName}]  Decoder: {decode}")

                if 'ZCZC-' in str(line):
                    if ZCZC_test(decode) == True:
                        SAME = decode.replace("\n", "")
                        UpdateStatus(self.monitorName, f"Receiving alert...")
                        print(f"[{self.monitorName}] ZCZC Check OK")
                        with open(Config_File, "r") as JCfile: config = JCfile.read()
                        ConfigData = json.loads(config)
                        dateNow = datetime.now().strftime("%B %d, %Y at %H:%M:%S")
                        Logger(ConfigData).SendLog("Emergency Alert Received", f"Receipt: Received on {dateNow} from {self.monitorName}", decode)
                        self.record = True
                        RecordThread = threading.Thread(target = self.RecordIP, args=(decode,))
                        RecordThread.start()
                    else:
                        print(f"[{self.monitorName}] WARNING: ZCZC Check FAILED!")
                        line = "NNNN"
                
                elif 'NNNN' not in str(last):
                    if 'NNNN' in str(line):
                        time.sleep(0.5)
                        self.record = False
                        try: RecordThread.join()
                        except: pass
                        UpdateStatus(self.monitorName, f"Ready For Alerts, listening to {self.streamURL}")
                last = line
        except:
            try:
                self.ffmpeg_process.terminate()
                self.source_process.terminate()
            except: pass
            UpdateStatus(self.monitorName, f"Failure")
            print(f"[{self.monitorName}] Monitor failure.")

    def start(self):
        while QEinterrupt() is False:
            if self.is_stream_online() is False:
                print(f"[{self.monitorName}] Stream URL {self.streamURL} is offline or unreachable.")
                UpdateStatus(self.monitorName, f"Stream URL {self.streamURL} is offline or unreachable.")
                time.sleep(30)
            else:
                try:
                    decodeThread = threading.Thread(target=self.decodeStream)
                    decodeThread.daemon = True
                    decodeThread.start()
                    while QEinterrupt() is False:
                        time.sleep(30)
                        if self.is_stream_online() is False:
                            print(f"[{self.monitorName}] Stream URL {self.streamURL} is offline or unreachable.")
                            UpdateStatus(self.monitorName, f"Stream URL {self.streamURL} is offline or unreachable.")
                            time.sleep(30)
                            break
                        else: pass
                    if QEinterrupt() is True:
                        self.ffmpeg_process.terminate()
                        self.source_process.terminate()
                except:
                    print(f"[{self.monitorName}] Monitor failure.")
                    UpdateStatus(self.monitorName, f"Failure.")
        exit()

class Monitor_Local:
    def __init__(self, monitorName):
        self.monitorName = monitorName
        self.record = False

    def recordAUDIO(self, SAME):
        OutputFile = f"{Tmp_Folder}/{self.monitorName}-audio.wav"
        try: os.remove(OutputFile)
        except: pass
        while QEinterrupt() is False:
            sd.default.reset()
            samplerate = 8000
            q = queue.Queue()

            def callback(indata, frames, time, status):
                if status: print(status, file=sys.stderr)
                q.put(indata.copy())

            with sf.SoundFile(OutputFile, mode='x', samplerate=samplerate,channels=2) as file:
                with sd.InputStream(samplerate=samplerate,channels=2,callback=callback):
                    print(f"[{self.monitorName}] Recording!")
                    last_check_time = time.time()
                    while QEinterrupt() is False:
                        file.write(q.get())
                        current_time = time.time()
                        if self.record is False or current_time - last_check_time > 120:
                            file.close()
                            print(f"[{self.monitorName}] Stopped Recording Thread")
                            RemoveEOMpATTN(OutputFile)
                            CreateSAMEmonitorXML(SAME, OutputFile, self.monitorName)
                            UpdateStatus(self.monitorName, f"Alert sent.")
                            print(f"[{self.monitorName}]  Alert Sent!")
                            exit()
        exit()

    def DecodeDev(self):
        while QEinterrupt() is False:
            try:
                platform = GetPlatform()
                last = None
                if platform == "win": self.source_process = subprocess.Popen(["multimon-ng-WIN32/multimon-ng.exe", "-a", "EAS", "-q"], stdout=subprocess.PIPE)
                else: self.source_process = subprocess.Popen(["multimon-ng", "-a", "EAS", "-q"], stdout=subprocess.PIPE)
                UpdateStatus(self.monitorName, f"Ready For Alerts.")
                print(f"[{self.monitorName}]  Ready For Alerts...\n")

                while QEinterrupt() is False:
                    line = self.source_process.stdout.readline().decode("utf-8")
                    if QEinterrupt() is True: break
                    decode = line.replace("b'EAS: ", "").replace("\n'", "").replace("'bEnabled Demodulators: EAS", "").replace('EAS:  ', '').replace('EAS: ', '').replace('Enabled demodulators: EAS', '')
                    if "ZCZC-" in decode or "NNNN" in decode: print(f"[{self.monitorName}]  Decoder: {decode}")

                    if 'ZCZC-' in str(line):
                        if ZCZC_test(decode) == True:
                            SAME = decode.replace("\n", "")
                            UpdateStatus(self.monitorName, f"Receiving alert...")
                            print(f"[{self.monitorName}] ZCZC Check OK")
                            with open(Config_File, "r") as JCfile: config = JCfile.read()
                            ConfigData = json.loads(config)
                            dateNow = datetime.now().strftime("%B %d, %Y at %H:%M:%S")
                            Logger(ConfigData).SendLog("Emergency Alert Received", f"Receipt: Received on {dateNow} from {self.monitorName}", SAME)
                            self.record = True
                            RecordThread = threading.Thread(target = self.recordAUDIO, args=(decode,))
                            RecordThread.start()
                        else:
                            print(f"[{self.monitorName}] WARNING: ZCZC Check FAILED!")
                            line = "NNNN"
                    
                    elif 'NNNN' not in str(last):
                        if 'NNNN' in str(line):
                            self.record = False
                            try: RecordThread.join()
                            except: pass
                            UpdateStatus(self.monitorName, f"Ready For Alerts.")
                    last = line
            except Exception as e:
                UpdateStatus(self.monitorName, f"Failure")
                print(f"[{self.monitorName}] Monitor failure.", e)
                time.sleep(5)
        exit()
    
    def start(self):
        try:
            decodeThread = threading.Thread(target=self.DecodeDev)
            decodeThread.daemon = True
            decodeThread.start()
            while QEinterrupt() is False: time.sleep(1) # keep-alive
            self.source_process.terminate()
            exit()
        except:
            print(f"[{self.monitorName}] Monitor failure.")
            UpdateStatus(self.monitorName, f"Failure.")

class AIOMG:
    # A.I.O.M.G: Alert Image Or Map Generator
    def __init__(self) -> None:
        self.ImageOutput = f"{Tmp_Folder}/alertImage.png"

    def overlay_polygon(self, ax, lats, lons, label='', color='red'):
        ax.plot(lons, lats, color=color, linewidth=2, linestyle='-', label=label, transform=ccrs.PlateCarree())

    def fill_polygon(self, ax, lats, lons, color='red', alpha=0.5):
        polygon = Polygon(list(zip(lons, lats)), facecolor=color, alpha=alpha, transform=ccrs.PlateCarree())
        ax.add_patch(polygon)

    def calculate_bounding_box(self, coordinates):
        min_lat = min(lat for lat, _ in coordinates)
        max_lat = max(lat for lat, _ in coordinates)
        min_lon = min(lon for _, lon in coordinates)
        max_lon = max(lon for _, lon in coordinates)
        return min_lat, max_lat, min_lon, max_lon

    def GenerateMapImage(self, InfoXML, PolyColor="#FF0000"):
        matplotlib.use('Agg')
        if "#" not in PolyColor: PolyColor = "#" + PolyColor
        if len(PolyColor) > 7: PolyColor = "#FF0000"
        for char in PolyColor:
            if 'G' <= char <= 'Z' or 'g' <= char <= 'z': PolyColor = "#FF0000"

        try:
            HEADLINE = re.search(r'<headline>\s*(.*?)\s*</headline>', InfoXML, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)  # Get alert title
        except:
            HEADLINE = "Alert region"
        
        AllCoords = re.findall(r'<polygon>\s*(.*?)\s*</polygon>', InfoXML, re.MULTILINE | re.IGNORECASE | re.DOTALL)  # Get all polygons
        
        # Generate map
        coordinates_string = ""
        for i in AllCoords:
            coordinates_string += f" {i}"
        polygon_coordinates = [list(map(float, item.split(','))) for item in coordinates_string.split()]
        min_lat, max_lat, min_lon, max_lon = self.calculate_bounding_box(polygon_coordinates)

        lat_center = (min_lat + max_lat) / 2
        lon_center = (min_lon + max_lon) / 2
        lat_range = max_lat - min_lat
        lon_range = max_lon - min_lon

        if lat_range > lon_range:
            lon_range = lat_range
        else:
            lat_range = lon_range

        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection=ccrs.PlateCarree())

        # Set map extent
        ax.set_extent([
            lon_center - 1.1 * lon_range, lon_center + 1.1 * lon_range,
            lat_center - 1.1 * lat_range, lat_center + 1.1 * lat_range
        ])

        # Add map features
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        ax.add_feature(cfeature.STATES, linestyle='--')
        ax.add_feature(cfeature.LAND, facecolor='#00AA44')
        ax.add_feature(cfeature.OCEAN, facecolor='#002255')
        ax.add_feature(cfeature.LAKES, facecolor='#002255')

        if os.path.exists("./map_addons/counties/ne_10m_admin_2_counties.shp"):
            print("counties shapefile detected")
            countines = cfeature.ShapelyFeature(
                shpreader.Reader("./map_addons/counties/ne_10m_admin_2_counties.shp").geometries(),
                ccrs.PlateCarree(),
                facecolor='none', edgecolor='black' )
            ax.add_feature(countines)

        if os.path.exists("./map_addons/roads/ne_10m_roads.shp"):
            print("roads shapefile detected")
            roads = cfeature.ShapelyFeature(
                shpreader.Reader("./map_addons/roads/ne_10m_roads.shp").geometries(),
                ccrs.PlateCarree(),
                facecolor='none', edgecolor='white' )
            ax.add_feature(roads)

        # Draw polygons
        for i in AllCoords:
            i = [list(map(float, item.split(','))) for item in i.split()]
            lats, lons = zip(*i)
            self.fill_polygon(ax, lats, lons, color=PolyColor, alpha=0.6)
            self.overlay_polygon(ax, lats, lons, label=HEADLINE, color=PolyColor)  # For outlined polygon

        if os.path.exists("./map_addons/populations/ne_10m_populated_places.shp"):
            print("population shapefiles detected")
            label_field = "NAME"
            color = "black"
            reader = shpreader.Reader("./map_addons/populations/ne_10m_populated_places.shp")
            
            # Function to check if a point is within the bounding box
            def is_within_bbox(x, y, bbox):
                min_lon, max_lon, min_lat, max_lat = bbox
                return min_lon <= x <= max_lon and min_lat <= y <= max_lat

            for record in reader.records():
                geometry = record.geometry
                if geometry.geom_type == "Point":
                    # Check if the point is within the bounding box
                    if is_within_bbox(geometry.x, geometry.y, (min_lon, max_lon, min_lat, max_lat)):
                        # Plot the point
                        ax.plot(geometry.x, geometry.y, 'o', color=color, transform=ccrs.PlateCarree())
                        
                        # Add label (if available)
                        label = record.attributes.get(label_field, "Unknown")
                        ax.text(geometry.x, (geometry.y + 0.05), label, fontsize=8, color=color, transform=ccrs.PlateCarree())

        ax.set_aspect('auto')
        legend_patch = Line2D([0], [0], marker='o', color='w', markerfacecolor=PolyColor, markersize=10, label=HEADLINE)
        plt.legend(handles=[legend_patch], loc='upper right')

        fig.savefig(self.ImageOutput, bbox_inches='tight', pad_inches=0.0, dpi=70)

    def ConvertImageFormat(self, inputAudio, outputAudio):
        result = subprocess.run(["ffmpeg", "-y", "-i", inputAudio, "-vf", "scale=-1:450", outputAudio], capture_output=True, text=True)
        if result.returncode == 0: print(f"{inputAudio} --> {outputAudio} ... Conversion successful!")
        else: print(f"{inputAudio} --> {outputAudio} ... Conversion failed: {result.stderr}")

    def GrabImage(self, InfoXML):
        resources = re.findall(r'<resource>\s*(.*?)\s*</resource>', InfoXML, re.MULTILINE | re.IGNORECASE | re.DOTALL)
        if "image/jpeg" in str(resources): pass
        elif "image/png" in str(resources): pass
        else: return False

        try:
            for ImageResource in resources:
                if "<derefUri>" in ImageResource:
                    ImageLink = bytes(re.search(r'<derefUri>\s*(.*?)\s*</derefUri>', ImageResource, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1), 'utf-8')
                    ImageType = re.search(r'<mimeType>\s*(.*?)\s*</mimeType>', ImageResource, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                    Decode = 1
                else:
                    ImageLink = re.search(r'<uri>\s*(.*?)\s*</uri>', ImageResource, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                    ImageType = re.search(r'<mimeType>\s*(.*?)\s*</mimeType>', ImageResource, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                    Decode = 0
                
                if ImageType == "image/jpeg":
                    GetMedia(ImageLink,f"{Tmp_Folder}/PreImage.jpg",Decode)
                    self.ConvertImageFormat(f"{Tmp_Folder}/PreImage.jpg", self.ImageOutput)
                    os.remove(f"{Tmp_Folder}/PreImage.jpg")
                    ImageGet = True
                elif ImageType == "image/png":
                    GetMedia(ImageLink,self.ImageOutput,Decode)
                    ImageGet = True
            
            if ImageGet is True: return True
            else: return False
        except: return False

    def OutputAlertImage(self, InfoXML=None, InputColor="#FF0000", Fallback=False, SkipMap=False):
        if Fallback is True or InfoXML is None: shutil.copy(f"{Assets_Folder}/fallbackImage.png", self.ImageOutput)
        else:
            try:
                global MapGenAvil
                print("[AIOMG]: Generating image...")
                if self.GrabImage(InfoXML) is True: pass
                elif MapGenAvil is True or SkipMap is True: self.GenerateMapImage(InfoXML, InputColor)
                else:
                    print("[AIOMG]: Alert map generation is not available or is set to skip.")
                    shutil.copy(f"{Assets_Folder}/fallbackImage.png", self.ImageOutput)
                
                print("[AIOMG]: Image generation finished")
            except Exception as e:
                print("[AIOMG]: Image generation failure: ", e)
                shutil.copy(f"{Assets_Folder}/fallbackImage.png", self.ImageOutput)

class Generate:
    def __init__(self, ConfigData, InfoXML, MessageType=None, InputSentISO=None):
        self.Config = ConfigData
        self.AlertInfo = InfoXML
        self.MessageType = MessageType
        self.InputSentISO = InputSentISO
        Language = re.search(r'<language>\s*(.*?)\s*</language>', self.AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
        if "en-ca" in Language or "en-us" in Language or "en" in Language: self.Language = "EN"
        elif "fr-ca" in Language or "fr" in Language: self.Language = "FR"
        else: self.Language = "NOT_SUPPORTED"

    def BroadcastText(self):
        try: BroadcastText = re.search(r'<valueName>layer:SOREM:1.0:Broadcast_Text</valueName>\s*<value>\s*(.*?)\s*</value>', self.AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1).replace('\n',' ').replace('  ',' ')
        except:
            try: MsgPrefix = MsgTypeConv[self.Language][self.MessageType]
            except: MsgPrefix = "has issued"
            
            if self.InputSentISO is not None:
                Sent = datetime.fromisoformat(datetime.fromisoformat(self.InputSentISO).astimezone(timezone.utc).isoformat())
                Sent = Sent.astimezone()
                if self.Language == "FR": Sent = Sent.strftime("À %Hh%M. ")
                else: Sent = Sent.strftime("At %H:%M %Z, %B %d, %Y. ")
            else: Sent = ""
            
            try: EventType = re.search(r'<valueName>layer:EC-MSC-SMC:1.0:Alert_Name</valueName>\s*<value>\s*(.*?)\s*</value>', self.AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
            except:
                if self.Language == "FR":
                    EventType = re.search(r'<event>\s*(.*?)\s*</event>', self.AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                    EventType = f"alerte {EventType}"
                else:
                    EventType = re.search(r'<event>\s*(.*?)\s*</event>', self.AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                    if EventSuffix(EventType) is True: pass
                    else: EventType = f"{EventType} alert"
            
            try:
                Coverage = re.search(r'<valueName>layer:EC-MSC-SMC:1.0:Alert_Coverage</valueName>\s*<value>\s*(.*?)\s*</value>', self.AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                if self.Language == "FR": Coverage = f"en {Coverage} pour:"
                else: Coverage = f"in {Coverage} for:"
            except:
                if self.Language == "FR": Coverage = "pour:"
                else: Coverage = "for:" 
            
            try:
                AreaDesc = re.findall(r'<areaDesc>\s*(.*?)\s*</areaDesc>', self.AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL)
                AreaDesc = ', '.join(AreaDesc) + '.'
            except: AreaDesc = "."
            try: SenderName = re.search(r'<senderName>\s*(.*?)\s*</senderName>', self.AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
            except: SenderName = "an alert issuer"
            try: Description = re.search(r'<description>\s*(.*?)\s*</description>', self.AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1).replace('\n', ' ')
            except: Description = ""
            try: Instruction = re.search(r'<instruction>\s*(.*?)\s*</instruction>', self.AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1).replace('\n', ' ')
            except: Instruction = ""
            
            if self.Language == "FR": BroadcastText = f"{Sent}{SenderName} {MsgPrefix} une {EventType} {Coverage} {AreaDesc} {Description} {Instruction}".replace('###','').replace('  ',' ').replace('..','.')
            else: BroadcastText = f"{Sent}{SenderName} {MsgPrefix} a {EventType} {Coverage} {AreaDesc} {Description} {Instruction}".replace('###','').replace('  ',' ').replace('..','.')
        
        return BroadcastText

    def BroadcastAudio(self):
        resources = re.findall(r'<resource>\s*(.*?)\s*</resource>', self.AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL)
        if "audio/mpeg" in str(resources): pass
        elif "audio/x-ms-wma" in str(resources): pass
        elif "audio/wave" in str(resources): pass
        elif "audio/wav" in str(resources): pass
        elif "audio/x-ipaws-audio-mp3" in str(resources): pass
        else: raise Exception("Generate TTS instead")

        for BroadcastAudioResource in resources:
            if "<derefUri>" in BroadcastAudioResource:
                AudioLink = bytes(re.search(r'<derefUri>\s*(.*?)\s*</derefUri>', BroadcastAudioResource, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1), 'utf-8')
                AudioType = re.search(r'<mimeType>\s*(.*?)\s*</mimeType>', BroadcastAudioResource, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                Decode = 1
            else:
                AudioLink = re.search(r'<uri>\s*(.*?)\s*</uri>', BroadcastAudioResource, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                AudioType = re.search(r'<mimeType>\s*(.*?)\s*</mimeType>', BroadcastAudioResource, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                Decode = 0
            
            AudioGet = False
            if AudioType == "audio/mpeg":
                GetMedia(AudioLink,f"{Tmp_Folder}/preaudio.mp3",Decode)
                ConvertAudioFormat(f"{Tmp_Folder}/preaudio.mp3", f"{Tmp_Folder}/preaudio.wav")
                os.remove(f"{Tmp_Folder}/preaudio.mp3")
                AudioGet = True

            elif AudioType == "audio/x-ms-wma":
                GetMedia(AudioLink,f"{Tmp_Folder}/preaudio.wma",Decode)
                ConvertAudioFormat(f"{Tmp_Folder}/preaudio.wma", f"{Tmp_Folder}/preaudio.wav")
                os.remove(f"{Tmp_Folder}/preaudio.wma")
                AudioGet = True

            elif AudioType == "audio/wave":
                GetMedia(AudioLink,f"{Tmp_Folder}/preaudio.wav",Decode)
                AudioGet = True

            elif AudioType == "audio/wav":
                GetMedia(AudioLink,f"{Tmp_Folder}/preaudio.wav",Decode)
                AudioGet = True

            elif AudioType == "audio/x-ipaws-audio-mp3":
                GetMedia(AudioLink,f"{Tmp_Folder}/preaudio.mp3",Decode)
                ConvertAudioFormat(f"{Tmp_Folder}/preaudio.mp3", f"{Tmp_Folder}/preaudio.wav")
                os.remove(f"{Tmp_Folder}/preaudio.mp3")
                AudioGet = True
            else: AudioGet = False

            if AudioGet is True:
                LoudenAudio(f"{Tmp_Folder}/preaudio.wav", "./assets/audio.wav")
                os.remove(f"{Tmp_Folder}/preaudio.wav")

    def HeaderSAME(self):
        CALLSIGN = self.Config['SAME_callsign']
        if len(CALLSIGN) > 8: CALLSIGN = "QUANTUM0"; print("[GENERATE]: Your callsign is too long!")
        elif len(CALLSIGN) < 8: CALLSIGN = "QUANTUM0"; print("[GENERATE]: Your callsign is too short!")
        elif "-" in CALLSIGN: CALLSIGN = "QUANTUM0"; print("[GENERATE]: Your callsign contains an invalid symbol!")

        try: ORG = re.search(r'<parameter>\s*<valueName>EAS-ORG</valueName>\s*<value>\s*(.*?)\s*</value>\s*</parameter>', self.AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
        except:
            try: ORG = CapCatToSameOrg[re.search(r'<category>\s*(.*?)\s*</category>', self.AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)]
            except: ORG = "CIV"
        
        try:
            EVE = re.search(r'<eventCode>\s*<valueName>SAME</valueName>\s*<value>\s*(.*?)\s*</value>', self.AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
            if EVE is None or EVE == "": EVE = "CEM"
        except:
            try:
                EVE = re.search(r'<eventCode>\s*<valueName>profile:CAP-CP:Event:0.4</valueName>\s*<value>\s*(.*?)\s*</value>', self.AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
                EVE = CapEventToSameEvent[EVE]
            except: EVE = "CEM"

        try: Effective = datetime.fromisoformat(datetime.fromisoformat(re.search(r'<effective>\s*(.*?)\s*</effective>', self.AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)).astimezone(timezone.utc).isoformat()).strftime("%j%H%M")
        except: Effective = datetime.now().astimezone(timezone.utc).strftime("%j%H%M")
        
        try:
            NowTime = datetime.now(timezone.utc)
            NowTime = NowTime.replace(microsecond=0).isoformat()
            NowTime = NowTime[:-6]
            NowTime = datetime.fromisoformat(NowTime)
            ExpireTime = re.search(r'<expires>\s*(.*?)\s*</expires>', self.AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
            ExpireTime = datetime.fromisoformat(ExpireTime).astimezone(timezone.utc)
            ExpireTime = ExpireTime.isoformat()
            ExpireTime = ExpireTime[:-6]
            ExpireTime = datetime.fromisoformat(ExpireTime)
            Purge = ExpireTime - NowTime
            hours, remainder = divmod(Purge.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            Purge = "{:02}{:02}".format(hours, minutes)
        except: Purge = "0600"

        if "layer:EC-MSC-SMC:1.1:Newly_Active_Areas" in str(self.AlertInfo):
            try: CLC = re.search(r'<valueName>layer:EC-MSC-SMC:1.1:Newly_Active_Areas</valueName>\s*<value>\s*(.*?)\s*</value>', self.AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1).replace(',','-')
            except: CLC = GeoToCLC(self.AlertInfo)
        else:
            CLC = re.findall(r'<geocode>\s*<valueName>SAME</valueName>\s*<value>\s*(.*?)\s*</value>\s*</geocode>', self.AlertInfo, re.MULTILINE | re.IGNORECASE | re.DOTALL)
            CLC = '-'.join(CLC)
            if str(CLC) == "": CLC = GeoToCLC(self.AlertInfo)
        if CLC == "": CLC = "000000"

        GeneratedHeader = f"ZCZC-{ORG}-{EVE}-{CLC}+{Purge}-{Effective}-{CALLSIGN}-"
        GeneratedHeader = GeneratedHeader.replace("\n", "")
        return GeneratedHeader

    def GenerateTextContent(self):
        BROADCASTTEXT = self.BroadcastText()
        if self.Config["PlayoutNoSAME"] is False: SAME = self.HeaderSAME()
        else: SAME = None
        if self.Language == "FR": HEADLINE = "ALERTE D'URGENCE"
        else: HEADLINE = "EMERGENCY ALERT"
        return { "SAME":SAME, "HEADLINE":HEADLINE, "TEXT":BROADCASTTEXT}
    
    def GenerateAudioVisualContent(self, TextContents, AlertColor="#FF0000"):
        if self.Config['PlayoutNoSAME'] is False:
            print("[GENERATE]: Generating S.A.M.E header...")
            SAMEheader = EASGen.genEAS(header=TextContents['SAME'], attentionTone=False, endOfMessage=False)
            SAMEeom = EASGen.genEAS(header="NNNN", attentionTone=False, endOfMessage=False)
            EASGen.export_wav(f"{Assets_Folder}/same.wav", SAMEheader)
            EASGen.export_wav(f"{Assets_Folder}/eom.wav", SAMEeom)
        
        try: self.BroadcastAudio()
        except: GenerateTTS(f"{Assets_Folder}/audio.wav", self.Config, TextContents['TEXT'], self.Language)

        if self.Config['Force120'] is True:
            try: TrimAudio(f"{Assets_Folder}/audio.wav")
            except: print("[GENERATE]: Failed to trim broadcast audio.")
        
        if self.Config["ProduceImages"] is True: AIOMG().OutputAlertImage(self.AlertInfo, AlertColor, self.Config["SkipMap"])

class Playout:
    def __init__(self, ConfigData, AlertRegion=None):
        self.ZCZC_audio = Assets_Folder + "/same.wav"
        self.EOM_audio = Assets_Folder + "/eom.wav"
        self.broadcast_audio = Assets_Folder + "/audio.wav"
        if ConfigData['Attn_BasedOnCountry'] is True:
            if AlertRegion == "CANADA": self.attention_audio = f"{Assets_Folder}/AttnCAN.wav"
            elif AlertRegion == "USA": self.attention_audio = f"{Assets_Folder}/AttnEBS.wav"
            else: self.attention_audio = f"{Assets_Folder}/{ConfigData['AttentionTone']}"
        else: self.attention_audio = f"{Assets_Folder}/{ConfigData['AttentionTone']}"
        self.ConfigData = ConfigData
        print("[Playout]: Ready for playout!")

    def playout(self, inputFile):
        UseSpecDevice = self.ConfigData['UseSpecified_AudioOutput']
        SpecDevice = self.ConfigData['Specified_AudioOutput']
        time.sleep(0.5)
        if UseSpecDevice is True:
            sd.default.reset()
            sd.default.device = SpecDevice
        sampling_rate, audio_data = wavfile.read(inputFile)
        sd.play(audio_data, samplerate=sampling_rate)
        sd.wait()

    def SAME(self):
        print("[Playout]: Playing S.A.M.E header")
        try: self.playout(self.ZCZC_audio)
        except Exception as e: print("[Playout]: Can't play SAME header! ", e)

    def EOM(self):
        print("[Playout]: Playing EOM header")
        try: self.playout(self.EOM_audio)
        except Exception as e: print("[Playout]: Can't play EOM! ", e)

    def ATTN(self):
        print("[Playout]: Playing attention tone: ", self.attention_audio)
        try: self.playout(self.attention_audio)
        except Exception as e: print("[Playout]: Can't play attention tone! ", e)

    def AUDIO(self):
        print("[Playout]: Playing broadcast audio")
        try: self.playout(self.broadcast_audio)
        except Exception as e: print("[Playout]: Can't play broadcast audio! ", e)

    def LEAD_IN(self):
        try: self.playout(Assets_Folder + "/pre.wav")
        except: pass

    def LEAD_OUT(self):
        try: self.playout(Assets_Folder + "/post.wav")
        except: pass

class Logger:
    def __init__(self, ConfigData):
        self.ConfigData = ConfigData

    def SendDiscord(self, Title, Description, ZCZC, type="", HookColor=None):
        Wauthorname = self.ConfigData['webhook_author_name']
        Wauthorurl = self.ConfigData['webhook_author_URL']
        Wiconurl = self.ConfigData['webhook_author_iconURL']
        Wurl = self.ConfigData['webhook_URL']
        Description = Description.replace("/n", " ")
        if len(Description) > 2000: Description = f"{Description[:2000]}..."
        if len(ZCZC) > 1000: ZCZC = f"{ZCZC[:1000]}..."
        webhook = DiscordWebhook(url=Wurl, rate_limit_retry=True)
        
        # Send audio and image (if enabled)
        if type == "TX":
            if self.ConfigData['webhook_sendAudio'] is True:
                try:
                    subprocess.run(["ffmpeg", "-y", "-i", f"{Assets_Folder}/audio.wav", "-map", "0:a:0", "-b:a", "64k", f"{Tmp_Folder}/DiskAudio.mp3"], capture_output=True, text=True)
                    with open(f"{Tmp_Folder}/DiskAudio.mp3", "rb") as f: webhook.add_file(file=f.read(), filename="audio.mp3")
                except: pass

            if self.ConfigData["ProduceImages"] is True:
                try:
                    with open(f"{Tmp_Folder}/alertImage.png", "rb") as f: webhook.add_file(file=f.read(), filename="image.png")
                except: pass

        if HookColor is None or HookColor == "": Wcolor = "ffffff"
        else: Wcolor = HookColor
        
        embed = DiscordEmbed(title=Title, description=Description, color=Wcolor,)
        if ZCZC == "" or ZCZC is None: pass
        else: 
            ZCZC = f"```{ZCZC}```"
            embed.add_embed_field(name="", value=ZCZC, inline=False)
        embed.set_author(name=Wauthorname, url=Wauthorurl, icon_url=Wiconurl)
        embed.set_footer(text="Powered by QuantumENDEC")
        embed.set_timestamp()
        webhook.add_embed(embed)
        webhook.execute()

    def SendEmail(self, Title, Description, ZCZC, HookColor=None):
        Description = Description.replace("\n", " ")
        ZCZC = ZCZC.replace("\n", "")
        if len(ZCZC) > 1: ZCZC = f"S.A.M.E: {ZCZC}" 
        if HookColor is None or HookColor == "": HookColor = "101010"
        date = datetime.now()
        date = date.astimezone()
        date = date.strftime("Log: %H:%M%z %d/%m/%Y")

        style = """
            <style>
                    body { background-color: #414141; color: white; font-family: Arial, sans-serif; margin: 0; padding: 0; }
                    header { background-color: """ + f"#{HookColor}" + """; padding: 20px; text-align: center; }
                    header h1 { margin: 0; font-size: 2em; }
                    main { padding: 20px; }
                    footer { background-color: """ + f"#{HookColor}" + """; padding: 10px; text-align: center; position: fixed; width: 100%; bottom: 0; }
            </style>
        """

        body = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>QuantumENDEC Email Log</title>
                {style}
            </head>
            <body>
                <header><h1>QuantumENDEC Email Log</h1></header>
                <main>
                    <h2>{Title}</h2>
                    <p>{Description}</p>
                    <p>{ZCZC}</p>
                </main>
                <footer><p>QuantumENDEC - {date}</p></footer>
            </body>
        </html>
        """

        message = MIMEMultipart()
        message["From"] = self.ConfigData["email_user"]
        message["Subject"] = f"QuantumENDEC: {Title} - {date}"
        if(type(self.ConfigData["email_sendto"]) == list): message['To'] = ",".join(self.ConfigData["email_sendto"])
        else: message['To'] = self.ConfigData["email_sendto"]

        if self.ConfigData["FancyHTML"] is True:    
            thing = MIMEText(body, 'html')
            message.attach(thing)
        else:
            basic_text = f"QuantumENDEC... {Title}\n{Description}\n{ZCZC}\n\n{date}"
            thing = MIMEText(basic_text, 'plain')
            message.attach(thing)

        mail = smtplib.SMTP(self.ConfigData['email_server'], int(self.ConfigData['email_server_port']))
        mail.ehlo()
        mail.starttls()
        mail.login(self.ConfigData["email_user"], self.ConfigData["email_user_pass"])
        mail.sendmail(self.ConfigData["email_user"], self.ConfigData["email_sendto"], message.as_string())
        mail.quit()

    def TxtLog(self, Title, Description, ZCZC):
        dateNow = datetime.now().strftime("%B %d, %Y %H:%M:%S")
        if ZCZC == "": log = f"{Title}\n{Description}"
        else: log = f"{Title}\n{Description}\n{ZCZC}"
        log = f"\n--- {dateNow} ---\n{log}\n"
        try:
            with open(f"{Assets_Folder}/alertlog.txt", "a", encoding='utf-8') as f: f.write(log)
        except:
            with open(f"{Assets_Folder}/alertlog.txt", "w", encoding='utf-8') as f: f.write(log)

    def SendLog(self, Title, Description, ZCZC, type="", HookColor=None):
        if self.ConfigData['enable_discord_webhook'] is True:
            print("[Logger]: Sending Discord webhook...")
            try: self.SendDiscord(Title, Description, ZCZC, type, HookColor)
            except: print("[Logger]: Discord, failed to log.")

        if self.ConfigData['enable_LogToTxt'] is True:
            print(f"[Logger]: Logging to {Assets_Folder}/alertlog.txt...")
            try: self.TxtLog(Title, Description, ZCZC)
            except: print("[Logger]: Text file, failed to log.")

        if self.ConfigData['enable_email'] is True:
            print("[Logger]: Logging to email...")
            try: self.SendEmail(Title, Description, ZCZC, HookColor)
            except: print("[Logger]: Email, failed to log,")

        print("[Logger]: Finished logging.")

def RelayLoop():
    while QEinterrupt() is False:
        Clear()
        with open(Config_File, "r") as JCfile: config = JCfile.read()
        ConfigData = json.loads(config)
        
        print(f"[RELAY]: Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        UpdateStatus("Relay", f"Waiting for alert...")
        ResultFileName = WatchNotify(XMLqueue_Folder, XMLhistory_Folder)
        if QEinterrupt() is True: exit()

        print(f"[RELAY]: Captured: {ResultFileName}")
        shutil.move(f"{XMLqueue_Folder}/{ResultFileName}", f"./relay.xml")
        with open("./relay.xml", "r", encoding='utf-8') as file: RelayXML = file.read()
        UpdateStatus("Relay", f"Processing alert...")
        
        if "<sender>NAADS-Heartbeat</sender>" in RelayXML:
            print("[RELAY]: NAADS HEARTBEAT DETECTED")
            References = re.search(r'<references>\s*(.*?)\s*</references>', RelayXML, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
            Heartbeat(References, XMLqueue_Folder, XMLhistory_Folder)
        else:
            status = re.search(r'<status>\s*(.*?)\s*</status>', RelayXML, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
            msgType = re.search(r'<msgType>\s*(.*?)\s*</msgType>', RelayXML, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)
            sent = re.search(r'<sent>\s*(.*?)\s*</sent>', RelayXML, re.MULTILINE | re.IGNORECASE | re.DOTALL).group(1)

            if ConfigData[f"status{status}"] and ConfigData[f"messagetype{msgType}"]:
                IntroPlayed = False
                REGION = GetAlertRegion(RelayXML)
                RelayINFOS = re.findall(r'<info>\s*(.*?)\s*</info>', RelayXML, re.MULTILINE | re.IGNORECASE | re.DOTALL)
                for InfoXML in RelayINFOS:
                    if FilterCheck_CAP(ConfigData, InfoXML) is True:
                        Gen = Generate(ConfigData, InfoXML, msgType, sent)
                        BroadcastContent = Gen.GenerateTextContent()
                        AlertColor = GetAlertLevelColor(ConfigData, BroadcastContent['SAME'])

                        if ConfigData['PlayoutNoSAME'] is False:
                            if not FilterCheck_SAME(ConfigData, BroadcastContent['SAME']): continue
                        
                        print(f"\n\n[RELAY]: NEW ALERT TO RELAY...\n{BroadcastContent['HEADLINE']}: {BroadcastContent['TEXT']}\n{BroadcastContent['SAME']}\n\n")
                        if QEinterrupt() is True: break

                        Gen.GenerateAudioVisualContent(BroadcastContent, f"#{AlertColor}")
                        Logger(ConfigData).SendLog(BroadcastContent['HEADLINE'], BroadcastContent['TEXT'], BroadcastContent['SAME'], "TX", AlertColor)
                        UpdateCGEN(AlertColor, BroadcastContent['HEADLINE'], BroadcastContent['TEXT'], True)
                        UpdateStatus("Relay", f"Transmitting alert...")
                        Plugins_Run("beforeRelay", BroadcastContent['SAME'], BroadcastContent['TEXT'], InfoXML)

                        global PlayoutAlerts
                        if PlayoutAlerts:
                            Play = Playout(ConfigData, REGION)
                            if ConfigData['PlayoutNoSAME'] is False:
                                if DuplicateSAME(BroadcastContent['SAME']):
                                    print("Duplicate S.A.M.E detected. Alert will be skipped.")
                                    continue

                                if IntroPlayed is False:
                                    Play.LEAD_IN()
                                    IntroPlayed = True
                                Play.SAME()
                                Play.ATTN()
                            else:
                                if IntroPlayed is False:
                                    Play.LEAD_IN()
                                    Play.ATTN()
                                    IntroPlayed = True
                            Play.AUDIO()
                            if ConfigData['PlayoutNoSAME'] is False: Play.EOM()
                
                if IntroPlayed is True:
                    Play.LEAD_OUT()
                    if ConfigData['CGEN_ClearAfterAlert'] is True: UpdateCGEN("000000", "EMERGENCY ALERT DETAILS", "", False)
                    Plugins_Run("afterRelay", BroadcastContent['SAME'], BroadcastContent['TEXT'], InfoXML)
            
            shutil.move(f"./relay.xml", f"{XMLhistory_Folder}/{ResultFileName}")
    exit()

def Clear():
    global clearScreen
    if clearScreen is True: os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='QuantumENDEC')
    parser.add_argument('-v', '--version', action='store_true', help='Displays QuantumENDECs version and exits.')
    parser.add_argument('-H', '--headless', action='store_true', help='Start QuantumENDEC without starting the webserver.')
    parser.add_argument('-c', '--clearScreen', action='store_true', help='Will clear the terminal after every alert.')
    parser.add_argument('-n', '--noPlayout', action='store_true', help='Alerts will not play, for testing.')
    QEARGS = parser.parse_args()

    if QEARGS.version is True:
        print(QuantumENDEC_Version)
        exit()

    if QEARGS.clearScreen is True: clearScreen = True
    else: clearScreen = False

    if QEARGS.noPlayout is True: PlayoutAlerts = False
    else: PlayoutAlerts = True

    print(f"-- Welcome to QuantumENDEC --\n{QuantumENDEC_Version}\n\nDevloped by ApatheticDELL alongside Aaron and BunnyTub\n")

    WebserverThread = None

    while True:
        print("\n\nStarting QuantumENDEC...")
        THREADSLIST = []
        Setup()
        time.sleep(1)
        with open(Config_File, "r") as JCfile: config = JCfile.read()
        ConfigData = json.loads(config)
        UpdateStatus("QuantumENDEC", "Starting up...")
        Plugins_Run("startup")

        QuantumStatus = 0
        
        RelayThread = threading.Thread(target=RelayLoop)
        THREADSLIST.append(RelayThread)

        if QEARGS.headless is False and WebserverThread is None:
            WebserverThread = threading.Thread(target=Webserver().StartServer, args=(ConfigData['WebserverHost'], int(ConfigData['WebserverPort'])))
            WebserverThread.start()

        # Start CAP monitors
        if ConfigData['TCP'] is True:
            if ConfigData['TCP1'] != "":
                TCPHOST, TCPPORT = ConfigData['TCP1'].split(":")
                TCPCAP1Thread = threading.Thread(target=Capture().TCPcapture, args=(TCPHOST, TCPPORT, 1024, "</alert>", "TCP1"))
                THREADSLIST.append(TCPCAP1Thread)
            
            if ConfigData['TCP2'] != "":
                TCPHOST, TCPPORT = ConfigData['TCP2'].split(":")
                TCPCAP2Thread = threading.Thread(target=Capture().TCPcapture, args=(TCPHOST, TCPPORT, 1024, "</alert>", "TCP2"))
                THREADSLIST.append(TCPCAP2Thread)

        if ConfigData['Enable_NWSCAP'] is True:
            if ConfigData['NWSCAP_AtomLink'] != "":
                NWSCAPThread = threading.Thread(target=Capture().NWScapture, args=(ConfigData['NWSCAP_AtomLink'],))
                THREADSLIST.append(NWSCAPThread)

        if ConfigData['HTTP_CAP'] is True:
            if ConfigData['HTTP_CAP_ADDR'] != "":
                HTTPCAP1Thread = threading.Thread(target=Capture().HTTPcapture, args=(ConfigData['HTTP_CAP_ADDR'], 1))
                THREADSLIST.append(HTTPCAP1Thread)
            
            if ConfigData['HTTP_CAP_ADDR1'] != "":
                HTTPCAP2Thread = threading.Thread(target=Capture().HTTPcapture, args=(ConfigData['HTTP_CAP_ADDR1'], 2))
                THREADSLIST.append(HTTPCAP2Thread)
            
            if ConfigData['HTTP_CAP_ADDR2'] != "":
                HTTPCAP3Thread = threading.Thread(target=Capture().HTTPcapture, args=(ConfigData['HTTP_CAP_ADDR2'], 3))
                THREADSLIST.append(HTTPCAP3Thread)
            
            if ConfigData['HTTP_CAP_ADDR3'] != "":
                HTTPCAP4Thread = threading.Thread(target=Capture().HTTPcapture, args=(ConfigData['HTTP_CAP_ADDR3'], 4))
                THREADSLIST.append(HTTPCAP4Thread)
            
            if ConfigData['HTTP_CAP_ADDR4'] != "":
                HTTPCAP5Thread = threading.Thread(target=Capture().HTTPcapture, args=(ConfigData['HTTP_CAP_ADDR4'], 5))
                THREADSLIST.append(HTTPCAP5Thread)

        # Start audio monitors for S.A.M.E
        if ConfigData['SAME-AudioDevice-Monitor'] is True:
            DEVmonitorThread = threading.Thread(target=Monitor_Local("LocalMonitor").start)
            THREADSLIST.append(DEVmonitorThread)
        
        if ConfigData['SAME_AudioStream_Monitors'] is True:
            if ConfigData['SAME-AudioStream-Monitor1'] != "":
                IPmonitor1Thread = threading.Thread(target=Monitor_Stream("IPmonitor1", ConfigData['SAME-AudioStream-Monitor1']).start)
                THREADSLIST.append(IPmonitor1Thread)
            
            if ConfigData['SAME-AudioStream-Monitor2'] != "":
                IPmonitor2Thread = threading.Thread(target=Monitor_Stream("IPmonitor2", ConfigData['SAME-AudioStream-Monitor2']).start)
                THREADSLIST.append(IPmonitor2Thread)
            
            if ConfigData['SAME-AudioStream-Monitor3'] != "":
                IPmonitor3Thread = threading.Thread(target=Monitor_Stream("IPmonitor3", ConfigData['SAME-AudioStream-Monitor3']).start)
                THREADSLIST.append(IPmonitor3Thread)
            
            if ConfigData['SAME-AudioStream-Monitor4'] != "":
                IPmonitor4Thread = threading.Thread(target=Monitor_Stream("IPmonitor4", ConfigData['SAME-AudioStream-Monitor4']).start)
                THREADSLIST.append(IPmonitor4Thread)

        for thread in THREADSLIST: thread.start()
        
        UpdateStatus("QuantumENDEC", "Ready and Running")

        while QuantumStatus == 0:
            try: time.sleep(0.5) # keep-alive
            except KeyboardInterrupt: QuantumStatus = 2

        if QuantumStatus == 1:
            print("QuantumENDEC is restarting... (please wait)")
            UpdateStatus("QuantumENDEC", "Restarting... (please wait)")
        elif QuantumStatus == 2:
            print("QuantumENDEC is shutting down... (please wait)")
            UpdateStatus("QuantumENDEC", "Shutting down... (please wait)")

        for thread in THREADSLIST: thread.join()
        
        if QuantumStatus == 1: continue
        else:
            os.kill(os.getpid(), signal.SIGINT) # This is one way to do it
            exit()