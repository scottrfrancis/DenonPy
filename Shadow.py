import json

# class Shadow:
#     @staticmethod
#     def hello():
#         return 'hello'
#
#     @staticmethod
def makeStatePayload(parameters):
    # payload = {'state': {type: parameters}}
    # set BOTH desired and reported
    payload = {'state': {
                    'desired': parameters,
                    'reported': parameters }}
    return json.dumps(payload)
