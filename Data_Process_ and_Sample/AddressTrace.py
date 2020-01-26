import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
plt.close('all')
PATH = "C:/Users/zitao_000/Dropbox/intern/data/Comptroller-0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b.csv"
DATA_STORE_PATH = 'C:/Users/zitao_000/Dropbox/intern/data/count.csv'

##for the dataset: Comptroller-xxxxxx.csv.

class AddressTrace:
    def __init__(self, data_path = PATH, data_store_path = DATA_STORE_PATH):
        self.data_path = data_path
        self.data_store_path = data_store_path
        self.transaction = None

    def run(self):##for the future
        self.clean_data()
        self.runModel()

    def clean_data(self):
        self.transaction = pd.read_csv(self.data_path, index_col=False)
        destination = list(self.transaction.From.unique())
        count_list = []
        from_list = self.transaction.From.to_list()
        for i in destination:
            count_list.append(from_list.count(i))
        d = {'address':destination,'count':count_list}
        df1= pd.DataFrame(data=d)
        df1.sort_values(by=['count'], inplace=True, ascending=False)
        print(df1)
        export_csv = df1.to_csv (self.data_store_path, index = None, header=True)
        """ To Do
        self.trainX, self.optmizeX, self.testX = 
        self.Y.... = 
        """

    def runModel(self):##for the future
        """TO do
        grid search
        self.model = LinearRegression()
        self.model = self.model.fit(self.X, self.Y)"""

    def predict(self, x):##for the future
        return self.model.predict(x)

    def store_or_print(self):##for the future
        pass


    def daily_transaction_count(self):##count daily transaction from same address
        daily_transaction = (pd.to_datetime(self.transaction['DateTime'])
                   .dt.floor('d')
                   .value_counts()
                   .rename_axis('date').reset_index(name='count'))
        print(daily_transaction)
        daily_price = self.transaction.loc[:,['DateTime','Historical $Price/Eth']]
        daily_price['DateTime'] = (pd.to_datetime(daily_price['DateTime'])
                             .dt.floor('d'))
        daily_price = daily_price.drop_duplicates()
        daily_price.rename(columns={"DateTime":"date"}, inplace=True)
        daily_count = pd.merge(daily_price,daily_transaction,on='date')
        daily_count.set_index('date', inplace=True)
        print(daily_count)
        daily_count.plot()
        plt.legend(loc='best')
        plt.show()


bm = AddressTrace(PATH, DATA_STORE_PATH)
bm.clean_data()
bm.daily_transaction_count()
