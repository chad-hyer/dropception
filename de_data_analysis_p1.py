# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 15:49:42 2026

@author: hyerc
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
from statannotations.Annotator import Annotator
import os, warnings
warnings.filterwarnings('ignore')

source = 'dropception_results_p1' #folder to pull data from
files = [file for file in os.listdir(source) if '.xlsx' in file] #excel data files
data_dict = {}
summary_agg = []
for file in files:
    timepoint = int(file[:2])
    summaryDF = pd.read_excel(f'{source}/{file}', sheet_name='Summary', header=10) #Get average stats for each image
    dropletDF = pd.read_excel(f'{source}/{file}', sheet_name='Droplet Data') #Get full data for each image
    data_dict.update({timepoint:{'Summary':summaryDF,'Droplet Data':dropletDF}}) #Store for later
    summary_agg.append(pd.Series({
        'timepoint' : timepoint,
        'size_mean' : summaryDF.loc[0]['Mean'],
        'size_std' : summaryDF.loc[0]['Std Dev'],
        'size_kde' : summaryDF.loc[0]['KDE Peak'],
        'green_mean' : summaryDF.loc[2]['Mean'],
        'green_std' : summaryDF.loc[2]['Std Dev'],
        'green_kde' : summaryDF.loc[2]['KDE Peak'],
        'red_mean' : summaryDF.loc[3]['Mean'],
        'red_std' : summaryDF.loc[3]['Std Dev'],
        'red_kde' : summaryDF.loc[3]['KDE Peak']
        }))

data = pd.DataFrame(summary_agg)

#Plot how size changes with time
fig, ax = plt.subplots()
ax.errorbar(x=data['timepoint'],y=data['size_mean'],yerr=data['size_std'],color='tab:red',ecolor='black',zorder=0,capsize=5)
sns.scatterplot(data=data, x='timepoint', y='size_mean', ax=ax,label='Radius',color='tab:red',zorder=1)
ax.axvline(6.5,color='red',linestyle='--',label='Flowrate Change')
ax.set_ylabel('Mean DE Radius (px)', fontsize=12, fontweight=600)
ax.set_xlabel('Timepoint', fontsize=12, fontweight=600)
ax.set_title('DE Size Over Time', fontsize=14, fontweight=600)
ax.legend()
plt.savefig(f'{source}/DE Size Over Time.svg')

#Plot how intensity across channels changes with time
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.errorbar(x=data['timepoint'],y=data['green_kde'],yerr=data['green_std'],color='tab:green',ecolor='black',zorder=0,capsize=5)
sns.scatterplot(data=data, x='timepoint', y='green_kde', ax=ax1,label='Green',color='tab:green',zorder=1)
ax1.set_ylabel('KDE Green Intensity (RFU)', fontsize=12, fontweight=600)
ax1.set_xlabel('Timepoint', fontsize=12, fontweight=600)
ax1.set_title('Fluorescence Across Channels Over Time', fontsize=14, fontweight=600)
ax1.legend('', frameon=False)

ax2.errorbar(x=data['timepoint'],y=data['red_kde'],yerr=data['red_std'],color='tab:orange',ecolor='black',zorder=0,capsize=5)
sns.scatterplot(data=data, x='timepoint', y='red_kde', ax=ax2,label='Red',color='tab:orange',zorder=1)
ax2.axvline(6.5,color='red',linestyle='--',label='Flowrate Change')
ax2.set_ylabel('KDE Red Intensity (RFU)', fontsize=12, fontweight=600, rotation=-90, labelpad=15)
ax2.legend('', frameon=False)

fig.legend(loc='lower center', bbox_to_anchor=(0.5, -0.1),ncol=3)
plt.savefig(f'{source}/Fluorescence Across Channels Over Time.svg')

#Plot how intensity across channels changes with time after cleaning the initial equilibration
cleaned = data.drop(index=[0,1,2])
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.errorbar(x=cleaned['timepoint'],y=cleaned['green_kde'],yerr=cleaned['green_std'],color='tab:green',ecolor='black',zorder=0,capsize=5)
sns.scatterplot(data=cleaned, x='timepoint', y='green_kde', ax=ax1,label='Green',color='tab:green',zorder=1)
ax1.set_ylabel('KDE Green Intensity (RFU)', fontsize=12, fontweight=600)
ax1.set_xlabel('Timepoint', fontsize=12, fontweight=600)
ax1.set_title('Fluorescence Across Channels Over Time', fontsize=14, fontweight=600)
ax1.legend('', frameon=False)

ax2.errorbar(x=cleaned['timepoint'],y=cleaned['red_kde'],yerr=cleaned['red_std'],color='tab:orange',ecolor='black',zorder=0,capsize=5)
sns.scatterplot(data=cleaned, x='timepoint', y='red_kde', ax=ax2,label='Red',color='tab:orange',zorder=1)
ax2.axvline(6.5,color='red',linestyle='--',label='Flowrate Change')
ax2.set_ylabel('KDE Red Intensity (RFU)', fontsize=12, fontweight=600, rotation=-90, labelpad=15)
ax2.legend('', frameon=False)

fig.legend(loc='lower center', bbox_to_anchor=(0.5, -0.1),ncol=3)
plt.savefig(f'{source}/Fluorescence Across Channels Over Time Stabilized.svg')

#Compare distributions across once acquisition has stabilized
stable5050 = data.loc[4:6]
stable3010 = data.loc[9:11]
stable5050['Flowrate (G:R)'] = '20:20'
stable3010['Flowrate (G:R)'] = '30:10'
stable = pd.concat([stable5050,stable3010])

