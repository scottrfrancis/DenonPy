
class DenonProtocol:
    protocol = { 'Power': 'PW'
                ,'Mute':  'MU'
                ,'Video': 'SV'
                ,'Volume': 'MV'
    }
    state = {}

    # def __init__():

    def makeQuery(self, parameters):
        queries = [];

        while parameters:
            if parameters[0] in self.protocol.keys():
                queries.append(self.protocol[parameters[0]] + "?")
            parameters = parameters[1:]

        return queries

    def parseEvents(self, events):
        while events:
            ev = events[0][0:2]
            if ev in self.protocol.values():
                self.state[ self.protocol.keys()[self.protocol.values().index(ev)] ] = events[0][2:]

            events = events[1:]


    def getState(self):
        return self.state
