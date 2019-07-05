import os
import time
import sys

# requests不是标准库，因此这里将其单独在标准库后import，并空出一行
import requests

# ISO 3166 country code，20个人口最多的国家
POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()

#
BASE_URL = 'http://flupy.org/data/flags'

#
DEST_DIR = 'downloads/'

# 存储img(byte sequence)到Filename
def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)

# 6
def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content

# 7 为了能够在一行里现实所有的信息，这里将结尾默认的换行改成了空格并manually flush stdout
# 通常情况下stdout的flush是在等到换行之后自动进行的
def show(text):
    print(text, end=' ')
    sys.stdout.flush()

def download_many(cc_list): # 8
    for cc in sorted(cc_list): # 9
        image = get_flag(cc)
        show(cc)
        save_flag(image, cc.lower() + '.gif')

    return len(cc_list)

# 10
def main(download_many):
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))

if __name__ == "__main__":
    main(download_many) # 11