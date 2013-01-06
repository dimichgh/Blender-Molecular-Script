from time import clock

def vec_normalize(vec):
    vec_lenght = (vec[0]**2 + vec[1]**2 + vec[2]**2)**0.5
    if vec_lenght == 0:
        return ((0,0,0))
    else:
        return ((vec[0] / vec_lenght),(vec[1] / vec_lenght),(vec[2] / vec_lenght))

def triangle_normal(a,b,c):
    u = [b[0] - a[0],b[1] - a[1],b[2] - a[2]]
    v = [c[0] - a[0],c[1] - a[1],c[2] - a[2]]
    c = [(u[1] * v[2] - u[2] * v[1]),(u[2] * v[0] - u[0] * v[2]),(u[0] * v[1] - u[1] * v[0])]
    l = (c[0]**2 + c[1]**2 + c[2]**2)**0.5
    normal = [c[0] / l,c[1] / l,c[2] / l]
    return normal
def cross_product(u,v):
    cross = [(u[1] * v[2] - u[2] * v[1]),(u[2] * v[0] - u[0] * v[2]),(u[0] * v[1] - u[1] * v[0])]
    return cross
def dot_product(u,v):
    dot = (u[0] * v[0]) + (u[1] * v[1]) + (u[2] * v[2])
    return dot
def plane_intersec(a,vn,p0,p1):
    numerator = (vn[0] * (a[0] - p0[0])) + (vn[1] * (a[1] - p0[1])) + (vn[2] * (a[2] - p0[2]))
    denominator = (vn[0] * (p1[0] - p0[0])) + (vn[1] * (p1[1] - p0[1])) + (vn[2] * (p1[2] - p0[2]))
    if denominator == 0:
        bool = False
        pintersec_point = [0,0,0]
    else:
        ri = (numerator / denominator)
        if ri > 1 or ri < 0:
            bool = False
            pi=[0,0,0]
        else:   
            vl = [(p1[0] - p0[0]) * ri,(p1[1] - p0[1]) * ri,(p1[2] - p0[2]) * ri]
            intersec_point = [p0[0] + vl[0],p0[1] + vl[1],p0[2] + vl[2]]
            bool = True
    return bool,intersec_point

def triangle_intersec(a,u,v,vn,p0,p1):
    numerator=(vn[0]*(a[0]-p0[0]))+(vn[1]*(a[1]-p0[1]))+(vn[2]*(a[2]-p0[2]))
    denominator=(vn[0]*(p1[0]-p0[0]))+(vn[1]*(p1[1]-p0[1]))+(vn[2]*(p1[2]-p0[2]))
    if denominator == 0:
        bool = False
        intersec_point = [0,0,0]
    else:
        ri = (numerator/denominator)
        if ri > 1 or ri < 0:
            bool = False
            intersec_point = [0,0,0]
        else:   
            vl = [(p1[0] - p0[0]) * ri,(p1[1] - p0[1]) * ri,(p1[2] - p0[2]) * ri]
            pi = [p0[0] + vl[0],p0[1] + vl[1],p0[2] + vl[2]]
            w = [pi[0]-a[0],pi[1]-a[1],pi[2]-a[2]]
            tdenominator = ((u[0] * v[0] + u[1] * v[1] + u[2] * v[2])**2) - ((u[0] * u[0] + u[1] * u[1] + u[2] * u[2]) * (v[0] * v[0] + v[1] * v[1] + v[2] * v[2]))
            si = (((u[0] * v[0] + u[1] * v[1] + u[2] * v[2]) * (w[0] * v[0] + w[1] * v[1] + w[2] * v[2])) - ((v[0] * v[0] + v[1] * v[1] + v[2] * v[2]) * (w[0] * u[0] + w[1] * u[1] + w[2] * u[2]))) / tdenominator
            ti = (((u[0] * v[0] + u[1] * v[1] + u[2] * v[2]) * (w[0] * u[0] + w[1] * u[1] + w[2] * u[2])) - ((u[0] * u[0] + u[1] * u[1] + u[2] * u[2]) * (w[0] * v[0] + w[1] * v[1] + w[2] * v[2]))) / tdenominator
            tsi=si+ti
            if (si >=0 and ti >=0)and tsi <= 1:
                intersec_point = pi
                bool = True
            else:
                intersec_point = [0,0,0]
                bool = False
    return bool,intersec_point

   
