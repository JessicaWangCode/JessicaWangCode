# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 23:13:58 2022

@author: 27666
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import MachineLearningPred as mlp
from sklearn import metrics
import SIRmodel as SIR

def main():
    ML_Pred= mlp.main()
    Realdata_df = pd.read_csv("real_data.csv")[::-1] 
    df = SIR.getDataFrame(53500000, 0.13, 0.114)
    
    #SET MACHINE LEARNING DATA
    y1=ML_Pred
    x1=np.arange(len(y1))
    
    #print(x1.shape) #TEST LINE
    
    #SET REAL DATA
    y2=Realdata_df['newcase']
    x2 = np.arange(len(y2))
    #print(y2.shape) #TEST LINE    
    
    #SET SIMULATION DATA
    y3=df['infected']
    x3 = np.arange(len(y3))
    
    #EVALUATE MODEL BY COMPARING WITH REAL DATA QUANTITATIVELY
    EV_ML=metrics.mean_squared_error(Realdata_df['newcase'], ML_Pred[0:len(y2)])
    EV_TH = metrics.mean_squared_error(Realdata_df['newcase'], df['infected'][0:len(y2)])
    
    #Plot real data
    plt.bar(x2,y2,color='r',label='real data')
    #Plot machine learning result
    plt.bar(x1,y1,label='machine learning result:%s'%(EV_ML),color='b')
    #Plot SIR model result
    plt.bar(x3,y3,color='g',label='SIR model result:%s'%(EV_TH))
    
    #STYLE&LEGEND
    plt.legend()
    plt.grid(b=True, which='major', axis='y', color='#888888', linestyle='--')
    plt.xlabel("Days Since Pandemic Outbreak")
    plt.ylabel("Number of People")
    plt.title("Comparison of Daily New Cases")
    plt.show()
    
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    