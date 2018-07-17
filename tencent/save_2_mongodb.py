#congding=utf-8

import pymongo
import json
import redis

def main():


    cli_redis = redis.StrictRedis(host='192.168.1.103', port=6379, db=0)

    mongocli = pymongo.MongoClient(host='localhost', port=27017)


    db = mongocli['tencent']

    table = db['tencent_job']

    while True:

        source, data = cli_redis.blpop(["tencent:items"])

        item = json.loads(data)
        table.insert(item)

        try:
            print u"Processing: %(name)s <%(link)s>" % item
        except KeyError:
            print u"Error procesing: %r" % item


if __name__ == '__main__':
    main()