def collision_response(obj1_loc,obj1_prevloc,obj1_mass,obj1_coefres,obj1_coeffric,obj2_loc,obj2_prevloc,obj2_mass,obj2_coefres,obj2_coeffric):
    avg_coeffric = 0.2 #(obj1_coeffric + obj2_coeffric) / 2
    avg_coefres = 0.3 #(obj1_coefres + obj2_coefres) / 2
    col1_normal = vec_normalize([(obj1_loc[0] - obj2_loc[0]),(obj1_loc[1] - obj2_loc[1]),(obj1_loc[2] - obj2_loc[2])])
    col2_normal = vec_normalize([(obj2_loc[0] - obj1_loc[0]),(obj2_loc[1] - obj1_loc[1]),(obj2_loc[2] - obj1_loc[2])])
    obj1_mult = dot_product(col1_normal,(obj1_prevloc[0] - obj1_loc[0],obj1_prevloc[1] - obj1_loc[1],obj1_prevloc[2] - obj1_loc[2]))
    obj2_mult = dot_product(col2_normal,(obj2_prevloc[0] - obj2_loc[0],obj2_prevloc[1] - obj2_loc[1],obj2_prevloc[2] - obj2_loc[2]))
    obj1_point = [obj1_prevloc[0] - (obj1_mult * col1_normal[0]),obj1_prevloc[1] - (obj1_mult * col1_normal[1]),obj1_prevloc[2] - (obj1_mult * col1_normal[2])]
    obj2_point = [obj2_prevloc[0] - (obj2_mult * col2_normal[0]),obj2_prevloc[1] - (obj2_mult * col2_normal[1]),obj2_prevloc[2] - (obj2_mult * col2_normal[2])]
    obj1_y = [obj1_point[0] - obj1_prevloc[0],obj1_point[1] - obj1_prevloc[1],obj1_point[2] - obj1_prevloc[2]]
    obj1_x = [obj1_loc[0] - obj1_point[0],obj1_loc[1] - obj1_point[1],obj1_loc[2] - obj1_point[2]]
    obj2_y = [obj2_point[0] - obj2_prevloc[0],obj2_point[1] - obj2_prevloc[1],obj2_point[2] - obj2_prevloc[2]]
    obj2_x = [obj2_loc[0] - obj2_point[0],obj2_loc[1] - obj2_point[1],obj2_loc[2] - obj2_point[2]]
    obj1_ny = vec_normalize(obj1_y)
    obj1_nx = vec_normalize(obj1_x)
    obj2_ny = vec_normalize(obj2_y)
    obj2_nx = vec_normalize(obj2_x)
    muly = 1
    #mul1x = 0
    #mul2x = 0
    sqmagn1_y = obj1_y[0]**2 + obj1_y[1]**2 + obj1_y[2]**2
    if obj1_mult > 0:
        obj1_oldvely = -((sqmagn1_y)**0.5)
        sqmagn1_x = obj1_x[0]**2 + obj1_x[1]**2 + obj1_x[2]**2
        if sqmagn1_x != 0:
            mul1x = (((sqmagn1_y) * (avg_coeffric**2)) / sqmagn1_x)**0.5
            #obj1_oldvelx = sqmagn_x
            #(Ua-Ub)+Ma*Ua+Mb*Ub)/(Ma+Mb)
            if mul1x >= 1:
                mul1x = 1
        else:
            mul1x = 0
    else:
        obj1_oldvely = ((sqmagn1_y)**0.5)
        mul1x = 0

    sqmagn2_y = obj2_y[0]**2 + obj2_y[1]**2 + obj2_y[2]**2       
    if obj2_mult > 0:
        obj2_oldvely = ((sqmagn2_y)**0.5)
        sqmagn2_x = (obj2_x[0]**2 + obj2_x[1]**2 + obj2_x[2]**2)
        if sqmagn2_x != 0:
            mul2x = (((sqmagn2_y) * (avg_coeffric**2)) / sqmagn2_x)**0.5
            if mul2x >= 1:
                mul2x = 1
        else:
            mul2x = 0
    else:
        obj2_oldvely = -((sqmagn2_y)**0.5)
        mul2x = 0

    #print('***')
    #print('***')   
       
    obj1_vely = (avg_coefres * obj2_mass * (obj2_oldvely - obj1_oldvely) + (obj1_mass * obj1_oldvely) + (obj2_mass * obj2_oldvely)) / (obj1_mass + obj2_mass)
    obj2_vely = (avg_coefres * obj1_mass * (obj1_oldvely - obj2_oldvely) + (obj1_mass * obj1_oldvely) + (obj2_mass * obj2_oldvely)) / (obj1_mass + obj2_mass)
    # Va = (Cr*Mb*(Ub-Ua)+Ma*Ua+Mb*Ub)/(Ma+Mb)
    # Vb = (Cr*Ma*(Ua-Ub)+Ma*Ua+Mb*Ub)/(Ma+Mb)
   
    obj1_y = [obj1_ny[0] * obj1_vely,obj1_ny[1] * obj1_vely,obj1_ny[2] * obj1_vely]
    obj2_y = [obj2_ny[0] * obj2_vely,obj2_ny[1] * obj2_vely,obj2_ny[2] * obj2_vely]
   
    obj1_newprevloc = [obj1_point[0] + (obj1_y[0] * muly) + (obj1_x[0] * mul1x),obj1_point[1] + (obj1_y[1]  * muly) + (obj1_x[1] * mul1x),obj1_point[2] + (obj1_y[2] * muly) + (obj1_x[2] * mul1x)]
    obj2_newprevloc = [obj2_point[0] + (obj2_y[0] * muly) + (obj2_x[0] * mul2x),obj2_point[1] + (obj2_y[1]  * muly) + (obj2_x[1] * mul2x),obj2_point[2] + (obj2_y[2] * muly) + (obj2_x[2] * mul2x)]
   
    return obj1_newprevloc,obj2_newprevloc

   
