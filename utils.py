import platforms

def clamp(v,low,high):
    return min(high,max(low,v))
def can_jump(x,y,obj_id):
    #TODO: poner con bloques escaleras y eso
    offset = 5
    return y >= 720-19*6 or platforms.collision_top(obj_id,offset)
