# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# <codecell>

# Update Logs from Polipo
import subprocess 
subprocess.call("zcat /var/log/polipo/*.gz | cat - /var/log/polipo/*.log > proxy.log", shell=True)

# Import Logs
df = pd.read_csv("proxy.log", sep=" - ", names=["date", "method", "url"])

# clean log file
subprocess.call("rm proxy.log", shell=True)

# Print Stats
df = df[df.url.notnull()] # discard rows without url
# df = df[df.method == "GET"]
df.date = pd.to_datetime(df.date)
df.index = df.date
df['host'] = df.url.apply(get_host)
print df.index.size
df.head()

# <codecell>

def get_host(url):
    url = url.strip("http://")
    url = url.split("/")[0]
    url = url.split(":")[0]
    return url

classes = {
    "news"   : ["zeit.de", "welt.de"],
    "social" : ["facebook.com", "twitter.com"],
    "status" : ["dropbox.com", "ghostery"],
    "learn"  : ["wikipedia.org", "stackoverflow", "wikibooks", "wikimedia"],
    "work"   : ["github.com", "calendar.google.com"],
    "search" : ["google"]
}

numeric_classes = {
    "news"   : 10,
    "social" : 15,
    "status" : 0,
    "unknown": -1,
    "search" : -5,
    "work"   : -8,
    "learn"  : -10,
}

def classify(host):
    for host_class, parts in classes.items():
        if any([ (host_part in host) for host_part in parts ]): 
            return host_class
    return "unknown"

def n_classify(host):
    return numeric_classes[classify(host)]

# <codecell>

df['host_type'] = df.host.apply(n_classify)
# plt.plot(df.host_type,df.date,'o')

# <codecell>

from datetime import datetime
plt.figure(figsize=(20,5))
gf = df[df.date > datetime(2014,9,7,0,0,0)]
plt.plot(gf.date,gf.host_type,'o')

# <codecell>