class HashTree:
    def __init__(self,gridsize):
        self.gridsize = gridsize
        self.tree={}
        self.ngrid = []
        self.goffset = 1000000000000000
        for xgrid in range(-1,2):
            for ygrid in range(-1,2):
                for zgrid in range(-1,2):
                    self.ngrid.append((xgrid,ygrid,zgrid))
        #print(self.ngrid)
        #print(len(self.ngrid))
        print("Gridsize at:",self.gridsize)
       
    def add_point(self,mol):
        x = mol.loc[0]
        y = mol.loc[1]
        z = mol.loc[2]
        intx = int((x / self.gridsize) + self.goffset)
        inty = int((y / self.gridsize) + self.goffset)
        intz = int((z / self.gridsize) + self.goffset)
        if (intx,inty,intz) not in self.tree:
            self.tree[intx,inty,intz] = []
        if mol not in self.tree[intx,inty,intz]:
            self.tree[intx,inty,intz].append(mol)
            #print (x,y,z,";",intx,inty,intz)
           
    def remove_point(self,mol):
        x = mol.loc[0]
        y = mol.loc[1]
        z = mol.loc[2]
        intx = int((x / self.gridsize) + self.goffset)
        inty = int((y / self.gridsize) + self.goffset)
        intz = int((z / self.gridsize) + self.goffset)
        if (intx,inty,intz) in self.tree:
            for i in range((self.tree[intx,inty,intz].count(mol))):
                if (intx,inty,intz) in self.tree:
                    self.tree[intx,inty,intz].remove(mol)
                       
    def update(self,prev_loc,mol):
        x = mol.loc[0]
        y = mol.loc[1]
        z = mol.loc[2]
        px = prev_loc[0]
        py = prev_loc[1]
        pz = prev_loc[2]
        intx = int((x / self.gridsize) + self.goffset)
        inty = int((y / self.gridsize) + self.goffset)
        intz = int((z / self.gridsize) + self.goffset)
        intpx = int((px / self.gridsize) + self.goffset)
        intpy = int((py / self.gridsize) + self.goffset)
        intpz = int((pz / self.gridsize) + self.goffset)
        if (intx,inty,intz) != (intpx,intpy,intpz):
            if (intpx,intpy,intpz) in self.tree:
                for i in range((self.tree[intpx,intpy,intpz].count(mol))):
                    self.tree[intpx,intpy,intpz].remove(mol)
                    #print("rem mol:",mol.index,"from:",(intpx,intpy,intpz))
                    if len(self.tree[intpx,intpy,intpz]) == 0:
                        del self.tree[intpx,intpy,intpz]
                        #print("del box:",(intpx,intpy,intpz))
            if (intx,inty,intz) not in self.tree:
                self.tree[intx,inty,intz] = []
            if mol not in self.tree[intx,inty,intz]:
                self.tree[intx,inty,intz].append(mol)

                   
    def query(self,mol):
        neighbours = []
        x = mol.loc[0]
        y = mol.loc[1]
        z = mol.loc[2]
        intx = int((x / self.gridsize) + self.goffset)
        inty = int((y / self.gridsize) + self.goffset)
        intz = int((z / self.gridsize) + self.goffset)
        if (intx,inty,intz) in self.tree:
            for i in self.ngrid:
                ngridcoord = (intx + i[0],inty + i[1],intz + i[2])
                if ngridcoord in self.tree:
                    neighbours.extend(self.tree[ngridcoord])
            return neighbours
 

