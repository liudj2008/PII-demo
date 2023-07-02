import json
import redis


class Redis:
    def __init__(self):
        self.conn = redis.Redis()

    def set(self):
        with open('Constants/RedisDataForTokenize', 'r') as file:
            data = json.loads(file.read())
            self.conn.json().set('tokenize', '$', data)

        with open('Constants/RedisDataForDeTokenize', 'r') as file:
            data = json.loads(file.read())
            self.conn.json().set('detokenize', '$', data)

    def get(self, data_category: str, key: str, reverse: bool):
        search_results = self.conn.json().get('tokenize', f'$.{data_category}.{key}') if not reverse \
            else self.conn.json().get('detokenize', f'$.{data_category}.{key}')
        if search_results:
            return search_results[0]
        return None
