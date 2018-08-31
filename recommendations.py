#!/usr/bin/python
# -*- coding: utf-8 -*-
from math import sqrt
# A dictionary of movie critics and their ratings of a small set of movies
critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0,
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5,
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0,
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'The Night Listener': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5,
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0,
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5,
    },
    'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0,
             'Superman Returns': 4.0},
}
def sim_distance(prefs,person1,person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    if len(si) == 0:
        return 0
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item],2) for item in prefs[person1] if item in prefs[person2]])
    return 1/(1 + sqrt(sum_of_squares))
#print(sim_distance(critics,'Lisa Rose','Gene Seymour'))
#print(sim_distance(critics,'Lisa Rose','eysdo'))
#返回p1和p2的皮尔逊相关系数
def sim_pearson(prefs,p1,p2):
    #把双方共同评价过的物品放入si字典
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    n = len(si)
    #如果p1和p2没有共同之处，则返回0
    if n == 0:
        return 0
    #对所有偏好求和
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    #求平方和
    sum1Sq = sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it],2) for it in si])
    #求乘积之和
    pSum = sum([prefs[p1][it]*prefs[p2][it] for it in si])
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1,2) / n ) * (sum2Sq - pow(sum2,2) / n ))
    if den == 0:
        return 0
    r = num / den
    return r
#print(sim_pearson(critics,'Lisa Rose','Gene Seymour'))
def topMatches(prefs,person,n=5,similarity=sim_pearson):
    scores = [(similarity(prefs,person,other),other) for other in prefs if other != person ]
    scores.sort()
    scores.reverse()
    return scores[0:n]
#print(topMatches(critics,'Toby'))
#利用所有他人评价值的加权平均，为某人提供推荐
def getRecommendations(prefs,person,similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        #不和自己作比较
        if other == person:
            continue
        sim = similarity(prefs,person,other)
        #忽略评价值<=0的情况
        if sim <=0:continue
        for item in prefs[other]:
            #只对自己还未曾看过的影片进行评价
            if item not in prefs[person] or prefs[person][item] == 0:
                #相似度*评价值
                totals.setdefault(item,0)
                totals[item] += prefs[other][item] * sim
                #相似度之和
                simSums.setdefault(item,0)
                simSums[item] += sim
    rankings = [(total / simSums[item],item) for item ,total in totals.items()]
    rankings.sort(reverse=True)
    return rankings
#print(getRecommendations(critics,'Toby'))
print(getRecommendations(critics,'Toby',similarity=sim_distance))