class GeoObjects:
    def __init__(self):
        self.index = 0
        self.polygon = [0,0,0]
       
    def create_poly(self):
        global geoObstacles
        self.polygon = [0] * len(geoObstacles[self.index])
        for i in range(0,len(self.polygon)):
            self.polygon[i] = Polygons()
            self.polygon[i].index = i
            self.polygon[i].create_tri(self.index)
           
           
class Polygons:
    def __init__(self):
        self.index = 0
        self.triangle = []
       
    def create_tri(self,objindex):
        global geoObstacles
        self.triangle = [0] * len(geoObstacles[objindex][self.index])
        for i in range(0,len(self.triangle)):
            self.triangle[i] = Triangles()
            self.triangle[i].index = i
            self.triangle[i].create_vertice(objindex,self.index)
           
           
class Triangles:
    def __init__(self):
        self.index = 0
        self.vertice = []
        self.normal = [0,0,0]
        self.u = [0,0,0]
        self.v = [0,0,0]
        self.w = [0,0,0]
        self.nu = [0,0,0]
        self.nv = [0,0,0]
        self.nw = [0,0,0]
       
    def create_vertice(self,objindex,polyindex):
        global geoObstacles
        global GeoObj
        self.vertice = [0] * len(geoObstacles[objindex][polyindex][self.index])
        for i in range(0,len(self.vertice)):
            self.vertice[i] = Vertices()
            self.vertice[i].index = i
            self.vertice[i].create_vertcoordinate(objindex,polyindex,self.index)
        a = self.vertice[0].co
        b = self.vertice[1].co
        c = self.vertice[2].co
        GeoObj[objindex].polygon[polyindex].triangle[self.index].normal = triangle_normal(a,b,c)
        GeoObj[objindex].polygon[polyindex].triangle[self.index].u = [b[0] - a[0],b[1] - a[1],b[2] - a[2]]
        GeoObj[objindex].polygon[polyindex].triangle[self.index].v = [c[0] - a[0],c[1] - a[1],c[2] - a[2]]
        GeoObj[objindex].polygon[polyindex].triangle[self.index].w = [c[0] - b[0],c[1] - b[1],c[2] - b[2]]
        GeoObj[objindex].polygon[polyindex].triangle[self.index].nu = vec_normalize(self.u)
        GeoObj[objindex].polygon[polyindex].triangle[self.index].nv = vec_normalize(self.v)
        GeoObj[objindex].polygon[polyindex].triangle[self.index].nw = vec_normalize(self.w)
       
           
class Vertices:
    def __init__(self):
        self.index = 0
        self.co = []
   
    def create_vertcoordinate(self,objindex,polyindex,triindex):
        global geoObstacles
        self.co = [0] * len(geoObstacles[objindex][polyindex][triindex][self.index])
        for i in range(0,len(self.co)):
            self.co[i] = geoObstacles[objindex][polyindex][triindex][self.index][i]
           
       
