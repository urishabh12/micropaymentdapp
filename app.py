import os
import sys
from werkzeug.utils import secure_filename
from flask import Flask, send_from_directory, render_template, request, redirect, url_for
from web3 import Web3, HTTPProvider
import json
import ipfsapi

web3=Web3(HTTPProvider('http://localhost:8101'))
ERC20_ABI = json.loads('[{"constant": false,"inputs": [{"name": "spender","type": "address"},{"name": "value","type": "uint256"}],"name": "approve","outputs": [{"name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function","signature": "0x095ea7b3"},{"constant": true,"inputs": [],"name": "totalSupply","outputs": [{"name": "","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function","signature": "0x18160ddd"},{"constant": false,"inputs": [{"name": "from","type": "address"},{"name": "to","type": "address"},{"name": "value","type": "uint256"}],"name": "transferFrom","outputs": [{"name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function","signature": "0x23b872dd"},{"constant": false,"inputs": [{"name": "spender","type": "address"},{"name": "addedValue","type": "uint256"}],"name": "increaseAllowance","outputs": [{"name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function","signature": "0x39509351"},{"constant": true,"inputs": [{"name": "","type": "address"},{"name": "","type": "uint256"}],"name": "transactr","outputs": [{"name": "to","type": "address"},{"name": "value","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function","signature": "0x61b908dd"},{"constant": true,"inputs": [{"name": "owner","type": "address"}],"name": "balanceOf","outputs": [{"name": "","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function","signature": "0x70a08231"},{"constant": false,"inputs": [{"name": "spender","type": "address"},{"name": "subtractedValue","type": "uint256"}],"name": "decreaseAllowance","outputs": [{"name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function","signature": "0xa457c2d7"},{"constant": true,"inputs": [{"name": "","type": "address"},{"name": "","type": "uint256"}],"name": "transacts","outputs": [{"name": "to","type": "address"},{"name": "value","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function","signature": "0xa4748845"},{"constant": false,"inputs": [{"name": "to","type": "address"},{"name": "value","type": "uint256"}],"name": "transfer","outputs": [{"name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function","signature": "0xa9059cbb"},{"constant": true,"inputs": [{"name": "owner","type": "address"},{"name": "spender","type": "address"}],"name": "allowance","outputs": [{"name": "","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function","signature": "0xdd62ed3e"},{"inputs": [],"payable": false,"stateMutability": "nonpayable","type": "constructor","signature": "constructor"},{"anonymous": false,"inputs": [{"indexed": true,"name": "from","type": "address"},{"indexed": true,"name": "to","type": "address"},{"indexed": false,"name": "value","type": "uint256"}],"name": "Transfer","type": "event","signature": "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"},{"anonymous": false,"inputs": [{"indexed": true,"name": "owner","type": "address"},{"indexed": true,"name": "spender","type": "address"},{"indexed": false,"name": "value","type": "uint256"}],"name": "Approval","type": "event","signature": "0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925"},{"constant": false,"inputs": [{"name": "_from","type": "address"},{"name": "_to","type": "address"},{"name": "_value","type": "uint256"}],"name": "send","outputs": [],"payable": false,"stateMutability": "nonpayable","type": "function","signature": "0x0779afe6"},{"constant": false,"inputs": [{"name": "num","type": "uint256"}],"name": "createmicro","outputs": [{"name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function","signature": "0xeec07c2e"}]')
erc20 = web3.eth.contract(address="0xb402a0ffA20EDF4d4799EA0Ac5a5Fff9Ee95AC83", abi=ERC20_ABI)
app = Flask(__name__)
accounts={'rishabh':[web3.eth.accounts[0], 'redhat'],
'ashutosh':[web3.eth.accounts[1], 'redhat'],
'ankur':[web3.eth.accounts[2], 'redhat'],
'baban':[web3.eth.accounts[3], 'redhat'],
'chaman':[web3.eth.accounts[4], 'redhat'],
'raman':[web3.eth.accounts[5], 'redhat'],
'raj':[web3.eth.accounts[6], 'redhat']}

web3.eth.defaultAccount = accounts['rishabh'][0]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        try:
            r = request.form['isMobile']
        except:
            r = None
        username = request.form['username']
        password = request.form['password']
        if username in accounts.keys():
            if accounts[username][1] == password:
                if r is not None:
                    return json.dumps({'message':'success'})
                return redirect(url_for('home', username=username))
            else:
                if r is not None:
                    return json.dumps({'message':'Error'})
                return render_template('index.html', message="Wrong username or password")
        else:
            if r is not None:
                    return json.dumps({'message':'Error'})
            return render_template('index.html', message="Wrong username or password")
    return render_template('index.html')

@app.route('/home/<string:username>', methods=['GET', 'POST'])
def home(username):
    uname = accounts[username][0]
    balance = erc20.functions.balanceOf(uname).call()
    if request.method == "POST":
        try:
            r = request.form['isMobile']
        except:
            r = None
        flag = 0
        to = request.form['to']
        value = int(request.form['value'])
        print("%s %s" %(to, value))
        if value>balance:
            if r is not None:
                return json.dumps({'message':'Error'})
            return redirect(url_for('home', username=username, message="Insufficient Balance"))
        to = accounts[to][0]
        erc20.functions.send(uname, to, value).transact()
        if r is not None:
            return json.dumps({'message':'success'})
        return redirect(url_for('home', username=username))
    transactionss = []
    transactionsr = []
    for i in range(150):
        try:
            transactionss.append(erc20.functions.transacts(uname, i).call())
        except:
            break
    for i in range(150):
        try:
            transactionsr.append(erc20.functions.transactr(uname, i).call())
        except:
            break
    try:
        r = request.form['isMobile']
    except:
        r = None
    if r is not None:
        d = {'sent':transactionss, 'received':transactionsr, 'balance':balance}
        d = json.dumps(d)
        return d
    return render_template('home.html', transactionss=transactionss, transactionsr = transactionsr, balance=balance)

@app.route('/mobile/<string:username>')
def mobile(username):
    uname = accounts[username][0]
    balance = erc20.functions.balanceOf(uname).call()
    transactionss = []
    transactionsr = []
    for i in range(150):
        try:
            transactionss.append(erc20.functions.transacts(uname, i).call())
        except:
            break
    for i in range(150):
        try:
            transactionsr.append(erc20.functions.transactr(uname, i).call())
        except:
            break
    d = {'sent':transactionss, 'received':transactionsr, 'balance':balance}
    d = json.dumps(d)
    return d

app.run(host='0.0.0.0')