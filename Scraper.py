"""
Requirements
Needs python 3.6
"""

import os.path
import requests
import sys


def link_preperation(url):
    links_final = []
    if not os.path.exists("videos.txt"):
        r = requests.get(url + "videos.txt")
        open('videos.txt', 'wb').write(r.content)
    with open("videos.txt") as f:
        links_list_raw = (f.read().splitlines())
    for prepared_end in links_list_raw:
        links_final.append(prepared_end.replace(" ", "%20"))
    return links_final


def download(url, path, iteration):
    with open(path, 'wb') as f:
        sys.stdout.write(f"Downloaded started | File number : {iteration}")
        response = requests.get(url, stream=True)
        total = response.headers.get('content-length')

        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                downloaded += len(data)
                f.write(data)
                done = int(50 * downloaded / total)
                sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50 - done)))
                sys.stdout.flush()
            print()
            sys.stdout.write(f"File Number {iteration} downloaded!")
    sys.stdout.write('\n')


if __name__ == '__main__':
    itr = 0
    print("***** SCRAPER ******")
    to_download = input("Paste the link where the videos are located: ")
    file_input = input("Enter the Location where you want to download: ")
    links_list = link_preperation(to_download.rstrip())

    for query in links_list:
        dwn_link = to_download + query + ".mp4"

        file_name = query.replace("%20", " ")
        file_path = file_input + "\\" + file_name + ".mp4"

        itr += 1
        if os.path.exists(file_path):
            print("Already Downloaded.. Skipped!")
            continue
        else:
            download(dwn_link, file_path, itr)
