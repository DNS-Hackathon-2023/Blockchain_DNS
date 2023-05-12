#!/usr/bin/env python3

#############################################################################################
#
#   res_bcdns.py  -- a class that provides blockchain connection and transaction execution
#
#           (c)2023 Joseph Gersch <jgersch@invykta.com>
#
#           Permission to use, copy, modify, and distribute this software and its
#           documentation for any purpose with or without fee is hereby granted,
#           provided that the above copyright notice and this permission notice
#           appear in all copies.
#
#           THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#           WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#           MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#           ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#           WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#           ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
#           OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
#############################################################################################

import json
import sys
sys.path.insert(1, '../')   # otherwise python won't find wallet.py
from applications.utils.wallet import Wallet
from dotenv import load_dotenv
import os
from web3 import Web3


#############################################################################################
#   BCDNS class and methods
#############################################################################################

class BCDNS:

    def __init__(self, walletName, passPhrase):
        self.w3 = None
        self.contract = None
        self.wallet = None
        self.account = ''
        self.nonce = 0
        self.accountBalance = 0
        self.accountBalanceEther = 0.0
        self.network = ''
        self.estimatedGas = 0
        self.totalEstimatedGas = 0
        self.txnHash = 0

        self.initWallet(walletName, passPhrase)
        self.initBC()


    #########################################################################################
    #   Method to connect to wallet for account number and private key
    #########################################################################################

    def initWallet(self, walletName, passPhrase):
        try:
            self.wallet = Wallet(walletName, passPhrase)
            self.account = self.wallet.get_account()
        except KeyError:
            print("**** Error:", self.walletName, "does not exist; program terminated\n")
            exit(1)

    #########################################################################################
    #   Method to connect to blockchain and DDNS smart contract, initialize nonce
    #########################################################################################

    def initBC(self):
        load_dotenv()

        try:
            self.w3 = Web3(Web3.HTTPProvider(os.getenv('BC_PROVIDER')))  # 'http://127.0.0.1:8545'))
            if not self.w3.isConnected(): raise Exception
            self.network = os.getenv('NETWORK')
            ADDRESS = os.getenv('CONTRACT_ADDRESS')
            with open(os.getenv('ABI_FILE'), "r") as myfile:
                data = myfile.read()
            obj = json.loads(data)
            self.contract = self.w3.eth.contract(address=ADDRESS, abi=obj["abi"])
            self.nonce = self.w3.eth.getTransactionCount(self.account)  # initialize nonce needed for each transaction
            self.accountBalance =  self.w3.eth.getBalance(self.wallet.account)
            self.accountBalanceEther = self.w3.fromWei(self.accountBalance, "ether")

        except Exception as err:
            print("**** Error: unable to connect to blockchain; program terminated\n")
            print(err)
            exit(1)


    #########################################################################################
    #   Utilities to  estimate gas, sign & execute transactions, and wait for a blockchain transaction.
    #########################################################################################

    def estimateGas(self, txn):
        self.estimatedGas = self.w3.eth.estimateGas(txn)
        print ("estimated gas", self.estimatedGas)
        self.totalEstimatedGas += self.estimatedGas
        return self.estimatedGas

    def buildTXNDict(self):
        txnDict = {
            'from': self.wallet.account,
            'nonce': self.nonce,
            #'gas': 500000
        }
        if self.network == 'ganache':
            txnDict['gasPrice'] = 2000000000
        elif self.network == 'sepolia':
            txnDict['gasPrice'] = 2000000000
        elif self.network == "goerli":
            txnDict['maxFeePerGas'] = 7660669988859
        elif self.network == "arbitrum":
            txnDict['gasPrice'] = 100000000

        else:
            print("bad blockchain network")
            exit(1)
        return txnDict

    def execTXN(self, txn, wait):
        signed_txn = self.wallet.sign_txn(self.w3, txn)
        self.txnHash = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        self.nonce += 1
        if wait:
            txn_receipt = self.w3.eth.wait_for_transaction_receipt(self.txnHash)

    def flushTXN(self):
        if self.txnHash:
            txn_receipt = self.w3.eth.wait_for_transaction_receipt(self.txnHash)
            self.txnHash = 0

