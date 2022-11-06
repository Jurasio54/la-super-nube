from threads import ThreadAsync

ANIMATING = False


def animating(func=None,bot=None,ev=None):
    while ANIMATING:
        if func:
            func(bot,ev)

def start_async(func=None,bot=None,ev=None,eventloop=None):
    tasync = ThreadAsync(loop=eventloop,targetfunc=animating,args=(func,bot,ev))
    tasync.start()