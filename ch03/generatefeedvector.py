#/usr/bin/python
#coding:utf-8
import feedparser
import re
def get_word_counts(url):
    #解析订阅源
    d = feedparser.parse(url)
    wc = {}
    #循环遍历所有的文章条目
    summary = ''
    for e in d.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description
        words = getwords(e.title + ' ' + summary)
        for word in words:
            wc.setdefault(word,0)
            wc[word] += 1
        return d.feed.title, wc
def getwords(html):
    #去除所有html标记
    txt = re.compile(r'<[^>]+>').sub('',html)
    #利用所有非字母字符拆分出单词
    words = re.compile(r'[^a-z^A-Z]+').split(txt)
    #所有单词转成小写
    return [word.lower() for word in words if word != '']
"""apcount = {}
wordcounts = {}
feedlist = [line for line in open(r'E:\python\ProgrammingCollectiveIntelligence\ch03\cnblogsfeedlist.txt')]
for feedurl in feedlist:
    try:
        (title, wc) = get_word_counts(feedurl)
        wordcounts[title] = wc
        for (word, count) in wc.items():
            apcount.setdefault(word, 0)
            if count > 1:
                apcount[word] += 1
    except:
        print('Failed to parse feed %s' % feedurl)

wordlist = []
for (w, bc) in apcount.items():
    frac = float(bc) / len(feedlist)
    if frac > 0.1 and frac < 0.5:
        wordlist.append(w)

out = open(r'E:\python\ProgrammingCollectiveIntelligence\ch03\cnblogsblogdata.txt', 'w')
out.write('Blog')
for word in wordlist:
    out.write('\t%s' % word)
out.write('\n')
for (blog, wc) in wordcounts.items():
    print(blog)
    out.write(blog)
    for word in wordlist:
        if word in wc:
            out.write('\t%d' % wc[word])
        else:
            out.write('\t0')
    out.write('\n')
"""
title, wc = get_word_counts('https://threatpost.com/feed/')
print(title,'\n',wc)