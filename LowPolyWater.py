#############################################
# Name LowPolyWater Component               #
# Description: Use to create low poly water #
# Author: Samuel Andrade                    #
# Version: 1.0                              #
#############################################
from bge import *
import random
import time

class Timer():
    def __init__(self):
        self.LastTime = time.time()
    def GetTimer(self):
        return time.time() - self.LastTime
    def ResetTimer(self):
        self.LastTime = time.time()
        
class Water(types.KX_PythonComponent):
    args = {
        "Max Height": 0.1,
        "Update Time": 0.2,
        "Move X Direction": False,
        "Move Y Direction": False,
        "Move Z Direction": True,
        "Update Physics": True
    }
    
    def start(self, args):
        self.max_height = args["Max Height"]
        self.update_time = args["Update Time"]
        self.move_x = args["Move X Direction"]
        self.move_y = args["Move Y Direction"]
        self.move_z = args["Move Z Direction"]
        self.update_physics = args["Update Physics"]
        self.mesh = self.object.meshes[0]
        self.vertexs = {}
        self.direction = 0
        self.timer = Timer()
        
        for i in range(0, self.mesh.getVertexArrayLength(0)):
            vertex = self.mesh.getVertex(0, i)
            max_height = random.uniform(0.0, self.max_height)
            self.vertexs[i] = {}
            self.vertexs[i]["OldPosition"] = vertex.z
            self.vertexs[i]["Vertex"] = vertex
            if i == 0:
                self.vertexs[i]["Height"] = max_height
            else:
                self.vertexs[i]["Height"] = (max_height + self.vertexs[i-1]["OldPosition"]) / 2
           
            self.vertexs[i]["Direction"] = "UP"
            
    def update(self):
        if self.timer.GetTimer() >= self.update_time:
            if self.move_x == True or self.move_y == True or self.move_z == True:
                for i in self.vertexs:
                    if self.vertexs[i]["Direction"] == "UP":
                        if self.move_x == True:
                            self.vertexs[i]["Vertex"].x += 0.01
                        if self.move_y == True:
                            self.vertexs[i]["Vertex"].y += 0.01
                        if self.move_z == True:
                            self.vertexs[i]["Vertex"].z += 0.01
                            
                    if self.vertexs[i]["Direction"] == "DOWN":
                        if self.move_x == True:
                            self.vertexs[i]["Vertex"].x -= 0.01
                        if self.move_y == True:
                            self.vertexs[i]["Vertex"].y -= 0.01
                        if self.move_z == True:
                            self.vertexs[i]["Vertex"].z -= 0.01
                    
                    if self.vertexs[i]["Vertex"].z >= self.vertexs[i]["Height"] and self.vertexs[i]["Direction"] == "UP":
                        self.vertexs[i]["Direction"] = "DOWN"
                    if self.vertexs[i]["Vertex"].z <= self.vertexs[i]["OldPosition"] and self.vertexs[i]["Direction"] == "DOWN":
                        self.vertexs[i]["Direction"] = "UP"
                        if i > 0:
                            max_height = random.uniform(0.0, self.max_height)
                            self.vertexs[i]["Height"] = (max_height + self.vertexs[i-1]["OldPosition"]) / 2
                        else:
                            max_height = random.uniform(0.0, self.max_height)
                            self.vertexs[i]["Height"] = max_height
                            
                        
                for poly in self.mesh.polygons:
                    v1 = self.mesh.getVertex(0, poly.v1).XYZ - self.mesh.getVertex(0, poly.v2).XYZ
                    v2 = self.mesh.getVertex(0, poly.v3).XYZ - self.mesh.getVertex(0, poly.v2).XYZ

                for vertex in poly.vertices:
                    vertex.normal = v2.cross(v1).normalized()
                
                if self.update_physics == True:
                    self.object.reinstancePhysicsMesh()
            
            self.timer.ResetTimer()