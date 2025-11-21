#!/usr/bin/python
#coding:utf-8

import os
try:
  import xml.etree.cElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET

# --- 第 1 部分：从 Info.plist 读取版本号 (无变化) ---
# 从 Info.plist 中读取 QMUIKit 的版本号，将其定义为一个 static const 常量以便代码里获取
infoFilePath = str(os.getenv('SRCROOT')) + '/QMUIKit/Info.plist'
infoTree = ET.parse(infoFilePath)
infoDictList = list(infoTree.find('dict'))
versionString = ''
for index in range(len(infoDictList)):
  element = infoDictList[index]
  if element.text == 'CFBundleShortVersionString':
    versionString = infoDictList[index + 1].text
    break
if versionString.startswith('$'):
  versionEnvName = versionString[2:-1]
  versionString = os.getenv(versionEnvName)
  print('umbrella creator: Bundle version string is %s, from env name: %s' % (versionString, versionEnvName))

# --- 第 2 部分：准备路径 ---
# publicHeaderFilePath 指向编译产物目录，用于获取公开头文件的【文件名列表】
publicHeaderFilePath = os.path.join(str(os.getenv('BUILT_PRODUCTS_DIR')), str(os.getenv('PUBLIC_HEADERS_FOLDER_PATH')))
print('umbrella creator: Reading public header list from: ' + publicHeaderFilePath)

# umbrellaHeaderFilePath 是 QMUIKit.h 的完整路径
umbrellaHeaderFileName = 'QMUIKit.h'
umbrellaHeaderFilePath = os.path.join(str(os.getenv('SRCROOT')), 'QMUIKit', umbrellaHeaderFileName)
print('umbrella creator: Umbrella header path = ' + umbrellaHeaderFilePath)

# symlinkDestDir 是符号链接的【目标位置】，位于 SRCROOT 中
symlinkDestDir = os.path.join(str(os.getenv('SRCROOT')), 'QMUIKit', 'include')
print('umbrella creator: Symlink destination directory = ' + symlinkDestDir)

# 确保符号链接的目标目录存在
if not os.path.exists(symlinkDestDir):
    os.makedirs(symlinkDestDir)
    print('umbrella creator: Created directory ' + symlinkDestDir)

# --- 预处理：构建源码头文件路径的映射 ---
# 遍历 SRCROOT/QMUIKit 目录，将所有找到的 .h 文件名和它的【绝对路径】存入字典
sourceSearchRoot = os.path.join(str(os.getenv('SRCROOT')), 'QMUIKit')
print('symlink creator: Searching for original header files in: ' + sourceSearchRoot)
headerSourceMap = {}
for root, dirs, files in os.walk(sourceSearchRoot):
    # 排除 include 目录本身，避免链接到链接
    if 'include' in dirs:
        dirs.remove('include')
    for file in files:
        if file.endswith('.h'):
            headerSourceMap[file] = os.path.join(root, file)

# --- 第 3 部分：生成 Umbrella Header 内容并创建【相对路径】符号链接 ---
umbrellaFileContent = '''/**
 * Tencent is pleased to support the open source community by making QMUI_iOS available.
 * Copyright (C) 2016-2021 THL A29 Limited, a Tencent company. All rights reserved.
 * Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
 * http://opensource.org/licenses/MIT
 * Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
 */

/// Automatically created by script in Build Phases

#import <UIKit/UIKit.h>

#ifndef QMUIKit_h
#define QMUIKit_h

static NSString * const QMUI_VERSION = @"%s";

''' % (versionString)

# 获取 Xcode 项目定义的“公开头文件”的文件名列表
publicHeaderFilenames = [ f for f in os.listdir(publicHeaderFilePath) if os.path.isfile(os.path.join(publicHeaderFilePath, f))]
publicHeaderFilenames.sort()

for filename in publicHeaderFilenames:
  # 1. (原有逻辑) 将头文件引用添加到 umbrella header 的内容中
  if filename != umbrellaHeaderFileName:
    umbrellaFileContent += '''#if __has_include("%s")
#import "%s"
#endif

''' % (filename, filename)

  # 2. (核心修改) 为每个头文件创建【相对路径】符号链接
  
  # 从映射中查找该文件名的【绝对】原始路径
  absoluteSourcePath = headerSourceMap.get(filename)
  
  if absoluteSourcePath:
    # 符号链接的【绝对】目标路径
    absoluteDestPath = os.path.join(symlinkDestDir, filename)
    
    # --- 关键步骤：计算相对路径 ---
    # 计算源文件相对于目标链接【所在目录】的路径
    # 例如，从 '.../QMUIKit/include/' 到 '.../QMUIKit/UIComponents/QMUIButton.h'
    # 结果会是 '../UIComponents/QMUIButton.h'
    relativeSourcePath = os.path.relpath(absoluteSourcePath, start=symlinkDestDir)
    
    # 如果目标路径已存在链接或文件，先删除
    if os.path.lexists(absoluteDestPath):
        os.remove(absoluteDestPath)
    
    # 创建符号链接，第一个参数使用计算出的【相对路径】
    os.symlink(relativeSourcePath, absoluteDestPath)
  else:
    # 如果在源码中找不到对应的头文件，打印一个警告
    print('symlink creator: WARNING - Could not find source file for %s in %s' % (filename, sourceSearchRoot))


umbrellaFileContent += '#endif /* QMUIKit_h */'
umbrellaFileContent = umbrellaFileContent.strip()

# --- 第 4 部分：写入 Umbrella Header 文件 (无变化) ---
f = open(umbrellaHeaderFilePath, 'r+')
f.seek(0)
oldFileContent = f.read().strip()
if oldFileContent == umbrellaFileContent:
  print('umbrella creator: ' + umbrellaHeaderFileName + ' content is unchanged, skipping write.')
else:
  print('umbrella creator: ' + umbrellaHeaderFileName + ' content has changed, rewriting file.')
  f.seek(0)
  f.write(umbrellaFileContent)
  f.truncate()

f.close()

print('umbrella creator: Script finished. Relative symlinks created in %s.' % symlinkDestDir)
