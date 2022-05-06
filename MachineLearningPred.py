# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 23:25:44 2022

@author: 27666
"""

import numpy as np
import pandas as pd
import datetime
from sklearn.model_selection import train_test_split 
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn import metrics
import seaborn as sns
import matplotlib.pyplot as plt

#ASK FOR INDEX
def index():
    answer = input("Choose for Covid index:\nCumulative Cases(1) \nCumulative Death(2) \nDaily New Case(3) \n")
    while True:
        if answer == '1':
            index = "cumCasesBySpecimenDate"
            break
        elif answer == '2':
            index = 'cumDeaths28DaysByPublishDate'
            break
        elif answer == '3':
            index = 'newCasesBySpecimenDate'
            break
        else:
            print("error. Please enter again.")
            answer = input("Choose for Covid index:\nCumulative Cases(1) \nCumulative Death(2) \nDaily New Case(3) \n")
        
    return(index)

def create_assist_date(datestart = None,dateend = None):
	# CREATE OUT OF SAMPLE DATELIST

	if datestart is None:
		datestart = '01/01/2022'
	if dateend is None:
		dateend = datetime.datetime.now().strftime("%d/%m/%Y")

	# TRANSFER TO DATE
	datestart=datetime.datetime.strptime(datestart,"%d/%m/%Y")
	dateend=datetime.datetime.strptime(dateend,"%d/%m/%Y")
	date_list = []
	date_list.append(datestart.strftime("%d/%m/%Y"))
    

	while datestart<dateend:
		# ADD A NEW DAY
	    datestart+=datetime.timedelta(days=+1)
	    #ADD TO LIST
	    date_list.append(datestart.strftime("%d/%m/%Y"))
    
	return(date_list)


#DATA CLEANING
def DataPreparation(COVID_df,index,datelist):
    
    COVID_df['date'] = COVID_df['date'].apply(lambda x: datetime.datetime.strptime(x, "%d/%m/%Y"))
    COVID_df['date'] = pd.to_numeric(COVID_df.date)
    
    datelist = pd.DataFrame(datelist)
    datelist.columns = ['ds']
    datelist['ds'] = datelist['ds'].apply(lambda x: datetime.datetime.strptime(x, "%d/%m/%Y"))
    datelist['ds'] = pd.to_numeric(datelist.ds)
    
    
    COVID_df_cleaned = COVID_df.dropna(axis=0,subset = [index]) #drop all rows that have any NaN values
   
    
    X = np.array(COVID_df_cleaned['date'])
    y = np.array(COVID_df_cleaned[index])
    datelist = np.array(datelist['ds'])
    # SPLITING DATASET INTO TRAINING SET AND TEST SET. 
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=0)
    
    #STANDARDIZATION
    scalerX1 = MinMaxScaler()
    scalerY1 = MinMaxScaler()
    x_train1 = scalerX1.fit_transform(np.array(X_train).reshape(-1,1))
    y_train1 = scalerY1.fit_transform(np.array(y_train).reshape(-1,1))
    datelist = scalerX1.transform(np.array(datelist).reshape(-1,1))
    x_test1 = scalerX1.transform(np.array(X_test).reshape(-1,1))
    
    return x_train1,y_train1,y_test,X_test,x_test1,y_train,scalerY1,datelist

class COVID_ML():
    def __init__(self,x_train1,y_train1,y_train,scalerY1,datelist,x_test1):
        self.x_train1 = x_train1
        self.y_train1 = y_train1
        self.y_train = y_train
        self.scalerY1 = scalerY1
        self.datelist = datelist
        self.x_test1 = x_test1
    def SVM_IS_Predict(self):  
        #SUPPORT VECTOR MACHINE MODEL WITH IN-SAMPLE PREDICTION
        svm=SVR(kernel="rbf", C=1,epsilon=0.01,gamma='scale')
        svm.fit(self.x_train1,self.y_train1)
        y_pred_IS=self.scalerY1.inverse_transform(np.array(svm.predict(self.x_test1)).reshape(-1,1))
        y_pred_IS=np.array(y_pred_IS).reshape(-1)
        return y_pred_IS
    def LR_IS_Predict(self):
        #LINEAR REGRESSION MODEL WITH IN-SAMPLE PREDICTION
        regressor = LinearRegression()
        regressor.fit(self.x_train1, self.y_train)
        y_pred_IS = regressor.predict(self.x_test1)
        y_pred_IS=np.array(y_pred_IS).reshape(-1)
        return y_pred_IS
    def SVM_OS_Predict(self):  
        #SUPPORT VECTOR MACHINE MODEL WITH OUT-SAMPLE PREDICTION
        svm=SVR(kernel="rbf", C=1,epsilon=0.01,gamma='scale')
        svm.fit(self.x_train1,self.y_train1)
        y_pred_OS=self.scalerY1.inverse_transform(np.array(svm.predict(self.datelist)).reshape(-1,1))
        y_pred_OS=np.array(y_pred_OS).reshape(-1)
        return y_pred_OS
    def LR_OS_Predict(self):
        #LINEAR REGRESSION MODEL WITH IN-SAMPLE PREDICTION
        regressor = LinearRegression()
        regressor.fit(self.x_train1, self.y_train)
        y_pred_OS = regressor.predict(self.datelist)
        y_pred_OS=np.array(y_pred_OS).reshape(-1)
        return y_pred_OS
    
    
def comparison(y_test,X_test,y_pred_IS):
        #EVALUATE LEARNING RESULT
        dff = pd.DataFrame({'Current': y_test, 'Predicted': y_pred_IS})
        print(dff.head())
        print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred_IS))  
        X_test = pd.to_datetime(X_test)
        sns.scatterplot(X_test,y_test,color='#A7A7A7',s=75,label="Actual")
        sns.lineplot(X_test,np.array(y_pred_IS).reshape(-1),color="#A4D54E",linewidth=2.25,label="Predicted")
        plt.show()
def main():
    #LOAD TRAINING DATA
    COVID_df = pd.read_csv("overview_2022-04-01 (1).csv")
    #CREATE DATELIST
    datelist = create_assist_date('30/01/2020')
    
    x_train1,y_train1,y_test,X_test,x_test1,y_train,scalerY1,datelist = DataPreparation(COVID_df,'newCasesBySpecimenDate',datelist)
    
    ML = COVID_ML(x_train1,y_train1,y_train,scalerY1,datelist,x_test1)
    
    #CHOOSE A MACHINELEARNING MODEL
    method = ML.SVM_OS_Predict()
    #GET MACHINE LEARNING RESULT
    predict = np.array(method.reshape(-1))
    
    #ENSURE ONLY IN SAMPLE PREDICTION WILL TRIGGER COMPARISON
    if method.shape == ML.SVM_IS_Predict().shape or method.shape ==ML.LR_IS_Predict().shape:
        comparison(y_test,X_test,predict)
    return predict
    
if __name__ == '__main__':
    main()    





