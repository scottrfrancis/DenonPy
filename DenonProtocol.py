import re

class DenonProtocol:
    protocol = { 'Power': 'PW'
                ,'Mute':  'MU'
                ,'Video': 'SV'
                # ,'Volume': 'MV'
                ,'VolumeMax': 'MVMAX\s'
                ,'VolumeLevel': 'MV'
    }

    state = {}

    def makeQuery(self, parameters):
        queries = [];

        while parameters:
            if parameters[0] in self.protocol.keys():
                queries.append(self.protocol[parameters[0]] + "?")
            parameters = parameters[1:]

        return queries

    def makeCommands(self, params):
        commands = []

        for c, p in params.items():
            if c in self.protocol.keys():
                commands.append(str(list(self.protocol.values())[list(self.protocol.keys()).index(c)] + p))

        return commands

    def parseEvents(self, events):
        has_changed = False

        # while events:
        #     ev = events[0][0:2]
        #     if ev in self.protocol.values():
        #         val = ''
        #         ob = events[0][2:]
        #         key = list(self.protocol.keys())[list(self.protocol.values()).index(ev)]

        #         if key in self.state.keys():
        #             val = self.state[key]

        #         if ob != val:
        #             has_changed = True
        #             self.state[key] = ob

        #     events = events[1:]

        for rk in list(map(lambda k: re.compile(k), list(self.protocol.values()))):
            print("searching " + k)
            matches = [ x for x in list(map(lambda e: rk.match(e), events)) 
                if x != None and x.start() == 0 ] 
            print(" found " + matches)

            l = len(matches)
            if l > 0:
                l -= 1
                # there could be more than one match, so take the 'last' as most current
                e = matches[l].end()
                key = matches[l].string[matches[l].start():e]
                ob = matches[l].string[e:]
                print("setting " + key + ":" + ob)

                has_changed = True
                self.state[key] = ob

        self.normalizeVolume()

        return has_changed
    
    def normalizeVolume(self):
        max = 98
        try:
            max = self.state.pop("VolumeMax")
        except:
            pass

        try:
            level = self.state.pop("VolumeLevel")
            vol = int((int(level[0:2])/int(max))*100)
            self.state['Volume'] = vol
        except:
            pass


    def getState(self):
        return self.state
