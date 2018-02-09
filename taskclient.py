import requests
import urllib.parse as upars
import json
import base64

def makerequest():
    host= input('enter host:')
    port= input('enter port:')
    if not host and not port:
        addr = 'http://localhost:8080/records/'
    else: addr = host+port
    while True:
        method = input("Method? (c)reate, (u)pdate, (l)ist, (v)iew, (d)elete, (e)xit: ")
        if method == 'e':
            break
        if method == 'l':
            url = upars.urljoin(addr,'get')
            resp = requests.get(url)
            print(resp.json())
        if method in ['c']:
            url = upars.urljoin(addr, 'post')
            attrlist=[('id', 'int'), ('price', 'float'), ('Description', 'string'), ('filename', 'file')]
            recs = get_records(attrlist)
            headers = {'Content-type': 'application/json'}
            resp = requests.post(url, data=json.dumps(recs), headers=headers)
            print(resp.json())

def get_records(attrlist):
    recnum = int(input('Enter number of records: '))
    recs = {}
    for i in range(recnum):
        recs[i] = get_record(attrlist)
    return recs

def get_record(attrlist):
    rec = {}
    for attr, mytype in attrlist:
        if mytype == 'int':
            line = input('enter '+attr+' or "abort": ')
            if line == 'abort':
                return 0
            else:
                rec[attr] = int(line)
        if mytype == 'float':
            line = input('enter '+attr+' or "abort": ')
            if line == 'abort':
                return 0
            else:
                rec[attr] = float(line)
        if mytype == 'string':
            line = input('enter '+attr+' or "abort": ')
            if line == 'abort':
                return 0
            else:
                rec[attr] = str(line)
        if mytype == 'file':
            line = input('enter '+attr+' or "abort": ')
            if line == 'abort':
                return 0
            else:
                rec[attr] = str(base64.encodebytes(open(line, 'rb').read()))
    return rec

def maketests():
    addr = 'http://localhost:8080/records/'
    records = {
        '0': {
            'id': 1,
            'price': 10.20,
            'description': 'apple',
            'file': str(base64.encodebytes(open('testfile1', 'rb').read()))
        },
        '1': {
            'id': 2,
            'price': 5.44,
            'description': 'potato',
            'file': str(base64.encodebytes(open('testfile1', 'rb').read()))
        },
        '2': {
            'id': 3,
            'price': 18.52,
            'description': 'banana',
            'file': str(base64.encodebytes(open('testfile1', 'rb').read()))
        },
    }
    test_create(addr, records)
    test_list(addr)
    records = {
        '0': {
            'id': 1,
            'description': 'red apple'
        },
        '1': {
            'id': 3,
            'price': 20.00
        },
    }
    test_update(addr, records)
    test_list(addr)
    records = {
        '0': {
            'id': 2
        }}
    test_delete(addr, records)
    test_list(addr)
    test_delete(addr, {})

def test_create(addr, records):
    url = upars.urljoin(addr, 'post')
    headers = {'Content-type': 'application/json'}
    resp = requests.post(url, data=json.dumps(records), headers=headers)
    respdict=resp.json()
    print("INSERT TEST")
    print(respdict['status'])
    for rec in respdict['records']:
        print('id: ' + str(respdict['records'][rec]['id']))
        print('price: ' + str(respdict['records'][rec]['price']))
        print('description: ' + respdict['records'][rec]['description'])
        print('filedata in base64: ' + respdict['records'][rec]['file'])

def test_update(addr, records):
    url = upars.urljoin(addr, 'put')
    headers = {'Content-type': 'application/json'}
    resp = requests.put(url, data=json.dumps(records), headers=headers)
    respdict = resp.json()
    print("UPDATE TEST")
    print(respdict['status'])
    for rec in respdict['records']:
        print(str(respdict['records'][rec]))

def test_delete(addr, records):
    url = upars.urljoin(addr, 'delete')
    records = {
        '0': {
            'id': 2
        }}
    headers = {'Content-type': 'application/json'}
    resp = requests.delete(url, data=json.dumps(records), headers=headers)
    respdict = resp.json()
    print("DELETE TEST")
    print(respdict['status'])
    for rec in respdict['records']:
        print('for filter: ' + str(respdict['records'][rec]['filter']))
        print('deleted count is: ' + str(respdict['records'][rec]['count']))

def test_list(addr):
    url = upars.urljoin(addr, 'get')
    resp = requests.get(url)
    respdict = resp.json()
    print("LIST TEST")
    print(respdict['status'])
    for rec in respdict['records']:
        print('id: ' + str(respdict['records'][rec]['id']))
        print('price: ' + str(respdict['records'][rec]['price']))
        print('description: ' + respdict['records'][rec]['description'])
        print('filedata in base64: ' + respdict['records'][rec]['file'])

if __name__ == "__main__":
    maketests()
    #makerequest()