#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 云服务器端功能实现代码

import MySQLdb
import os
import os.path
import numpy

'''
图片上传与去重函数：

输入参数
    图片ID，图像特征值密文，图像感知哈希，图像密文
返回值
    上传成功：1
    有同名图像：2
    有重复图像：3
''' 
def image_upload_dedup(image_id, feature, dhash, ciphertext):
    
    #连接MySQL数据库
    conn = MySQLdb.connect(
            host='localhost', 
            user='admin', 
            passwd='123456', 
            db='img',
            charset='utf8'
            )
    
    # 创建游标
    cur = conn.cursor() 
  
    # 判断是否已有同名图像
    image_id = image_id.encode('utf-8') 
    sql_search = "SELECT * FROM images WHERE image_id = '%s'" % image_id
    
    # 如无同名图像
    if cur.execute(sql_search) == 0L: 
        
        # 遍历数据库
        cur.execute("SELECT * FROM images")
        result = cur.fetchall()
    
        for row in result:
            dhash_temp = row[3]
            
            # 计算感知哈希差异位数
            difference = (int(dhash, 16)) ^ (int(dhash_temp, 16))
            
            # 如有重复图像（差异位数小于5视为相同图像）
            if bin(difference).count("1") < 5:
                return 3 
        
        # 保存密文图像文件
        with open('images/%s' % image_id, 'w') as f:
            f.write('%s' % ciphertext) 
        
        # 在数据库中添加图像信息
        sql = "insert into images(image_id, feature, dhash) values('%s','%s','%s')" % (image_id, feature, dhash)
        cur.execute(sql)
        
        # 提交数据库操作
        conn.commit() 
        
        # 上传成功
        return 1 
    
    # 如有同名图像
    elif os.path.exists('images/%s' % image_id): 
        return 2
    
    # 关闭数据库连接
    conn.close() 

'''
图片搜索函数：

输入参数
    图像特征值密文
返回值
    图像密文列表（10张）
'''
def image_search(feature):
    
    #连接MySQL数据库
    conn = MySQLdb.connect(
            host='localhost', 
            user='admin', 
            passwd='123456', 
            db='img',
            charset='utf8'
            )
    
    # 创建游标        
    cur = conn.cursor() 
    
    # 将传入特征向量字符串转换为float类型列表
    feature = feature[1:-1].split(', ')
    feature = map(float, feature)
    
    # 将特征向量转换为numpy数组
    search_feature = numpy.array(feature) 
    
    image_list = []
    image_dict = {}
    #threshold = 2.6 # 设置门限值
    
    # 遍历数据库
    cur.execute("SELECT * FROM images")
    result = cur.fetchall()
    
    for row in result:
        image_id = row[1]
        feature = row[2]
        
        # 将特征向量字符串转换为float类型列表
        feature = feature[1:-1].split(', ')
        feature = map(float, feature)
        
        # 将特征向量转换为numpy数组
        source_feature = numpy.array(feature) 
        
        #distance = numpy.linalg.norm(search_feature - source_feature) # 计算欧氏距离
        
        # 计算相似度
        distance = search_feature.dot(source_feature) 
        
        '''
        with open('images/%s' % image_id, 'r') as f:
            ciphertext = f.read()
        '''
        
        image_dict[image_id] = distance
        
        '''
        if distance < threshold: # 如果欧氏距离小于门限值
        
            # 读出图像密文
            with open('images/%s' % image_id, 'r') as f:
                ciphertext = f.read()
            image_dict[ciphertext] = distance
        '''
    
    # 将搜索结果按相似度排序       
    image_dict = sorted(image_dict.items(), key = lambda item:item[1])   
    
    # 取前10个相似图像
    for i in range(10):
        with open('images/%s' % image_dict[i][0], 'r') as f:
            ciphertext = f.read()
        image_list.append(ciphertext)
    
    # 返回搜索结果密文图像列表
    return image_list 
    
    # 关闭数据库连接
    conn.close() 
