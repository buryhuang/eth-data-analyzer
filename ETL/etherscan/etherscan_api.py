##This is the code for getting data from etherscan
import json
import io
import csv
import sys
import etherscan.accounts as accounts
from datetime import datetime


##transfer  内部转账  beabacc8    borrow  借款  4b8a3529   repay  还款  22867d78
# depositToken  存款  338b5dea
# withdrawToken   取款  9e281a98    withdrawAllToken   全部取款  ae4dd0fc
# liquidate    清算  86b9d81f
class definer_data_collector():
    def __init__(self):
        self.transaction = []
        self.transaction_erc20 = []
        self.definer_function = {"beabacc8 ":"transfer", "4b8a3529":"borrow","22867d78":"repay", \
                                 "9e281a98":"withdrawToken","338b5dea":"depositToken","ae4dd0fc":"withdrawAllToken", \
                                 "86b9d81f":"liquidate "}

    # This is the function to get ALL Transaction from the specific account/contract from etherscan
    # Due to the Limitation of the API, only 10000 transaction will be stored
    # No erc20 Token info
    # it will return a jason file:"Definer.json"
    def etherscan_reader(self,number = 10000,address = "0x8fFd2bD41E1AE6664FeDed043fA6fDc0AdFdA85a"):
        with open('api_key.json', mode='r') as key_file:
            key = json.loads(key_file.read())['key']
        api = accounts.Account(address=address, api_key=key)
        self.transaction = api.get_transaction_page(sort='desc',offset=number)
        self.change_dictionary()
        with open("Definer.json","w")as outfile:
            json.dump(self.transaction, outfile)

    # This is the function to get  Transaction with ERC_20 from the specific account/contract from etherscan
    # If you want all transactions, set full_transaction = True. Otherwise, it will return the transaction, which only have erc20 token envolved
    # Due to the Limitation of the API, only 10000 transaction will be stored
    #it will return a json file:"Definer_erc20.json"
    def etherscan_reader_erc20(self,number = 10000,address = "0x8fFd2bD41E1AE6664FeDed043fA6fDc0AdFdA85a",full_transaction = False):
        with open('api_key.json', mode='r') as key_file:
            key = json.loads(key_file.read())['key']
        api = accounts.Account(address=address, api_key=key)
        self.transaction_erc20 = api.get_transaction_page(sort='desc',offset=number,erc20=True)
        transaction_action_input = api.get_transaction_page(sort='desc',offset=number)
        self.change_dictionary_erc20(transaction_action_input,full_transaction)
        with open("Definer_erc20.json","w")as outfile:
            json.dump(self.transaction_erc20, outfile)

    # Data cleaning for function:etherscan_reader
    def change_dictionary(self):
        for transaction in self.transaction:
            time = datetime.fromtimestamp(int(transaction["timeStamp"]))
            transaction["timeStamp"] = time.strftime("%m/%d/%Y, %H:%M:%S")
            if transaction["input"][2:10] in self.definer_function:
                transaction["input"] = self.definer_function[transaction["input"][2:10]]
            else:
                transaction["input"] = "Unknown"

    # Data cleaning for function: etherscan_reader_erc20
    def change_dictionary_erc20(self, action_input,full_transaction = False):
        new_d = {}
        ## Get action name
        for action in action_input:
            time = datetime.fromtimestamp(int(action["timeStamp"]))
            action["timeStamp"] = time.strftime("%m/%d/%Y, %H:%M:%S")
            if action["input"][2:10] in self.definer_function:
                action["input"] = self.definer_function[action["input"][2:10]]
                action["tokenName"] = 'Ethereum'
            else:
                action["input"] = "Unknown"
            new_d[action["hash"]] = action["input"]

        used_hash = []
        for transaction_erc20 in self.transaction_erc20:
            time = datetime.fromtimestamp(int(transaction_erc20["timeStamp"]))
            transaction_erc20["timeStamp"] = time.strftime("%m/%d/%Y, %H:%M:%S")
            if transaction_erc20["hash"] in new_d:
                transaction_erc20["input"] = new_d[transaction_erc20["hash"]]
            else:
                transaction_erc20["input"] = "Unknown"
            used_hash.append(transaction_erc20["hash"])

        if full_transaction !=False:
            for action in action_input:
                if action['hash'] not in action_input:
                    self.transaction_erc20.append(action)


    def find_all_keys(self,data):
        keys = set()
        for entry in data:
            try:
                for key in entry.keys():
                    keys.add(key)
            except:
                print(entry)
                print("Unexpected error:", entry, sys.exc_info()[0])
        return keys


    def json_to_csv(self,data,name):
        output = io.StringIO()
        csv_writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        count = 0
        header = self.find_all_keys(data)
        for entry in data:
            if count == 0:
                # Writing headers of CSV file
                csv_writer.writerow(list(header))
                count += 1
            try:
                values = []
                for key in header:
                    if key in entry:
                        values.append(entry[key])
                    else:
                        values.append(None)
                # Writing data of CSV file
                csv_writer.writerow(values)
            except:
                print(entry)
                print("Unexpected error:", entry, sys.exc_info()[0])

        text = output.getvalue().replace("\r","")
        text_file = open(name+".csv", "w")
        n = text_file.write(text)
        text_file.close()


## Wrapper
name = definer_data_collector()
name.etherscan_reader()
name.etherscan_reader_erc20()
with open('Definer.json') as f:
    data = json.load(f)
with open('Definer_erc20.json') as f:
    data1 = json.load(f)
name.json_to_csv(data,"Definer")
name.json_to_csv(data1,"Definer_erc20")