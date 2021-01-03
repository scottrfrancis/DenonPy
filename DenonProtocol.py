import functools
import re

class DenonProtocol:
    def __init__(self):
        self.protocol = [
            { 'state-key':  "Power",            # publicly visible reported/desired name
                'tag2':       "PW",               # two letter Command defined by denon
                'parser': self.parseSimpleArg     # function to parse the event
            },
            { 'state-key':  "Mute", 
                'tag2':       'MU',
                'parser': self.parseSimpleArg
            },
            { 'state-key':  'Volume',
                'tag2':       'MV',
                'parser': self.volumeParser
            }
        ]
 
        self.volMax = 695                          # default in case max message never comes

        self.state = {}


    # simple parser strips the tag from the event and considers the remainder of the event
    #   to be the argument
    def parseSimpleArg(self, tag, event):
        return event[len(tag):] if event.find(tag, 0) >= 0 else ""

    # volume is tricky... it's a compound thing, where level and max are reported as separate
    #   events, but always paired
    def volumeParser(self, tag, event):
        # first strip the comand tag
        arg = self.parseSimpleArg(tag, event)

        # check for vol max and update the member var ***AS SIDE EFFECT***
        maxArg = self.parseSimpleArg("MAX ", arg)
        if maxArg:
            self.volMax = int(maxArg)/(10**(len(maxArg) - 2))
            return ""                       # squelch the event

        # arg has the volume data -- but could be 2 or 3 digits
        try:
            level = int(arg)/(10**(len(arg) - 2))
            percent = (level/self.volMax)*100
            return str(int(percent))
        except:
            return ""

    def makeQuery(self, parameters):
        queries = list(map(lambda x: x['tag2'] + "?", [x for x in self.protocol if x['state-key'] in parameters]))
        print("made query " + str(queries) + " from " + str(parameters))
        return queries

    def makeCommands(self, params):
        commands = list(map(lambda c: c['tag2'] + params[c['state-key']].upper(), 
            [ x for x in self.protocol if x['state-key'] in params.keys() ] ))
        return commands

    def parseEvents(self, events):
        has_changed = False

        if len(events) <= 0:
            return has_changed

        while events:
            e = events[0]
            t2 = e[:2]
            protos = [ x for x in self.protocol if x['tag2'] == t2 ]
            if protos:
                val = protos[0]['parser'](t2, e)

                if val:
                    self.state[protos[0]['state-key']] = val
                    has_changed = True

            events = events[1:]

        return has_changed
    

    def getState(self):
        return self.state
