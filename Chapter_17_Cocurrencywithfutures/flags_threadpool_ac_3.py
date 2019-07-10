# Example 17-4. replacing executor.map with executor.submit and futures.as_completed
# in the download_many function
from concurrent import futures

from flags_1 import save_flag, get_flag, show, main
from flags_threadpool_2 import download_one

def download_many(cc_list):
    cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do = []
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc)
            to_do.append(future)
            msg = 'Schedule for {}:{}'
            print(msg.format(cc, future))

        results = []
        for future in futures.as_completed(to_do):
            res = future.result()
            msg = '{} result: {!r}'
            print(msg.format(future, res))
            results.append(res)

    return len(results)

if __name__ == "__main__":
    main(download_many)


'''
Output:
    Schedule for BR:<Future at 0x7f164c2995c0 state=running>
    Schedule for CN:<Future at 0x7f164c31c518 state=running>
    Schedule for ID:<Future at 0x7f164c2a9320 state=running>
    Schedule for IN:<Future at 0x7f164c2999b0 state=pending>
    Schedule for US:<Future at 0x7f164c2a92e8 state=pending>
    ID BR <Future at 0x7f164c2a9320 state=finished returned str> result: 'ID'
    CN <Future at 0x7f164c2995c0 state=finished returned str> result: 'BR'
    <Future at 0x7f164c31c518 state=finished returned str> result: 'CN'
    IN <Future at 0x7f164c2999b0 state=finished returned str> result: 'IN'
    US <Future at 0x7f164c2a92e8 state=finished returned str> result: 'US'

    5 flags downloaded in 0.16s
'''