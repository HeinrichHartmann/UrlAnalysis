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
print df.index.size
df.head()

# <codecell>

def get_host(url):
    url = url.strip("http://")
    url = url.split("/")[0]
    url = url.split(":")[0]
    return url

classes = {
    "news"   : { 'patterns': ["zeit.de", "welt.de"],          'value' : 10 },
    "social" : { 'patterns': ["facebook.com", "twitter.com"], 'value' : 15 },
    "status" : { 'patterns': ["dropbox.com", "ghostery"],     'value' : 0 },
    "learn"  : { 'patterns': ["wikipedia.org", "stackoverflow", "wikibooks", "wikimedia"], 'value' : -5 },
    "work"   : { 'patterns': ["github.com", "calendar.google.com"], 'value' : -10 },
    "search" : { 'patterns': ["google"], 'value' : 1 },
    "unknown": { 'patterns': [], 'value' : 0 },
}

def classify(host):
    for host_class, ob in classes.items():
        if any([ (pattern in host) for pattern in ob['patterns'] ]): 
            return host_class
    return "unknown"

def n_classify(host):
    return classes[classify(host)]['value']

# <codecell>

df['host'] = df.url.apply(get_host)
df['host_type'] = df.host.apply(n_classify)
# plt.plot(df.host_type,df.date,'o')

# <codecell>

from datetime import datetime
plt.figure(figsize=(20,5))
gf = df# [df.date > datetime(2014,9,7,0,0,0)]
plt.plot(gf.date,gf.host_type,'o')

# <codecell>


