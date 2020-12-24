"""
/***************************************************************************
 * 
 * Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
 * 
 **************************************************************************/
 
 
 
/**
 * @file setup.py
 * @author daiwenkai(com@baidu.com)
 * @date 2015/02/10 19:32:41
 * @brief 
 *  
 **/
"""
from setuptools import setup, find_packages
setup(
        name = "express" ,
        version = "1.0" ,
        description = "express" ,
        author = "daiwenkai" ,
        packages = [
            'express', 
            'express/framework', 
            'express/framework/models', 
            'express/framework/libs', 
            'express/framework/tools', 
            'express/framework/tools/configures', 
            'express/framework/globals', 
            'express/framework/connections', 
            ], 
#        package_data = {'express': ['express/framework/libs/*.so']}, 
        data_files = [('express/framework/libs', ['express/framework/libs/_mcpack.so'])], 
#        scripts = ['express/__init__.py']
        )
"""
/* vim: set expandtab ts=4 sw=4 sts=4 tw=100: */
"""
