import os,json

class file:
    def __init__(self,file):#file传相对值即可
        self.file = os.path.join(os.path.dirname(__file__),file)

    def listdir(self,filename):#传回当前文件夹内的所有文件（没有递归），返回值为json，filename为在初始化时输入的文件夹下的路径，为相对路径
        #实现列出文件夹下的文件
        if os.path.isdir(self.file+"/"+filename):
            file = os.listdir(self.file+"/"+filename)#只列出当前文件夹的文件
            js = []

            for i in file:#开始构建返回的json
                size = os.path.getsize(self.file+"/"+filename+"/"+i)#文件大小，单位：字节
                type = str(i).split(".")[-1]
                if size == 0:#如果大小是零，那么就是文件夹
                    js.append({str(i):{"type":"文件夹"}})
                else:
                    js.append({str(i):{"type":type,"size":str(size/1000)}})

            return str(js)#这个接口返回json