source_5050 = [4,5,6]
source_3010 = [10,11,12]

green_5050 = []
red_5050 = []

green_3010 = []
red_3010 = []

for timepoint in source_5050:
    df = data_dict[timepoint]['Droplet Data']
    green_5050.append(df['Ch2_Net'])
    red_5050.append(df['Ch3_Net'])

for timepoint in source_3010:
    df = data_dict[timepoint]['Droplet Data']
    green_3010.append(df['Ch2_Net'])
    red_3010.append(df['Ch3_Net'])

g5050 = pd.concat(green_5050).to_frame()
g5050['Flowrate (G:R)'] = '20:20'
g3010 = pd.concat(green_3010).to_frame()
g3010['Flowrate (G:R)'] = '30:10'
g = pd.concat([g5050,g3010])

r5050 = pd.concat(red_5050).to_frame()
r5050['Flowrate (G:R)'] = '20:20'
r3010 = pd.concat(red_3010).to_frame()
r3010['Flowrate (G:R)'] = '30:10'
r = pd.concat([r5050,r3010])

#Perform stats on each distribution
gt, gp = stats.ttest_ind(g5050['Ch2_Net'].to_list(),g3010['Ch2_Net'].to_list())
rt, rp = stats.ttest_ind(r5050['Ch3_Net'].to_list(),r3010['Ch3_Net'].to_list())

gts, gps = stats.ttest_ind(stable5050['green_kde'].to_list(),stable3010['green_kde'].to_list())
rts, rps = stats.ttest_ind(stable5050['red_kde'].to_list(),stable3010['red_kde'].to_list())

pairs = [('20:20','30:10')]

#Green distribution plot
fig, (ax, ax2) = plt.subplots(ncols=2, figsize=(10, 5))
sns.histplot(data=g,x='Ch2_Net',hue='Flowrate (G:R)', ax=ax, kde=True)
#Find kde maxes for each flowrate to calculate the foldchange
kde2020 = ax.lines[1]
kde3010 = ax.lines[0]
kdemax2020 = kde2020.get_xdata()[np.argmax(kde2020.get_ydata())]
kdemax3010 = kde3010.get_xdata()[np.argmax(kde3010.get_ydata())]
fc = kdemax3010 / kdemax2020
ax.set_ylabel('Count', fontsize=12, fontweight=600)
ax.set_xlabel('Green Fluorescence (RFU)', fontsize=12, fontweight=600)
ax.set_title(f't-stat: {round(gt,3)} | p-value: {gp:.3e} | KDE FC: {round(fc,3)}')
sns.barplot(data=stable,x='Flowrate (G:R)',y='green_kde', ax=ax2, alpha=0.8, capsize=0.25)
ax2.set_ylabel('Green Fluorescence (RFU)', fontsize=12, fontweight=600)
annotator = Annotator(ax2, pairs, data=stable, x='Flowrate (G:R)', y='green_kde')
annotator.configure(test='t-test_ind', text_format='star', loc='inside')
annotator.apply_and_annotate()
ax2.set_xlabel('Flowrate (G:R)', fontsize=12, fontweight=600)
fc = stable3010['green_kde'].mean() / stable5050['green_kde'].mean()
ax2.set_title(f't-stat: {round(gts,3)} | p-value: {gps:.3e} | KDE FC: {round(fc,3)}')
fig.suptitle('Green Fluorescence Distributions Over Flowrates', fontsize=14, fontweight=600)
fig.tight_layout()
plt.savefig(f'{source}/Green Fluorescence Distributions Over Flowrates.svg')

#Red distribution plot
fig, (ax, ax2) = plt.subplots(ncols=2, figsize=(10, 5))
sns.histplot(data=r,x='Ch3_Net',hue='Flowrate (G:R)', ax=ax, kde=True)
#Find kde maxes for each flowrate to calculate the foldchange
kde2020 = ax.lines[1]
kde3010 = ax.lines[0]
kdemax2020 = kde2020.get_xdata()[np.argmax(kde2020.get_ydata())]
kdemax3010 = kde3010.get_xdata()[np.argmax(kde3010.get_ydata())]
fc = kdemax3010 / kdemax2020
ax.set_ylabel('Count', fontsize=12, fontweight=600)
ax.set_xlabel('Red Fluorescence (RFU)', fontsize=12, fontweight=600)
ax.set_title(f't-stat: {round(rt,3)} | p-value: {rp:.3e} | KDE FC: {round(fc,3)}')
sns.barplot(data=stable,x='Flowrate (G:R)',y='red_kde', ax=ax2, alpha=0.8, capsize=0.25)
ax2.set_ylabel('Red Fluorescence (RFU)', fontsize=12, fontweight=600)
annotator = Annotator(ax2, pairs, data=stable, x='Flowrate (G:R)', y='red_kde')
annotator.configure(test='t-test_ind', text_format='star', loc='inside')
annotator.apply_and_annotate()
ax2.set_xlabel('Flowrate (G:R)', fontsize=12, fontweight=600)
fc = stable3010['red_kde'].mean() / stable5050['red_kde'].mean()
ax2.set_title(f't-stat: {round(rts,3)} | p-value: {rps:.3e} | KDE FC: {round(fc,3)}')
fig.suptitle('Red Fluorescence Distributions Over Flowrates', fontsize=14, fontweight=600)
fig.tight_layout()
plt.savefig(f'{source}/Red Fluorescence Distributions Over Flowrates.svg')