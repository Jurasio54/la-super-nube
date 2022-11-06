import threading
from utils import createID
import asyncio

class StoppableThread(threading.Thread):
    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

class ThreadAsync(object):
    def __init__(self,loop=None,targetfunc=None,args=(),update=None):
        self.id = createID(12)
        self.func = targetfunc
        self.update = update
        self.tstore = {}
        self.args = args
        self.loop = loop
        pass
    def tasync(self):
        try:
            self.loop.create_task(self.func(*self.args))
        except:pass
    def start(self):
        self.handle = threading.Thread(target=self.tasync)
        self.handle.start()
    def stop(self):
        self.handle.join()
        pass
    def store(self,name,obj):
        self.tstore[name] = obj
    def getStore(self,name):
        try:
            return self.tstore[name]
        except:pass
        return None

class Thread(object):
    def __init__(self,targetfunc=None,args=(),update=None):
        self.id = createID(12)
        self.handle = threading.Thread(target=targetfunc, args=args)
        self.update = update
        self.tstore = {}
        pass
    def start(self):
        self.handle.start()
    def stop(self):
        self.handle.join()
        pass
    def store(self,name,obj):
        self.tstore[name] = obj
    def getStore(self,name):
        try:
            return self.tstore[name]
        except:pass
        return None