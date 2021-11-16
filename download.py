#!/usr/bin/env python3

import os
import requests
import argparse
import re
import unicodedata
from shutil import rmtree
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser(
    description='Download a website with html & css')
parser.add_argument('url', metavar='URL', type=str,
                    nargs='?', help='full url to website')

url = parser.parse_args().url

if not url:
    url = input("Please enter a url: ")

    if not url:
        parser.print_help()
        exit(1)


# define helper functions
def get_valid_filename(name):
    def match(c):

        m = re.match(r'[\w\d -.()\[\]\.,]', c)
        return m

    filename = ''.join(e for e in name if match(e) is not None)
    return filename


def save_file(path, sourceurl):
    # print(path, sourceurl)
    print(f"downloading file {path[-1]}...")

    cur_p = FOLDER
    for subpath in path[:-1]:
        subpath = get_valid_filename(subpath)
        cur_p = os.path.join(cur_p, subpath)
        if not os.path.exists(cur_p):
            os.mkdir(cur_p)

    filename = get_valid_filename(path[-1])

    with open(os.path.join(cur_p, filename), 'wb') as f:
        script_f = requests.get(sourceurl).content
        f.write(script_f)


def prep_url(sourceurl):
    if sourceurl.startswith('./'):
        sourceurl = f"{'/'.join(url.split('/')[:-1])}{sourceurl.replace('./','/')}"

    if sourceurl.startswith('/'):
        sourceurl = f"{url.split('/')[0]}//{url.split('/')[2]}{sourceurl}"

    path = sourceurl.replace('..', 'dot').split('/')

    if sourceurl.startswith('http'):
        path = path[3:]
    if sourceurl.startswith('..'):
        sourceurl = f"{'/'.join(url.split('/')[:-1])}"

        sourceurl = sourceurl.split('/')
        sourceurl = sourceurl[:-(path.count('dot'))]
        sourceurl = f"{'/'.join(sourceurl)}/{path[-1]}"

    return (sourceurl, path)


# request url

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

title = None
if soup.head.title is not None:
    title = soup.head.title.contents[0]
elif soup.title is not None:
    title = soup.title.contents[0]
else:
    title = url.split('/')[2]

CWD = os.getcwd()
FOLDER = os.path.join(CWD, get_valid_filename(title))

if (os.path.exists(FOLDER)):
    rmtree(FOLDER)

os.mkdir(FOLDER)

# get links, dereference, download and save
links = soup.find_all('link')
scripts = soup.find_all('script')

for link in links:
    if link.get('rel', [''])[0].lower() == 'stylesheet':

        sourceurl = link.get('href', '')

        (source, path) = prep_url(sourceurl)

        link['href'] = '/'.join(path)

        save_file(path, source)

for script in scripts:
    if script.get('src', '') != '':
        sourceurl = script.get('src')

        (source, path) = prep_url(sourceurl)

        script['src'] = '/'.join(path)

        save_file(path, source)

# fix relative links
for link in soup.find_all('a'):
    href = link.get('href', '')
    if href.startswith('./'):
        link['href'] = f"{'/'.join(url.split('/')[:-1])}{href.replace('./','/')}"

    elif href.startswith('/'):
        link['href'] = f"{url.split('/')[0]}//{url.split('/')[2]}{href}"

    elif href.startswith('..'):
        href = href.split('/')
        dot_cnt = href.count('..')
        sourceurl = f"{'/'.join(url.split('/')[:-1])}"

        sourceurl = sourceurl.split('/')
        sourceurl = sourceurl[:-(dot_cnt)]
        sourceurl = f"{'/'.join(sourceurl)}/{'/'.join(href[dot_cnt:])}"

        link['href'] = sourceurl

with open(os.path.join(FOLDER, 'index.html'), 'wb') as f:
    f.write(soup.encode())

print()
print(f"    Website '{title}' saved to {FOLDER}")
