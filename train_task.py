'''
训练脚本 (运行在高性能电脑，进行质量测试)
'''

import os
import subprocess
import sys

TRAIN_SCRIPT = "train.py"

# 输入根目录
INPUT_ROOT = "input"

# 输出根目录
OUTPUT_ROOT = "output"

# 迭代次数配置数组
ITERATIONS_LIST = [7000, 15000, 30000]

RESOLUTION = 1
# ==========================================

def run_trainings():
    if not os.path.exists(TRAIN_SCRIPT):
        print(f"错误: 找不到 {TRAIN_SCRIPT}")
        return

    if not os.path.exists(INPUT_ROOT):
        print(f"错误: 找不到输入目录 {INPUT_ROOT}")
        return

    sub_dirs = [d for d in os.listdir(INPUT_ROOT) if os.path.isdir(os.path.join(INPUT_ROOT, d))]
    
    if not sub_dirs:
        print(f"警告: 在 {INPUT_ROOT} 下没有找到任何子文件夹。")
        return

    print(f"找到子文件夹: {sub_dirs}")

    for iterations in ITERATIONS_LIST:
        print(f"\n开始执行迭代次数为 {iterations} 的任务序列...")
        
        for dir_name in sub_dirs:
            source_path = os.path.join(INPUT_ROOT, dir_name)
            
            model_path = os.path.join(OUTPUT_ROOT, str(f"iter_{iterations}"), dir_name)
            
            command = [
                "python", TRAIN_SCRIPT,
                "-s", source_path,
                "--model_path", model_path,
                "--iterations", str(iterations),
                "--resolution", str(RESOLUTION)
            ]
            
            print("-" * 50)
            print(f"正在训练: {dir_name} | 迭代: {iterations}")
            print(f"执行命令: {' '.join(command)}")
            print("-" * 50)
            
            try:
                subprocess.run(command, check=True)
                print(f"完成训练: {dir_name} (迭代: {iterations})")
            except subprocess.CalledProcessError as e:
                print(f"训练出错! 文件夹: {dir_name}, 错误代码: {e.returncode}")
                sys.exit(1)

    print("\n完成")

if __name__ == "__main__":
    run_trainings()