# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 17:49:11 2021

@author: 18000
"""

import jieba
import jieba.posseg as pseg

# 输入文件
txt_file_name = './小时代.txt'
# 输出文件
node_file_name = './小时代-人物节点.csv'
link_file_name ='./小时代-人物共现.csv'
jieba.load_userdict('./小时代userdict.txt')

# 打开文件，读入文字
txt_file = open(txt_file_name, 'r', encoding='ANSI')
line_list = txt_file.readlines() # 返回列表，每一行（段落）是列表的一个元素
txt_file.close()
#print(line_list)  # 测试点


##--- 第1步：生成基础数据（一个列表，一个字典）
line_name_list = []  # 每个段落出现的人物列表
name_cnt_dict = {}  # 统计人物出现次数

for line in line_list: # 逐个段落循环处理
    word_gen = pseg.cut(line) # peseg.cut返回分词结果，“生成器”类型
    line_name_list.append([])

    for one in word_gen:
        word = one.word
        flag = one.flag
        
        if len(word) == 1:
            continue
        #print(word)  # 测试点
        
        if flag == 'nr': 
            line_name_list[-1].append(word)
            if word in name_cnt_dict.keys():
                name_cnt_dict[word] = name_cnt_dict[word] + 1
            else:
                name_cnt_dict[word] = 1

#print(line_name_list)  # 测试点
#print('-'*20)
#print(name_cnt_dict)  # 测试点


##--- 第2步：用字典统计人名“共现”数量（relation_dict）
relation_dict = {}

for line_name in line_name_list:
    for name1 in line_name:  # 判断该人物name1是否在字典中
        if name1 in relation_dict.keys():
            pass  # 如果已经在字典中，继续后面的统计工作
        else:
            relation_dict[name1] = {}  # 把name1加入字典“键”，作为连接的起点
            #print('add ' + name1)  # 测试点
        
        # 统计name1与本段的所有人名（除了name1自身）的共现数量
        for name2 in line_name:
            if name2 == name1:   # 不统计name1自身
                continue
            # 检查name1的值列表（即连接的终点）中是否已经有name2
            if name2 in relation_dict[name1].keys():
                relation_dict[name1][name2] = relation_dict[name1][name2] + 1
            else:
                relation_dict[name1][name2] = 1

##--- 第3步：输出统计结果
#for k,v in relation_dict.items():  # 测试点
#    print(k, ':', v)

node_file = open(node_file_name, 'w') 
# 节点文件，格式：Name,Weight -> 人名,出现次数
node_file.write('Name,Weight\n')
for name,cnt in name_cnt_dict.items(): 
    node_file.write(name + ',' + str(cnt) + '\n')
node_file.close()

link_file = open(link_file_name, 'w')
# 连接文件，格式：Source,Target,Weight -> 人名1,人名2,共现数量
link_file.write('Source,Target,Weight\n')
for name1,link_dict in relation_dict.items():
    for name2,link in link_dict.items():
        if link>5:
    
            link_file.write(name1 + ',' + name2 + ',' + str(link) + '\n')
link_file.close()
print('finished')