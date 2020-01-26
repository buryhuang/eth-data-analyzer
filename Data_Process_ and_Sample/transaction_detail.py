import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
plt.close('all')

PATH_ORIGIN = "Comptroller-0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b.csv"
PATH_FUNCTION = "transaction.csv"
DATA_STORE_PATH = 'C:/Users/zitao_000/Dropbox/intern/data/transaction_detail.csv'

## for the dataset:compound_function_calls.csv(here I renamed as Transaction.CSV). The features are renamed as: Txhash	Function	lable1	lable2	Token_Number	token1	token2	token3	token4	token5	token6	token7.
## see uploded example


class Transaction:
    def __init__(self, data_function_path = PATH_FUNCTION, data_store_path = DATA_STORE_PATH):
        self.data_function_path = data_function_path
        self.data_store_path = data_store_path
        self.function = None
        self.transaction = None

    def run(self):##for the future
        self.clean_data()
        self.runModel()

    def clean_data(self):  ##delete 0s from coin name
        self.function = pd.read_csv(self.data_function_path, index_col=False)
        for i in range(self.function.shape[0]):
            for j in range(5,self.function.shape[1]):
                self.function.iloc[i,j] = str(self.function.iloc[i,j]).lstrip(" 0")
        """ To Do
        self.trainX, self.optmizeX, self.testX = 
        self.Y.... = 
        """

    def merge_data(self, data_origin_path = PATH_ORIGIN): ##combine datasets, and return coin name
        origin = pd.read_csv(data_origin_path, index_col=False)
        self.transaction = pd.merge(origin,self.function,on = "Txhash")
        dictionary = {"6c8c6b02e7b2be14d4fa6022dfd6d75921d90e4e":"cBAT",
                      "5d3a536e4d6dbd6114cc1ead35777bab948e3643":"cDAI",
                      "4ddc2d193948926d02f9b1fe9e1daa0718270ed5":"cETH",
                      "158079ee67fce2f58472a96584a73c7ab9ac95c1":"cREP",
                      "f5dce57282a584d2746faf1593d3121fcac444dc":"cSAI",
                      "39aa39c021dfbae8fac545936693ac917d5e7563":"cUSDC",
                      "c11b1268c1a384e55c48c2391d8d480264a3a7f4":"cWBTC",
                      "b3319f5d18bc0d84dd1b4825dcde5d5f7266d407":"cZRX"
                      }
        ind = list(self.transaction.columns).index("token1")
        self.transaction.iloc[:,ind:] = self.transaction.iloc[:,ind:].replace(dictionary)
        export_csv = self.transaction.to_csv(self.data_store_path, index=None, header=True)


    def token_combinantion(self,store_path = 'C:/Users/zitao_000/Dropbox/intern/data/token_combination.csv'): ##rturn transaction statitics
       data = pd.read_csv(self.data_store_path, index_col=False)
       ind = list(data.columns).index("token1")
       token = data.iloc[:,ind:]
       #combination = token.drop_duplicates()
       token['comb'] = token['token1'].map(str)+token['token2'].map(str)+token['token3'].map(str)\
                       +token['token4'].map(str)+token['token5'].map(str)+token['token6'].map(str)+token['token7'].map(str)

       #['token1', 'token2', 'token3', 'token4', 'token5', 'token6', 'token7']

       result = token.groupby(['comb'])['token1'].count().reset_index(name='count') \
                             .sort_values(['count'], ascending=False)
       export_csv = result.to_csv(store_path, index=None, header=True)



    def runModel(self):##for the future
        """TO do
        grid search
        self.model = LinearRegression()
        self.model = self.model.fit(self.X, self.Y)"""

    def predict(self, x):##for the future
        return self.model.predict(x)

    def store_or_print(self):##for the future
        pass

Tr = Transaction(PATH_FUNCTION, DATA_STORE_PATH)
#Tr.clean_data()
#Tr.merge_data(PATH_ORIGIN)
Tr.token_combinantion()
