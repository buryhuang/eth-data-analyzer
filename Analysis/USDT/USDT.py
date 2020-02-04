import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
plt.close('all')
PATH = "C:/Users/zitao_000/Dropbox/intern/data/export-token-0xdac17f958d2ee523a2206206994597c13d831ec7.csv"
DATA_STORE_SELL_PATH = 'C:/Users/zitao_000/Dropbox/intern/data/USDT_sell.csv'

DATA_STORE_BUY_PATH = 'C:/Users/zitao_000/Dropbox/intern/data/USDT_buy.csv'
DATA_STORE_COMPLETE_PATH = 'C:/Users/zitao_000/Dropbox/intern/data/USDT_complete.csv'


##INPUT DATA sample export-token-0xdac17f958d2ee523a2206206994597c13d831ec7.csv
class USDT:
    def __init__(self, data_path = PATH, data_store_complete_path = DATA_STORE_COMPLETE_PATH, data_store_sell_path = DATA_STORE_SELL_PATH, data_store_buy_path = DATA_STORE_BUY_PATH):
        self.data_path = data_path
        self.data_store_sell_path = data_store_sell_path
        self.data_store_buy_path = data_store_buy_path
        self.data_store_complete_path = data_store_complete_path
        self.transaction = None

    def run(self):##for the future
        self.clean_data()
        self.runModel()

    def sell_count(self):##return USDT_sell
        self.transaction = pd.read_csv(self.data_path, index_col=False)
        sell = self.transaction.loc[self.transaction.From=="0x5754284f345afc66a98fbb0a0afe71e0f007b949"]
        export_csv = sell.to_csv(self.data_store_sell_path, index=None, header=True)
        destination = list(sell.To.unique())
        count_list = []
        destination_list = sell.To.to_list()
        for i in destination:
            count_list.append(destination_list.count(i))
        d = {'address':destination,'sell_count':count_list}
        df1= pd.DataFrame(data=d)
        df1.sort_values(by=['sell_count'], inplace=True, ascending=False)


        ##sum goup by destination
        df2 = sell.loc[:,['To','Quantity']].groupby('To').sum()

        sell1 = pd.merge(df1, df2, how='left', left_on=['address'], right_on=['To'])
        export_csv = sell1.to_csv(self.data_store_sell_path, index=None, header=True)
        return ()

    def buy_count(self):##return USDT_buy
        self.transaction = pd.read_csv(self.data_path, index_col=False)
        buy = self.transaction.loc[self.transaction.To == "0x5754284f345afc66a98fbb0a0afe71e0f007b949"]
        export_csv = buy.to_csv(self.data_store_buy_path, index=None, header=True)
        origin = list(buy.From.unique())
        count_list = []
        origin_list = buy.From.to_list()
        for i in origin:
            count_list.append(origin_list.count(i))
        d = {'address': origin, 'buy_count': count_list}
        df1 = pd.DataFrame(data=d)
        df1.sort_values(by=['buy_count'], inplace=True, ascending=False)

        ##sum goup by destination
        df2 = buy.loc[:, ['From', 'Quantity']].groupby('From').sum()

        buy1 = pd.merge(df1, df2, how='left', left_on=['address'], right_on=['From'])
        export_csv = buy1.to_csv(self.data_store_buy_path, index=None, header=True)
        return()

    def combine_buy_sell(self):##return USDT_complete
        buy = pd.read_csv(self.data_store_buy_path, index_col=False)
        sell = pd.read_csv(self.data_store_sell_path, index_col=False)
        total = pd.merge(sell, buy, how='left', on=['address'])
        export_csv = total.to_csv(self.data_store_complete_path, index=None, header=True)




bm = USDT(PATH, DATA_STORE_COMPLETE_PATH, DATA_STORE_SELL_PATH,DATA_STORE_BUY_PATH)
bm.buy_count()
bm.sell_count()
bm.combine_buy_sell()
#bm.daily_transaction_count()