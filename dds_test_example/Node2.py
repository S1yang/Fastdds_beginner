# Node2.py

from machine import DDSMachine
import time

def main():
    # 初始化 DDSMachine 为订阅模式
    dds_machine = DDSMachine(mode='subscribe')

    # 简单等待循环，保持程序运行
    print("Subscriber running. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(2)  # 等待一秒，减少CPU占用
    except KeyboardInterrupt:
        # 捕获到中断信号，退出循环
        print("Subscriber stopped.")

if __name__ == "__main__":
    main()
