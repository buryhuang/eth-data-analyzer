##This is the code for getting data from etherscan
import json
import io
import csv
import sys
import etherscan.accounts as accounts
from datetime import datetime
import boto3


##transfer  beabacc8    borrow  4b8a3529   repay  22867d78
# depositToken  338b5dea
# withdrawToken  9e281a98    withdrawAllToken  ae4dd0fc
# liquidate  86b9d81f
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
        return self.transaction

    # This is the function to get  Transaction with ERC_20 from the specific account/contract from etherscan
    # If you want all transactions, set full_transaction = True. Otherwise, it will return the transaction, which only have erc20 token envolved
    # Due to the Limitation of the API, only 10000 transaction will be stored
    #it will return a json file:"Definer_erc20.json"
    def etherscan_reader_erc20(self,number = 10000,address = "0x8fFd2bD41E1AE6664FeDed043fA6fDc0AdFdA85a",full_transaction = False):
        with open('api_key.json', mode='r') as key_file:
            key = json.loads(key_file.read())['key']
        api = accounts.Account(address=address, api_key=key)
        print("bury000")
        print(api)
        self.transaction_erc20 = api.get_transaction_page(sort='desc',offset=number,erc20=True)
        print("burytest")
        print(self.transaction_erc20)
        transaction_action_input = api.get_transaction_page(sort='desc',offset=number)
        self.change_dictionary_erc20(transaction_action_input,full_transaction)
        print(self.transaction_erc20)
        return self.transaction_erc20

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

def find_all_keys(data):
    keys = set()
    for entry in data:
        try:
            for key in entry.keys():
                keys.add(key)
        except:
            print(entry)
            print("Unexpected error:", entry, sys.exc_info()[0])
    return keys

def json_to_csv(data):
    output = io.StringIO()
    csv_writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
    
    count = 0
    header = find_all_keys(data)
    print(header)
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

    return output.getvalue()

def lambda_handler(event, context):
    print("bury starting")
    data_collector = definer_data_collector()
    erc20_transactions = data_collector.etherscan_reader_erc20()
    
    client = boto3.client('s3')
    client.put_object(Body=json_to_csv(erc20_transactions), Bucket='definerdatastore', Key='Definer_erc20.csv')
    
    return {
        'statusCode': 200,
        'body': 'returned %d' % len(erc20_transactions)
    }
