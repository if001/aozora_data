
"""
This program get aozora_bunko novels.
To do it, you set author_id as option.

example,
$ python3 get_aozora.py -id <savefname>

"""

#import urllib.request
import requests
import os
import sys
import argparse
import signal
from multiprocessing import Pool


def get_request(url):
    try:
        r = requests.get(url, stream=True, timeout=10)
        r.encoding
        print(">>>> get : ", url)
        return r
    except:
        print(" ----- html error code", url)
        return None


def get_body(r):
    if r is None:
        return ""
    else:
        return r.text


def get_cards(body):
    __cards = []
    for value in body.split("\n"):
        if ('<li>' in value) and ('.html' in value):
            __cards.append(value.split('"')[1].split(
                '/')[-1].split(".")[0].replace("card", ""))
    return __cards


def get_zip_code(body, cardId):
    zipcode = []
    for value in body.split("\n"):
        if ('.zip' in value) and ('files' in value) and (cardId in value):
            zipcode.append(value.split('"')[1].split("/")[-1])
    if len(zipcode) != 0:
        return zipcode[0]
    if len(zipcode) == 0:
        return ""


def set_novel_url(authorId, cardId):
    url = "http://www.aozora.gr.jp/cards/" + authorId + "/card" + cardId + ".html"
    return url


def zero_padding(authorId):
    # authorIDが6けたなので足りないぶんを0で埋める
    if len(str(authorId)) < 6:
        zero = ""
        for i in range(6 - len(authorId)):
            zero += "0"
        authorId = zero + authorId
    return authorId


def download(url, savedir, filename):
    print("download : " + filename)
    r = get_request(url)
    if r is None:
        return False

    with open(savedir + filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        return savedir + filename
    return False


def get_path():
    return os.path.dirname(os.path.abspath(__file__))


class Novel():
    def __init__(self, author_id, project_path, save_dir):
        self.author_id = author_id
        self.project_path = project_path
        self.save_dir = save_dir

    # TODO 副作用がすごいから修正する
    def save_novel_body(self, card_id):
        novel_url = set_novel_url(self.author_id, card_id)
        novel_body = get_body(get_request(novel_url))
        zip_code = get_zip_code(novel_body, card_id)

        files = os.listdir(self.project_path + self.save_dir)

        print(zip_code)
        url = "http://www.aozora.gr.jp/cards/" + self.author_id + "/files/" + zip_code
        if zip_code in files:
            print("zip file already exist")
            return False
        if zip_code == "":
            print("zip code get error")
            return False
        result = download(url, self.project_path + self.save_dir, zip_code)
        if result is False:
            print("download error:", url)
            return False


def handler(signal, frame):
    print('うおおお、やられたーー')
    exit(0)


def main():
    parser = argparse.ArgumentParser(description='get aozora')
    parser.add_argument('--id', '-i', required=True, type=str,
                        help='author_id')
    parser.add_argument('--save', '-s', default="/",
                        help='save file name')
    parser.add_argument('--exclude', '-e', default=[], nargs='+', type=str,
                        help='want to exclude card id list')

    args = parser.parse_args()

    author_id = args.id
    save_dir = args.save
    exclude_list = args.exclude

    project_path = get_path()
    if os.path.isdir(project_path + save_dir):
        print("ok. save " + project_path + save_dir + " exist.")
    else:
        print("file no exist.")
        print("make file to ", project_path + save_dir)
        os.makedirs(project_path + save_dir)

    url = "http://www.aozora.gr.jp/index_pages/person" + author_id + ".html"
    body = get_body(get_request(url))

    card_ids = get_cards(body)
    author_id = zero_padding(author_id)

    for exclude in exclude_list:
        if exclude in card_ids:
            card_ids.remove(exclude)

    novel = Novel(author_id, project_path, save_dir)
    p = Pool(10)
    signal.signal(signal.SIGINT, handler)
    result = p.map(novel.save_novel_body, card_ids)

    # zip_code = []
    # for value in card_ids:
    #     if value not in exclude_list:
    #         novel_url = set_novel_url(author_id, value)
    #         novel_body = get_body(get_request(novel_url))
    #         zip_code.append(get_zip_code(novel_body, value))
    #     else:
    #         print("excluse ", str(value))

    # files = os.listdir(project_path + save_dir)

    # for value in zip_code:
    #     print(author_id)
    #     print(value)
    #     url = "http://www.aozora.gr.jp/cards/" + author_id + "/files/" + value
    #     if value not in files:
    #         result = download(url, project_path + save_dir, value)
    #         if result is False:
    #             print("download error:", url)
    #     else:
    #         print("zip file already exist")


if __name__ == "__main__":
    main()
