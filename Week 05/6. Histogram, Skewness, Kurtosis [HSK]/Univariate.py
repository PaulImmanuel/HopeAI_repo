import pandas as pd
class Univariate():
    def quanQual(self,dataset):
        quan = []
        qual = []
        for data in dataset.columns:
            if(dataset[data].dtype=='object'):
                qual.append(data)
            else:
                quan.append(data)
        return quan,qual
        
    def freqTable(dataset,columnName):
        freqTable=pd.DataFrame(columns=["Unique_Values","Frequency","Relative Frequency","Cusum"])
        freqTable["Unique_Values"] = dataset[columnName].value_counts().index
        freqTable["Frequency"] = dataset[columnName].value_counts().values
        freqTable["Relative Frequency"] = freqTable["Frequency"]/len(freqTable)
        freqTable["Cusum"] = freqTable["Relative Frequency"].cumsum()
        return freqTable

    def Univariate(dataset,quan):
        descriptive =pd.DataFrame(index=["Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%","Q4:100%","IQR","1.5rule","Lesser","Greater","Min","Max","Kurtosis","Skew"],columns=quan)
        for columnName in quan:
            descriptive[columnName]["Mean"]=dataset[columnName].mean()
            descriptive[columnName]["Median"]=dataset[columnName].median()
            descriptive[columnName]["Mode"]=dataset[columnName].mode()[0]
            descriptive[columnName]["Q1:25%"]=dataset.describe()[columnName]['25%']
            descriptive[columnName]["Q2:50%"]=dataset.describe()[columnName]['50%']
            descriptive[columnName]["Q3:75%"]=dataset.describe()[columnName]['75%']
            descriptive[columnName]["Q4:100%"]=dataset.describe()[columnName]['max']
            descriptive[columnName]["IQR"]=descriptive[columnName]["Q3:75%"]-descriptive[columnName]["Q1:25%"]
            descriptive[columnName]["1.5rule"]=1.5*descriptive[columnName]["IQR"]
            descriptive[columnName]["Lesser"]=descriptive[columnName]["Q1:25%"]-descriptive[columnName]["1.5rule"]
            descriptive[columnName]["Greater"]=descriptive[columnName]["Q3:75%"]+descriptive[columnName]["1.5rule"]
            descriptive[columnName]["Min"]=dataset[columnName].min()
            descriptive[columnName]["Max"]=dataset[columnName].max()
            descriptive[columnName]["Kurtosis"]=dataset[columnName].kurtosis()            
            descriptive[columnName]["Skew"]=dataset[columnName].skew()

        return descriptive
