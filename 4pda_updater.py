import re
import requests as rq

# BaconReader Premium, Relay PRO, "https://4pda.ru/forum/index.php?showtopic=405738", "https://4pda.ru/forum/index.php?showtopic=592442", "https://4pda.ru/forum/index.php?showtopic=358275"
sites = ["https://4pda.ru/forum/index.php?showtopic=260256",
         "https://4pda.ru/forum/index.php?showtopic=200425",
         "https://4pda.ru/forum/index.php?showtopic=273456",
         "https://4pda.ru/forum/index.php?showtopic=248833",
         "https://4pda.ru/forum/index.php?showtopic=826265",
         "https://4pda.ru/forum/index.php?showtopic=246914",
         "https://4pda.ru/forum/index.php?showtopic=297970",
         "https://4pda.ru/forum/index.php?showtopic=652935",
         "https://4pda.ru/forum/index.php?showtopic=230839",
         "https://4pda.ru/forum/index.php?showtopic=744314"]
ver_s = ["1.2.5", "1.4", "3.2.0", "1.0", "1.1", "5.97", "4", "0.16", "4.8.4", "14.0.0"]

for i, a in enumerate(zip(sites, ver_s)):
    html = rq.get(a[0]).content.decode("cp1251")
    ver  = re.findall("версия: [0-9\.]+", html)[0].split()[1]
    date = re.findall("Последнее обновление программы в шапке [0-9\.]+", html)
    if ver > a[1]:
        print(i, ver, a[0], a[1])
