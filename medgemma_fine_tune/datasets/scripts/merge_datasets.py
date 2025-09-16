#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
合并LLaMA Factory格式的数据集
将guidence和instructions两个数据集合并到merge_data目录
"""

import os
import json
import shutil
from pathlib import Path

def merge_json_files(source_files, output_file):
    """
    合并多个JSON文件到一个文件
    
    Args:
        source_files: 源JSON文件列表
        output_file: 输出JSON文件路径
    """
    merged_data = []
    
    for file_path in source_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        merged_data.extend(data)
                    else:
                        # 如果是dataset_info.json这样的单个对象，使用最后一个
                        merged_data = data
                print(f"成功读取: {file_path}")
            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {str(e)}")
        else:
            print(f"文件不存在: {file_path}")
    
    # 写入合并后的数据
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)
    
    print(f"合并完成，已写入: {output_file}")

def copy_directory_structure(source_dirs, target_dir):
    """
    复制目录结构
    
    Args:
        source_dirs: 源目录列表
        target_dir: 目标目录
    """
    # 创建目标目录
    os.makedirs(target_dir, exist_ok=True)
    
    # 复制files和toc目录
    for subdir in ['files', 'toc']:
        target_subdir = os.path.join(target_dir, subdir)
        os.makedirs(target_subdir, exist_ok=True)
        
        for source_dir in source_dirs:
            source_subdir = os.path.join(source_dir, subdir)
            if os.path.exists(source_subdir):
                # 复制文件
                for item in os.listdir(source_subdir):
                    source_item = os.path.join(source_subdir, item)
                    target_item = os.path.join(target_subdir, item)
                    
                    if os.path.isdir(source_item):
                        # 如果是目录，递归复制
                        shutil.copytree(source_item, target_item, dirs_exist_ok=True)
                    else:
                        # 如果是文件，直接复制
                        shutil.copy2(source_item, target_item)
                
                print(f"已复制 {source_subdir} 到 {target_subdir}")

def main():
    # 设置路径
    base_dir = Path("e:/R/medgemma_fine_tune/datasets")
    source_dirs = [
        base_dir / "guidence",
        base_dir / "instructions"
    ]
    target_dir = base_dir / "merge_data"
    
    # 创建目标目录
    os.makedirs(target_dir, exist_ok=True)
    
    # 合并JSON文件
    json_files = ['alpaca.json', 'sharegpt.json', 'dataset_info.json']
    
    for json_file in json_files:
        source_files = [os.path.join(src_dir, json_file) for src_dir in source_dirs]
        output_file = os.path.join(target_dir, json_file)
        
        print(f"\n正在合并 {json_file}...")
        merge_json_files(source_files, output_file)
    
    # 复制目录结构
    print("\n正在复制目录结构...")
    copy_directory_structure(source_dirs, target_dir)
    
    print("\n数据集合并完成！")
    print(f"合并后的数据集位置: {target_dir}")

if __name__ == "__main__":
    main()