class Molecule:
    def __init__(self):
        temp='do nothing'
        self.loc = [0,0,0]
        self.prev_loc = [0,0,0]
        self.acceleration = [0,0,0]
        self.mass = 1
        self.index = 0
        self.link = {}
       
    def create_link(self):
        global totallinks
        gsize = PTree.gridsize
        goffset = PTree.goffset
        x = self.loc[0]
        y = self.loc[1]
        z = self.loc[2]
        linkseq = ((0,0,1),(0,1,0),(1,0,0),(0,1,1),(1,0,1),(1,1,0),(0,-1,1),(-1,0,1),(-1,1,0))
        for i in linkseq:
            ix = i[0]
            iy = i[1]
            iz = i[2]
            key = (int((x/gsize) + goffset) - ix,int((y/gsize) + goffset) - iy,int(((z/gsize) + goffset) - iz))
            if (key) in PTree.tree:
                #print(self,": ",PTree.tree[key])
                mol = PTree.tree[key]
                mol = mol[0]
                PourcentSpace = 1.002
                #sqinitlenght = (((self.loc[0] - mol.loc[0])**2) + ((self.loc[1] - mol.loc[1])**2) + ((self.loc[2] - mol.loc[2])**2)) * (PourcentSpace**2)
                sqinitlenght = (((mol.loc[0] - self.loc[0])**2) + ((mol.loc[1] - self.loc[1])**2) + ((mol.loc[2] - self.loc[2])**2)) * (PourcentSpace**2)
                initlenght = (sqinitlenght**0.5)
                self.link[ix,iy,iz] = (self,mol,sqinitlenght,initlenght)
                totallinks = totallinks + 1


    def apply_link(self):
        global brokenlinks
        destroylink = []
        destroynum = 0
        for i in self.link:
            mol = self.link[i][1]
            #lenghtx = mol.loc[0] - self.loc[0]
            #lenghty = mol.loc[1] - self.loc[1]
            #lenghtz = mol.loc[2] - self.loc[2]
            lenghtx = self.loc[0] - mol.loc[0]
            lenghty = self.loc[1] - mol.loc[1]
            lenghtz = self.loc[2] - mol.loc[2]
            sqlenght = lenghtx**2 + lenghty**2 + lenghtz**2
            sqInitLength = self.link[i][2]
            if sqlenght != sqInitLength:
           
                #selfoldloc = (self.loc[0],self.loc[1],self.loc[2])
                #mololdloc = (mol.loc[0],mol.loc[1],mol.loc[2])
               
                vStiff = 0.9
                InitLength = self.link[i][3]
                Dist = sqlenght**0.5
                if Dist > (InitLength * 1.01) or Dist < (InitLength * 0.99):
                    destroylink.append(i)
                    destroynum = destroynum + 1
                else:
                    Diff = Dist - InitLength
                    Diff = Diff / InitLength
                   
                    lenghtx = (lenghtx*0.5)
                    lenghty = (lenghty*0.5)
                    lenghtz = (lenghtz*0.5)
                   
                    self.loc[0] = ( self.loc[0] - ((Diff * lenghtx) * vStiff))
                    self.loc[1] = ( self.loc[1] - ((Diff * lenghty) * vStiff))
                    self.loc[2] = ( self.loc[2] - ((Diff * lenghtz) * vStiff))
                   
                    mol.loc[0] = (mol.loc[0] + ((Diff*lenghtx)*vStiff))
                    mol.loc[1] = (mol.loc[1] + ((Diff*lenghty)*vStiff))
                    mol.loc[2] = (mol.loc[2] + ((Diff*lenghtz)*vStiff))
                   
                    #prev_loc = [self.prev_loc[0],self.prev_loc[1],self.prev_loc[2]]
                    #self.prev_loc = [prev_loc[0] + (self.loc[0] - selfoldloc[0]),prev_loc[1] + (self.loc[1] - selfoldloc[1]),prev_loc[2] + (self.loc[2] - selfoldloc[2])]
                    #prev_loc = [mol.prev_loc[0],mol.prev_loc[1],mol.prev_loc[2]]
                    #mol.prev_loc = [prev_loc[0] + (mol.loc[0] - mololdloc[0]),prev_loc[1] + (mol.loc[1] - mololdloc[1]),prev_loc[2] + (mol.loc[2] - mololdloc[2])]
       
        if destroynum > 0:
            for i in destroylink:
                brokenlinks = brokenlinks + 1
                del self.link[i]
        destroynum = 0
        destroylink = []
    def jakobsen():
        pass
       
    def gravity(self):
        self.acceleration[0] = self.acceleration[0] + 0
        self.acceleration[1] = self.acceleration[1] + 0
        self.acceleration[2] = self.acceleration[2] + -9.8

    def verlet(self,DeltaTime):
        tmp = self.loc
        newloc=[0,0,0]
        newloc[0] = (((2- AirDamp) * self.loc[0]) - ((1- AirDamp) * self.prev_loc[0])) + self.acceleration[0]*((DeltaTime)*(DeltaTime))
        newloc[1] = (((2- AirDamp) * self.loc[1]) - ((1- AirDamp) * self.prev_loc[1])) + self.acceleration[1]*((DeltaTime)*(DeltaTime))
        newloc[2] = (((2- AirDamp) * self.loc[2]) - ((1- AirDamp) * self.prev_loc[2])) + self.acceleration[2]*((DeltaTime)*(DeltaTime))
        self.loc = newloc
        self.prev_loc = tmp
        self.acceleration = [0,0,0]
        PTree.update(self.prev_loc,self)
   
    def constraint(self):
        wallfriction = 0.0
        selfoldloc = (self.loc[0],self.loc[1],self.loc[2])
       
        if self.loc[2] <= -10.0000:
            self.loc[2] = -10.0000
            PTree.update(selfoldloc,self)

        if self.loc[0] <= -10.5000:
            self.loc[0] = -10.5000
            PTree.update(selfoldloc,self)

        if self.loc[0] >= 10.5000:
            self.loc[0] = 10.5000
            PTree.update(selfoldloc,self)

        if self.loc[1] <= -10.5000:
            self.loc[1] = -10.5000
            PTree.update(selfoldloc,self)

        if self.loc[1] >= 10.5000:
            self.loc[1] = 10.5000
            PTree.update(selfoldloc,self)
           
           
    def self_collide(self,MolSize):
        global PTree
        PNeighbours = PTree.query(self)
        target = MolSize * 2
        sqtarget = target**2
        if PNeighbours != None:
            #print(len(PNeighbours))
            for mol in PNeighbours:
                lenghtx = self.loc[0] - mol.loc[0]
                lenghty = self.loc[1] - mol.loc[1]
                lenghtz = self.loc[2] - mol.loc[2]
                sqlenght = (lenghtx * lenghtx) + (lenghty * lenghty) + (lenghtz * lenghtz)
                if sqlenght != 0 and sqlenght < sqtarget:
                    lenght = sqlenght**0.5
                    factor = (lenght - target) / lenght
                    selfoldloc = (self.loc[0],self.loc[1],self.loc[2])
                    mololdloc = (mol.loc[0],mol.loc[1],mol.loc[2])
                    self.loc[0] -= lenghtx * factor * 0.5
                    self.loc[1] -= lenghty * factor * 0.5
                    self.loc[2] -= lenghtz * factor * 0.5
                    mol.loc[0] += lenghtx * factor * 0.5
                    mol.loc[1] += lenghty * factor * 0.5
                    mol.loc[2] += lenghtz * factor * 0.5
                   
                    prev_loc = [self.prev_loc[0],self.prev_loc[1],self.prev_loc[2]]
                    self.prev_loc = [prev_loc[0] + (self.loc[0] - selfoldloc[0]),prev_loc[1] + (self.loc[1] - selfoldloc[1]),prev_loc[2] + (self.loc[2] - selfoldloc[2])]
                    prev_loc = [mol.prev_loc[0],mol.prev_loc[1],mol.prev_loc[2]]
                    mol.prev_loc = [prev_loc[0] + (mol.loc[0] - mololdloc[0]),prev_loc[1] + (mol.loc[1] - mololdloc[1]),prev_loc[2] + (mol.loc[2] - mololdloc[2])]
                  
                    col_resp = collision_response(self.loc,self.prev_loc,1,1,1,mol.loc,mol.prev_loc,1,1,1)
                    self.prev_loc = col_resp[0]
                    mol.prev_loc = col_resp[1]
                    #print("collision particles")
                   
                    PTree.update(selfoldloc,self)
                    PTree.update(mololdloc,mol)

                   
    def self_collide_bruteforce(self,MolSize):
        target = MolSize * 2
        sqtarget = target**2
        for mol in mols:
            lenghtx = self.loc[0] - mol.loc[0]
            lenghty = self.loc[1] - mol.loc[1]
            lenghtz = self.loc[2] - mol.loc[2]
            sqlenght = (lenghtx * lenghtx) + (lenghty * lenghty) + (lenghtz * lenghtz)
            if sqlenght != 0 and sqlenght < sqtarget:
                lenght = sqlenght**0.5
                factor = (lenght - target) / lenght
                selfoldloc = (self.loc[0],self.loc[1],self.loc[2])
                mololdloc = (mol.loc[0],mol.loc[1],mol.loc[2])
                self.loc[0] -= lenghtx * factor * 0.5
                self.loc[1] -= lenghty * factor * 0.5
                self.loc[2] -= lenghtz * factor * 0.5
                mol.loc[0] += lenghtx * factor * 0.5
                mol.loc[1] += lenghty * factor * 0.5
                mol.loc[2] += lenghtz * factor * 0.5
               
               
    def raycast_triangle_collide(self):
        global GeoObj
        for obj in GeoObj:
            for poly in obj.polygon:
                for tri in poly.triangle:
                    verta = tri.vertice[0].co
                    vertb = tri.vertice[1].co
                    vertc = tri.vertice[2].co
                    normal = tri.normal
                    u = [vertb[0] - verta[0],vertb[1] - verta[1],vertb[2] - verta[2]]
                    v = [vertc[0] - verta[0],vertc[1] - verta[1],vertc[2] - verta[2]]
                    offset = MolSize
                    offset_ray = vec_normalize(((self.prev_loc[0] - self.loc[0]),(self.prev_loc[1] - self.loc[1]),(self.prev_loc[2] - self.loc[2])))
                    offset_ray = (offset_ray[0] * offset,offset_ray[1] * offset,offset_ray[2] * offset)
                    start_ray = (self.prev_loc[0] + offset_ray[0],self.prev_loc[1] + offset_ray[1],self.prev_loc[2] + offset_ray[2])
                    end_ray = self.loc
                    colpoint_result = triangle_intersec(verta,u,v,normal,start_ray,end_ray)
                    if colpoint_result[0]:
                        selfoldloc = (self.loc[0],self.loc[1],self.loc[2])
                       
                        loc_mult = dot_product(normal,(self.loc[0] - colpoint_result[1][0],self.loc[1] - colpoint_result[1][1],self.loc[2] - colpoint_result[1][2]))
                        prevloc_mult = dot_product(normal,(self.prev_loc[0] - colpoint_result[1][0],self.prev_loc[1] - colpoint_result[1][1],self.prev_loc[2] - colpoint_result[1][2]))
                       
                        damp = 1
                       
                        self.loc[0] = self.loc[0] - (loc_mult * normal[0] * damp)
                        self.loc[1] = self.loc[1] - (loc_mult * normal[1] * damp)
                        self.loc[2] = self.loc[2] - (loc_mult * normal[2] * damp)
                       
                        self.prev_loc[0] = self.prev_loc[0] - (prevloc_mult * normal[0] * damp)
                        self.prev_loc[1] = self.prev_loc[1] - (prevloc_mult * normal[1] * damp)
                        self.prev_loc[2] = self.prev_loc[2] - (prevloc_mult * normal[2] * damp)
                       
                        PTree.update(selfoldloc,self)
                       
    def triangle_collide(self):
        global GeoObj
        target = MolSize
        sqtarget = target**2
        for obj in GeoObj:
            for poly in obj.polygon:
                for tri in poly.triangle:
                    verta = tri.vertice[0].co
                    normal = tri.normal
                    loc_mult = dot_product(normal,(self.loc[0] - verta[0],self.loc[1] - verta[1],self.loc[2] - verta[2]))                      
                    col_sph = [0,0,0]
                    col_sph[0] = self.loc[0] - (loc_mult * normal[0])
                    col_sph[1] = self.loc[1] - (loc_mult * normal[1])
                    col_sph[2] = self.loc[2] - (loc_mult * normal[2])
                    sq_dist_plane = ((self.loc[0] - col_sph[0])**2) + ((self.loc[1] - col_sph[1])**2) + ((self.loc[2] - col_sph[2])**2)
                    if sq_dist_plane != 0 and sq_dist_plane < sqtarget:
                        vertb = tri.vertice[1].co
                        vertc = tri.vertice[2].co
                        u = tri.u
                        v = tri.v
                        w = tri.w
                        nu = tri.nu
                        nv = tri.nv
                        nw = tri.nw
                        ray_start = [col_sph[0] + normal[0],col_sph[1] + normal[1],col_sph[2] + normal[2]]
                        ray_end = [col_sph[0] - normal[0],col_sph[1] - normal[1],col_sph[2] - normal[2]]
                        colpoint_result = triangle_intersec(verta,u,v,normal,ray_start,ray_end)
                        if colpoint_result[0] == False:
                            dist_dict = {}
                            dist_keys = []
                            for i in ([verta,nu,u],[verta,nv,v],[vertb,nw,w]):   
                                vec = [self.loc[0] - i[0][0],self.loc[1] - i[0][1],self.loc[2] - i[0][2]]
                                mult = dot_product(vec,i[1]) / ((i[2][0]**2 + i[2][1]**2 + i[2][2]**2)**0.5)
                                if mult <= 0:
                                    mult = 0
                                if mult >= 1:
                                    mult = 1
                                point = [i[0][0] + (i[2][0] * mult),i[0][1] + (i[2][1] * mult),i[0][2] + (i[2][2] * mult)]
                                sqt_dist = ((self.loc[0] - point[0])**2) + ((self.loc[1] - point[1])**2) + ((self.loc[2] - point[2])**2)
                                dist_dict[sqt_dist] = point
                                dist_keys.append(sqt_dist)
                            dist_keys.sort()
                            near_dist = dist_keys[0]
                            col_sph = dist_dict[near_dist]               
                        lenghtx = self.loc[0] - col_sph[0]
                        lenghty = self.loc[1] - col_sph[1]
                        lenghtz = self.loc[2] - col_sph[2]
                        sqlenght = (lenghtx * lenghtx) + (lenghty * lenghty) + (lenghtz * lenghtz)
                        if sqlenght != 0 and sqlenght < sqtarget:
                            lenght = sqlenght**0.5
                            factor = (lenght - target) / lenght
                            selfoldloc = (self.loc[0],self.loc[1],self.loc[2])
                           
                            self.loc[0] -= lenghtx * factor * 1
                            self.loc[1] -= lenghty * factor * 1
                            self.loc[2] -= lenghtz * factor * 1
                           
                            prev_loc = [self.prev_loc[0],self.prev_loc[1],self.prev_loc[2]]
                            self.prev_loc = [prev_loc[0] + (self.loc[0] - selfoldloc[0]),prev_loc[1] + (self.loc[1] - selfoldloc[1]),prev_loc[2] + (self.loc[2] - selfoldloc[2])]
                          
                            col_resp = collision_response(self.loc,self.prev_loc,1,1,1,col_sph,col_sph,10**10,1,1)
                            self.prev_loc = col_resp[0]
                            #print("collision polygone")

                            PTree.update(selfoldloc,self)
               
       
