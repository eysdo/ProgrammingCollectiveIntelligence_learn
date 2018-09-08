#coding:utf-8
import numpy as np
def data_load(file):
    #只取file文件的第一行以后的第一，第二列数据
    data = np.genfromtxt(file,delimiter=',',skip_header=1,usecols=(1,2),dtype=float)
    return np.array(data,dtype=float)
def plus_center(dataset,k=3):
    lenth, dim = dataset.shape
    _max = np.max(dataset,axis=0)
    _min = np.min(dataset,axis=0)
    centers = []
    #生成第一个中心点
    centers.append((_min + (_max - _min) * np.random.rand(dim)))
    centers = np.array(centers)
    for i in range(1,k):
        #计算dataset中所有点距离第一个中心点centers距离
        distances = []
        for row in dataset:
            distances.append(np.min(np.linalg.norm(row - centers,axis=1)))
        #蒙特卡罗法, 假设总距离由各个距离条组成,落在距离条长的上面概率大,蒙特卡罗法是因为落在长条上的概率大,可以用概率求长条长度,这里反过来用
        temp = sum(distances) * np.random.rand()
        for j in range(lenth):
            temp -= distances[j]
            if temp < 0:
                centers = np.append(centers,[dataset[j]],axis=0)
                break
    return centers
#dataset = data_load(r'E:\python\ProgrammingCollectiveIntelligence\ch03\dogs.csv')
#print(plus_center(dataset))
def kmeans(dataset,k):
    centers = plus_center(dataset,k)
    def get_label(data):
        distances = np.linalg.norm(data - centers,axis=1)
        #返回最小距离值的索引即label
        return np.where(distances == np.min(distances))[0][0]
    labels = np.ones(len(dataset))
    while 1:
        #生成新的标签
        label_new = np.array(list(map(get_label,dataset)))
        #判断标签是否改变
        if sum(np.abs(labels - label_new)) == 0:
            break
        labels = label_new
        for i in range(k):
            #更新聚类中心
            centers[i] = np.mean(dataset[labels == i],axis=0)
    #计算误差平方和
    SSE = sum([sum([(j - centers[i]).dot(j-centers[i]) for j in dataset[labels == i]]) for i in range(k)])
    print("SSE:",SSE)
    return label_new,centers
dataset = data_load(r'E:\python\ProgrammingCollectiveIntelligence\ch03\dogs.csv')
labels, centers = kmeans(dataset,3)
for i in set(labels):
    print(i,"-----\n",dataset[labels == i])
