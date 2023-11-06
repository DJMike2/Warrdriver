#Create the functions
import os
import subprocess

def PasswordCracker():
    pass



def Deauth(Type):
    if Type == 1:# aireplay-ng
        process = subprocess(f'sudo aireplay-ng wlan0mon -b') #-b bssid, sud -0 deaut hattack -c client, -w ...
        print(process.pid)#mdk4,
    if Type == 2:# mdk4 ATTACK MODE d: Deauthentication and Disassociation

        pass
    if Type == 3:#mixidkk??
        pass
def ARP():
    pass

def Spoofing():
    pass


def MITM():
    pass
def Twin():
    pass
def Phishing():
    pass


#Gonna get very complicated