def Init(ParLoc,ParNum,Psize,Obstacles):
    global mols
    global PTree
    global MolSize
    global GeoObj
    global geoObstacles
    global totallinks
    global totalbrokenlinks
    totalbrokenlinks = 0
    totallinks = 0
    geoObstacles = Obstacles
    MolSize = Psize
    GridSize = MolSize * 2
    mols = [0] * ParNum
    stime = clock()
    GeoObj = [0] * len(geoObstacles)
    for i in range(0,len(GeoObj)):
        GeoObj[i] = GeoObjects()
        GeoObj[i].index = i
        GeoObj[i].create_poly()
    for i in range(0,ParNum):
        mols[i]=Molecule()
        mols[i].loc = ParLoc[(i*3):(i*3+3)]
        mols[i].prev_loc = ParLoc[(i*3):(i*3+3)]
        mols[i].index = i
    print("Particles generation in:",round((clock()-stime),5),"sec")  
    stime = clock()
    PTree = HashTree(GridSize)
    for mol in mols:
        PTree.add_point(mol)      
    print("Hash grid generation in:",round((clock()-stime),5),"sec")
    for mol in mols:
        mol.create_link()
    print(totallinks,"Links generation in:",round((clock()-stime),5),"sec")
    return
def Simulate(Fps):
    global AirDamp
    global DeltaTime
    global brokenlinks
    global totallinks
    global totalbrokenlinks
    brokenlinks = 0
    SubStep = 4
    AirDamp = 0.05 / (SubStep + 1)
    DeltaTime = (1/Fps)/(SubStep + 1)
    for i in range(SubStep + 1):
        for mol in mols:
            mol.verlet(DeltaTime)
        for mol in mols:
            mol.gravity()
        for mol in mols:
            mol.triangle_collide()
        for mol in mols:
            mol.self_collide(MolSize)
        for mol in mols:
            #mol.jakobsen()
            mol.apply_link()
        #for mol in mols:
            #mol.constraint()
       
        #info_grid()
    totalbrokenlinks = totalbrokenlinks + brokenlinks
    print("    >broken links:",brokenlinks,"( total of",totalbrokenlinks,"/",totallinks,")")
    brokenlinks = 0
    ParLoc=[]
    for mol in mols:
        for axe in mol.loc:
            ParLoc.append(axe)
    return ParLoc
   
def info_grid():
    global PTree
    mol_id = []
    for i in PTree.tree:
        for ii in PTree.tree[i]:
            x = round(ii.loc[0],2)
            y = round(ii.loc[1],2)
            z = round(ii.loc[2],2)
            mol_id.append(str(ii.index) + str((x,y,z)))
        print("Box:",i,"contains mol number:",mol_id)
        mol_id = []