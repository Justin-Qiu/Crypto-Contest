#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# 云服务器端Web服务接口代码

import soaplib  
from soaplib.core.service import rpc, DefinitionBase, soap  
from soaplib.core.model.primitive import String, Integer, Double
from soaplib.core.server import wsgi  
from soaplib.core.model.clazz import Array

# 从功能实现代码中引入图像上传和去重、图像检索函数
from functions import image_upload_dedup, image_search

# 服务器IP地址
IP_ADDRESS = '10.170.43.249'

# 端口号
PORT = 7789

class WebService(DefinitionBase): 
      
    '''
    图片上传与去重函数：

    输入参数
        图片ID，图像特征值密文，图像感知哈希，图像密文
    返回值
        上传成功：1
        有同名图像：2
        有重复图像：3
    '''
    @soap(String, String, String, String, _returns = Integer)  
    def upload(self, image_id, feature, dhash, ciphertext):
        info = image_upload_dedup(image_id, feature, dhash, ciphertext)
        return info
    
    '''
    图片搜索函数：

    输入参数
        图像特征值密文
    返回值
        图像密文列表（10张）
    ''' 
    @soap(String, _returns = Array(String))  
    def search(self, feature):
        info = image_search(feature)
        return info
 
if __name__=='__main__':  
    try:  
        from wsgiref.simple_server import make_server  
        soap_application = soaplib.core.Application([WebService], 'tns')  
        wsgi_application = wsgi.Application(soap_application)  
        
        # 启动服务器
        server = make_server(IP_ADDRESS, PORT, wsgi_application)  
        print 'Cloud server is running...'  
        server.serve_forever()  
        
    except ImportError:  
    
        # Python版本需不低于于2.5
        print "Error: Python version >= 2.5 is required."  
