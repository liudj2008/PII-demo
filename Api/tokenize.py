# transform a single customer record
# {"id": XXX, "name": XXX, "ssn": XXX, "address": XXX}
import json
from DataTransform.data_transform import data_transform
from Redis.redis import Redis


def tokenize(conn: Redis, data_catalog: str, data: json, reverse: bool):
    dict_result = dict()
    for key in data.keys():
        res = conn.get(data_catalog, key, reverse)
        if res:
            dict_result[key] = data_transform(data[key], res)
        else:
            dict_result[key] = data[key]

    return dict_result
