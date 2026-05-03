import platforms


def clamp(v,low,high):
    return min(high,max(low,v))
def can_jump(x,y,*args):
    #TODO: poner con bloques escaleras y eso
    return y >= 720-19*6 or platforms.collision_top(x,y)[0]
