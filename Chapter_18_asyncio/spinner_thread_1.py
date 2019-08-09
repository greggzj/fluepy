import threading
import itertools
import time
import sys

# 1 定义一个simple mutable object来控制子线程
class Signal:
    go = True


def spin(msg, signal): # 2 定义子线程运行的函数
    write, flush = sys.stdout.write, sys.stdout.flush
    # 3 itertools.cycle定义了无限循环的字符串
    for char in itertools.cycle('|/-\\'): 
        status = char + ' ' + msg
        write(status)
        flush()
        # 4 tricky:　'\x08'表示backspace，本句话是让cursor光标回退到开头
        write('\x08' * len(status))
        time.sleep(.1)
        if not signal.go:  # 5
            break
    # 6 Clear the status line by overwriting with spaces and moving the cursor back to the beginning.
    write(' ' * len(status) + '\x08' * len(status))

def slow_function():    # 7
    # pretend waiting a long time for I/O
    # 7 调用sleep会block main thread，更重要的是GIL会被释放，secondary thread会继续运行
    time.sleep(3)
    return 42


def supervisor():   # 9
    signal = Signal()
    spinner = threading.Thread(target=spin,
                               args=('thinking!', signal))
    print('spinner object:', spinner)   # 10 
    spinner.start() # 11 Start the secondary thread.
    result = slow_function()    # 12 main thread block, second thread执行，绘制动画
    signal.go = False   # 13 终止second thread
    spinner.join()  # 14 等待second thread 结束.
    return result

def main():
    result = supervisor()   # 15
    print('Answer:', result)

if __name__ == "__main__":
    main()

"""
Output:
    执行了一个动画/-\/，thnking!,最后是answer:42

    从设计上说，python中终止线程是没有API的，你必须自己发送一个让thread shutdown的消息，
    这里用了signal.go 属性。
"""