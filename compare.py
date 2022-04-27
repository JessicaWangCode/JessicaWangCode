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
def main():
    ML_Pred= mlp.main()
    Realdata_df = pd.read_csv("test.csv")[::-1] 


    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    y1=ML_Pred
    x1=np.arange(len(y1))
    print(x1.shape) #TEST LINE
    y2=Realdata_df['number']
    print(y2.shape) #TEST LINE
    plt.bar(x1,y1,label="machine learning",color='b')
    x2 = np.arange(len(y2))
    plt.bar(x2,y2,color='r',label="real data")
    plt.legend()
    plt.xlabel("Days")
    plt.ylabel("Number of People")
    plt.title("Comparison")
    plt.show()

    print('Mean Squared Error:', metrics.mean_squared_error(Realdata_df['number'], ML_Pred[0:len(y2)])) 
    
if __name__ == '__main__':
    main()