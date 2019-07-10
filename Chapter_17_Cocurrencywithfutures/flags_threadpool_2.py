from concurrent import futures

from flags_1 import save_flag, get_flag, show, main

MAX_WORKER = 20

# 每一个线程执行的函数
def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower()+'.gif')
    return cc


def download_many(cc_list):
    workers = min(MAX_WORKER, len(cc_list))
    # 用线程数初始化ThreadPoolExecutor
    # executor.__exit__方法会调用executor.shutdown(wait=True)，因此会保证所有线程都
    # 执行完成后再退出
    with futures.ThreadPoolExecutor(workers) as executor:
        # 这里的map和built-in类似，有一点不同，download_one函数是并发在不同线程中被调用的
        # map返回一个generator，包含所有线程中函数执行的返回结果
        res = executor.map(download_one, sorted(cc_list))

    # Return the number of results obtained; if any of the threaded calls raised an
    # exception, that exception would be raised here as the implicit next() call tried
    # to retrieve the corresponding return value from the iterator.
    return len(list(res))

if __name__ == "__main__":
    main(download_many)