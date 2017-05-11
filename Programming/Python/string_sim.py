#!/usr/bin/env python
import math,sys

class Vec:
    x=0
    y=0

    def __init__(self,x,y):
        self.x=x*1.0
        self.y=y*1.0
    def __add__(self,other):
        return Vec(self.x+other.x,self.y+other.y)
    def __sub__(self,other):
        return self.__add__(-other)
    def __mul__(self,fac):
        return Vec(self.x*fac,self.y*fac)
    def __div__(self,fac):
        return self.__mul__(1.0/fac)
    def __neg__(self):
        return Vec(-self.x,-self.y)
    def __str__(self):
        return "("+str(round(self.x,3))+","+str(round(self.y,3))+")"
    def __repr__(self):
        return str(self.x)+","+str(self.y)

    def dupe(self):
        return Vec(self.x,self.y)
    def mag(self):
        return math.sqrt(self.x**2+self.y**2)
    def dir(self):
        return self/self.mag()
    
class StringPoint:
    pos=Vec(0,0)
    velocity=Vec(0,0)
    accel=Vec(0,0)

    def __init__(self,p,v,a):
        self.pos=p
        self.velocity=v
        self.accel=a
    def __str__(self):
        return "p"+str(self.pos)+" v"+str(self.velocity)+" a"+str(self.accel)
    def __repr__(self):
        return self.__str__()

    def tick(self,dt):
        self.velocity+=self.accel*dt
        self.pos+=self.velocity*dt

    def dupe(self):
        return StringPoint(self.pos.dupe(),self.velocity.dupe(),self.accel.dupe())

class StringPointSet:
    points=[]

    def __init__(self,points=[]):
        self.points=points
    def __getitem__(self,index):
        return self.points[index]
    def __len__(self):
        return len(self.points)
    def __str__(self):
        to_print="|"
        #for point in self.points:
        to_print+=str(self.points[len(self.points)/2].pos)+"|"#str(round(point.pos.y,1))+"|"
        return to_print


    def dupe(self):
        dupe_points=[]
        for point in self.points:
            dupe_points.append(point.dupe())
        duped_point_set=StringPointSet(dupe_points)
        return duped_point_set

class String:
    point_set=None
    original_length=0

    adj_point_length=0
    extension=0
    force_constant=0
    mass_per_unit_length=0

    def __init__(self,num_points,length,force_constant,mass_per_unit_length):
        self.adj_point_length=length*1.0/num_points
        points=[]
        x_pos=0.0
        for i in range(num_points):
            points.append(StringPoint(Vec(x_pos,0),Vec(0,0),Vec(0,0)))
            x_pos+=self.adj_point_length
        self.point_set=StringPointSet(points)
            
        self.original_length=length
        self.force_constant=force_constant
        self.mass_per_unit_length=mass_per_unit_length

    def tick(self,dt):
        self.apply_forces(dt)
        
        """current_length=0
        previous_point_pos=Vec(0,0)
        for point in points:
            point.tick(dt)
            delta=point.pos-previous_point_pos
            current_length+=math.sqrt(delta.y**2+delta.x**2)
            previous_point_pos=point.pos
        self.extension=current_length-self.original_length"""
        for i in range(len(self.point_set)):
            self.point_set[i].tick(dt)

        for i in range(len(self.point_set)):
            self.point_set[i].accel=self.calculate_spring_force(i)/(self.mass_per_unit_length*self.adj_point_length)
    def calculate_spring_force(self,index):
        force=Vec(0,0)
        for i in range(max(index-1,0),min(index+2,len(self.point_set))):
            if (index==i):
                continue
            delta=self.point_set[i].pos-self.point_set[index].pos
            force+=delta.dir()*self.force_constant*(delta.mag()-self.adj_point_length)
            #print "Force iterate "+str(i)
        #print force
        return force #this may need to be multiplied by length or something
        
    def apply_forces(self,dt):
        pass

class PianoString(String):

    def __init__(self,num_points,length,force_constant,mass_per_unit_length,impulse_height):
        String.__init__(self,num_points,length,force_constant,mass_per_unit_length)

        for point in self.point_set:
            point.pos.y=math.sin(point.pos.x/length*math.pi)*impulse_height
        #self.point_set[impulse_point].pos.y=impulse_height
        #print self.point_set[impulse_point]
    
    def apply_forces(self,dt):
        self.point_set[0].accel=self.point_set[0].velocity=Vec(0,0)
        self.point_set[-1].accel=self.point_set[-1].velocity=Vec(0,0)
        #for point in self.point_set:
        #    point.velocity*=(0.999)
        pass
    

def test(dt,ticks,output_file_path):
    string=PianoString(100,1,100000,0.25,0.05)
    data=[None]
    output_file=None
    if (output_file_path!=None):
        output_file=open(output_file_path,"w")

    for i in range(ticks):
        current_tick_data=string.point_set.dupe()
        #print str(current_tick_data)
        mid_point=int(len(current_tick_data)*.5-1)
        
        data[0]=current_tick_data
        if (output_file!=None):
            data_string=""
            for point in current_tick_data:
                data_string+=repr(point.pos)+" "
            output_file.write(data_string+"\n")
        else:
            if i!=0 and math.copysign(1,current_tick_data[mid_point].pos.y) != math.copysign(1,data[len(data)-1][mid_point].pos.y):
                print i,current_tick_data[mid_point]
        if (i%100)==0:
            print i,current_tick_data[mid_point]   
                
        string.tick(dt)

    if output_file!=None:
        output_file.close()
        
    return data

if __name__=="__main__":
    if len(sys.argv)<3:
        print "Correct Usage: python ./string_sim.py <frequency> <tick count> <output_file (optional)>"
        quit()
    print StringPoint(Vec(1,1),Vec(1,1),Vec(1,1)).dupe()
    print Vec(0,1).mag()
    print Vec(1,1).mag()
    dt=1.0/float(sys.argv[1])
    ticks=int(sys.argv[2])
    output_file=None
    if len(sys.argv)==4:
        output_file=sys.argv[3]
    data=test(dt,ticks,output_file)
    
    
