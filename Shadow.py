import json

# class Shadow:
#     @staticmethod
#     def hello():
#         return 'hello'
#
#     @staticmethod
def makeStatePayload(type, parameters):
    payload = {'state': {type: parameters}}
    return json.dumps(payload)
