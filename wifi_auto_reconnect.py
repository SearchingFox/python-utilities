# Windows only :(
from subprocess import check_output

wlan_name = "zzznet"
connectedQ = (check_output("netsh wlan show interfaces", shell=True).decode('ascii', 'ignore')).find(wlan_name)

if connectedQ < 0:
    out = check_output("netsh wlan connect " + wlan_name, shell=True)
    print(out.decode('ascii', 'ignore'))