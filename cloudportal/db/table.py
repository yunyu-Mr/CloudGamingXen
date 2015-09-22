import settings
# lod = []

def get_table():
    return settings.lod

def insert_lod(lod, record):
    lod.append(record)

# query_lod(lod, lambda r:int(r['Year'])==1998 and int(r['Priority']) > 2)
def query_lod(lod, filter=None, sort_keys=None):
    if filter is not None:
        lod = (r for r in lod if filter(r))
    if sort_keys is not None:
        lod = sorted(lod, key=lambda r:[r[k] for k in sort_keys])
    else:
        lod = list(lod)
    return lod

def lookup_lod(lod,  **kw):
    for row in lod:
        for k,v in kw.iteritems():
            if row[k] != str(v): break
        else:
            return row
    return None



class Onlytable:
    """ A python Onlytable """

    class __impl:
        """ Implementation of the Onlytable interface """

        def __init__(self):
            self.lod = []

        def get_table(self):
            # self.lod.append(self.lod[-1]+1)
            return self.lod

        def insert_lod(self, record):
            self.lod.append(record)

        def query_lod(self, filter=None, sort_keys=None):
            if filter is not None:
                self.lod = (r for r in self.lod if filter(r))
            if sort_keys is not None:
                self.lod = sorted(self.lod, key=lambda r:[r[k] for k in sort_keys])
            else:
                self.lod = list(self.lod)
            return self.lod

        def lookup_lod(self, **kw):
            for row in self.lod:
                for k,v in kw.iteritems():
                    if row[k] != str(v): break
                else:
                    return row
            return None

        def spam(self):
            """ Test method, return Onlytable id """
            return id(self)

    # storage for the instance reference
    __instance = None

    def __init__(self):
        """ Create Onlytable instance """
        # Check whether we already have an instance
        if Onlytable.__instance is None:
            # Create and remember instance
            Onlytable.__instance = Onlytable.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_Onlytable__instance'] = Onlytable.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)