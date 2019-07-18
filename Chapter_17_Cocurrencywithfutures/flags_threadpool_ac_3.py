# Example 17-4. replacing executor.map with executor.submit and futures.as_completed
# in the download_many function
from concurrent import futures

from flags_1 import save_flag, get_flag, show, main
from flags_threadpool_2 import download_one

def download_many(cc_list):
    cc_list = cc_list[:5] 
    # max_workers没有设置太多，以便于更好地观察最终输出结果
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do = []
        for cc in sorted(cc_list):
            # 调用submit,download_one就会被调度起来，submit返回一个future对象
            future = executor.submit(download_one, cc)
            # 将future 对象存储起来，这样后续可以调用as_completed函数来判断对应的download_one的执行结果。
            to_do.append(future)
            msg = 'Schedule for {}:{}'
            print(msg.format(cc, future))

        results = []
        # 当future list对象完成时， as_completed会yield futures
        for future in futures.as_completed(to_do):
            # 8
            res = future.result()
            msg = '{} result: {!r}'
            # 9
            print(msg.format(future, res))
            results.append(res)

    return len(results)

if __name__ == "__main__":
    main(download_many)


'''
Output:
    Schedule for BR:<Future at 0x7f164c2995c0 state=running> # 1 future的调度顺序就是按照字母顺序(国家顺序来的)
    Schedule for CN:<Future at 0x7f164c31c518 state=running>
    Schedule for ID:<Future at 0x7f164c2a9320 state=running>
    Schedule for IN:<Future at 0x7f164c2999b0 state=pending> # 2 maxworker=3，剩下的都是Pending
    Schedule for US:<Future at 0x7f164c2a92e8 state=pending>
    ID BR <Future at 0x7f164c2a9320 state=finished returned str> result: 'ID' # 3 ID BR是download_one函数所在现成的输出(该线程被连续调度执行了2次)，剩下的是download_many现成的输出
    CN <Future at 0x7f164c2995c0 state=finished returned str> result: 'BR'
    <Future at 0x7f164c31c518 state=finished returned str> result: 'CN'
    IN <Future at 0x7f164c2999b0 state=finished returned str> result: 'IN'
    US <Future at 0x7f164c2a92e8 state=finished returned str> result: 'US'

    5 flags downloaded in 0.16s
'''