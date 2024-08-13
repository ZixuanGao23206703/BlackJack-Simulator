import multiprocessing
import subprocess

# 定义一个函数来运行每个脚本
def run_script(script_name):
    subprocess.run(["python", script_name])

if __name__ == "__main__":
    # 列出需要并行运行的脚本
    scripts = ["montecarlo_strategy.py", "basic_strategy.py"]
    
    # 创建进程列表
    processes = []
    
    # 启动每个脚本
    for script in scripts:
        process = multiprocessing.Process(target=run_script, args=(script,))
        processes.append(process)
        process.start()
    
    # 等待所有脚本运行完毕
    for process in processes:
        process.join()

    print("Both scripts have finished executing.")
