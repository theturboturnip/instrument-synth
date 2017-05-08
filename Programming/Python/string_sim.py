#!/usr/bin/env python
import math,sys

class Vec:
    x=0
    y=0

    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __add__(self,other):
        return Vec(self.x+other.x,self.y+other.y)
    def __sub__(self,other):
        return self.add(-other)
    def __mul__(self,fac):
        return Vec(self.x*fac,self.y*fac)
    def __div__(self,fac):
        return self.__mul__(1.0/fac)
    def __neg__(self):
        return Vec(-self.x,-self.y)

    def dupe(self):
        return Vec(self.x,self.y)
    
class StringPoint:
    pos=Vec(0,0)
    velocity=Vec(0,0)
    accel=Vec(0,0)

    def __init__(self,p,v,a):
        self.pos=p
        self.velocity=v
        self.accel=a

    def tick(self,dt):
        pos+=velocity*dt
        velocity+=accel*dt

    def dupe(self):
        return StringPoint(self.pos.dupe(),self.velocity.dupe(),self.accel.dupe())

class StringPointSet:
    points=[]

    def __init__(self,points=[]):
        self.points=points
    def __getitem__(self,index):
        return self.points[index]

    def dupe(self):
        dupe_points=[]
        for point in self.points:
            dupe_points.append(point.dupe())
        return StringPointSet(dupe_points)

class String:
    point_set=None
    original_length=0
    extension=0

    def __init__(self,num_points,length):
        points=[]
        x_pos=0.0
        for i in range(num_points):
            points.append(StringPoint(Vec(x_pos,0),Vec(0,0),Vec(0,0)))
            x_pos+=length*1.0/num_points
        self.point_set=StringPointSet
            
        self.original_length=length

    def tick(self,dt):
        self.apply_forces(dt)
        
        current_length=0
        previous_point_pos=Vec(0,0)
        for point in points:
            point.tick(dt)
            delta=point.pos-previous_point_pos
            current_length+=math.sqrt(delta.y**2+delta.x**2)
            previous_point_pos=point.pos
        self.extension=current_length-self.original_length
        
    def apply_forces(self,dt):
        pass

class PianoString(String):
    def apply_forces(self,dt):
        pass
    

def test(dt,ticks):
    string=PianoString()
    data=[]

    for i in range(ticks):
        data.append(string.point_set.dupe())
        string.tick(dt)

    return data

if __name__=="__main__":
    if len(sys.argv)!=3:
        print "Correct Usage: python ./string_sim.py <frequency> <tick count>"
        quit()
    dt=1.0/float(sys.argv[1])
    ticks=int(sys.argv[2])
    data=test(dt,ticks)
    
    
