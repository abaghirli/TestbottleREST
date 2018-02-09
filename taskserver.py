from bottle import response, request
from bottle import post, get, put, delete
from pymongo import MongoClient, ReturnDocument
from bson import json_util
import bottle

app = application = bottle.default_app()
client = MongoClient('localhost', 27017)
mydb = client.my_database
MyDataCollection = mydb.test_collection

@post('/records/post')
def route_create():
    '''Handles name creation'''
    try:
        # parse input data
        try:
            data = request.json
        except:
            raise ValueError
        if data is None:
            raise ValueError
        for key in data:
            record = data[key]
        # check for existence
            if MyDataCollection.find({'id': record['id']}).count():
                raise KeyError
    except ValueError:
        # if bad request data, return 400 Bad Request
        response.status = 400
        return
    except KeyError:
        # if record already exists, return 409 Conflict
        response.status = 409
        return
    # add records
    insertedrecords={}
    for key in data:
        result = MyDataCollection.insert_one(data[key])
        insertedrecords[str(result.inserted_id)] = data[key]
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json_util.dumps({'status': 'success', 'records': insertedrecords})

@get('/records/get')
def route_get():
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    recs = {}
    records = MyDataCollection.find()
    for el in (records):
        recs[str(el['_id'])] = el

    return json_util.dumps({'status': 'success', 'records': recs})

@put('/records/put')
def route_update():
    try:
        # parse input data
        try:
            data = request.json
        except:
            raise ValueError
        if data is None:
            raise ValueError
        for key in data:
            record = data[key]
        # check for existence
            if not MyDataCollection.find({'id': record['id']}).count():
                raise KeyError
    except ValueError:
        # if bad request data, return 400 Bad Request
        response.status = 400
        return
    except KeyError:
        # if record already exists, return 409 Conflict
        response.status = 409
        return
    # add records
    updatedrecords={}
    for key in data:
        result = MyDataCollection.find_one_and_update(
            {'id': data[key]['id']},
            {'$set': data[key]},
            return_document=ReturnDocument.AFTER
        )
        updatedrecords[str(data[key]['id'])] = result
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json_util.dumps({'status': 'success', 'records': updatedrecords})

@delete('/records/delete')
def route_delete():
    try:
        # parse input data
        try:
            data = request.json
        except:
            raise ValueError
        if data is None:
            raise ValueError
    except ValueError:
        # if bad request data, return 400 Bad Request
        response.status = 400
        return
    # add records
    updatedrecords={}
    for key in data:
        result = MyDataCollection.delete_many(data[key])
        updatedrecords[str(data[key]['id'])] = {'count': result.deleted_count, 'filter':data[key]}
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json_util.dumps({'status': 'success', 'records': updatedrecords})

bottle.run(host='localhost', port=8080)