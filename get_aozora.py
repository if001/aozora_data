"""
This program get aozora_bunko novels.
To do it, you set author_id as option.

example,
$ python3 get_aozora.py -id <savefname>

"""

import urllib.request
import os
import sys


def get_body(url):
    try:
        response = urllib.request.urlopen(url)
        print(">>>> get body : ", url)
        return response.read().decode('utf-8')
    except:
        print(" ----- html error code", url)
        return ""


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


def get_novel_body(authorId, cardId):
    url = "http://www.aozora.gr.jp/cards/" + authorId + "/card" + cardId + ".html"
    return get_body(url)


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
    try:
        urllib.request.urlretrieve(url, savedir + filename)
        print("save ok to " + savedir + filename)
    except:
        print("html error cood", url)
        return ""


def get_path():
    return os.path.dirname(os.path.abspath(__file__))


import argparse


def main():
    parser = argparse.ArgumentParser(description='get aozora')
    parser.add_argument('--id', '-i', required=True, type=str,
                        help='author_id')
    parser.add_argument('--save', '-s', default="/",
                        help='save file name')
    parser.add_argument('--exclude', '-e', default=None, nargs='+', type=str,
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
    body = get_body(url)
    card_ids = get_cards(body)

    author_id = zero_padding(author_id)

    zip_code = []

    for value in card_ids:
        if value not in exclude_list:
            body = get_novel_body(author_id, value)
            zip_code.append(get_zip_code(body, value))
        else:
            print("excluse ", str(value))

    files = os.listdir(project_path + save_dir)

    for value in zip_code:
        print(author_id)
        print(value)
        url = "http://www.aozora.gr.jp/cards/" + author_id + "/files/" + value
        if value not in files:
            download(url, project_path + save_dir, value)
        else:
            print("zip file already exist")


if __name__ == "__main__":
    main()
