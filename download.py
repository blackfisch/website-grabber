#!/usr/bin/env python3

'''
    Download websites with respective CSS and JS to ensure functionality with ease.

    Usage: python download.py <url>
'''

import os
import re
import sys
import argparse
from shutil import rmtree
import requests
from bs4 import BeautifulSoup


# define helper functions
def get_valid_filename(name):
    '''
        Remove invalid characters from filename.

        @args name: filename to be cleaned
    '''
    def match(char):
        return re.match(r'[\w\d -.()\[\]\.,]', char)

    filename = ''.join(char for char in name if match(char) is not None)
    return filename


def save_file(path_l: list, sourceurl: str, cur_dir: str):
    '''
        Download file from sourceurl and save to path.

        @args path_l: list of path elements
        @args sourceurl: url of file to be downloaded
    '''
    print(f"downloading file {path_l[-1]}...")

    for subpath in path_l[:-1]:
        subpath = get_valid_filename(subpath)
        cur_dir = os.path.join(cur_dir, subpath)
        if not os.path.exists(cur_dir):
            os.mkdir(cur_dir)

    filename = get_valid_filename(path_l[-1])

    with open(os.path.join(cur_dir, filename), 'wb') as file:
        script_f = requests.get(sourceurl).content
        file.write(script_f)


def prep_url(sourceurl: str, site_url: str):
    '''
        Prepare url for download.

        @args sourceurl: url to be prepared
    '''
    if sourceurl.startswith('./'):
        sourceurl = f"{'/'.join(site_url.split('/')[:-1])}{sourceurl.replace('./','/')}"

    if sourceurl.startswith('/'):
        sourceurl = f"{site_url.split('/')[0]}//{site_url.split('/')[2]}{sourceurl}"

    path_l = sourceurl.replace('..', 'dot').split('/')

    if sourceurl.startswith('http'):
        path_l = path_l[3:]
    if sourceurl.startswith('..'):
        sourceurl = f"{'/'.join(site_url.split('/')[:-1])}"

        sourceurl = sourceurl.split('/')
        sourceurl = sourceurl[:-(path_l.count('dot'))]
        sourceurl = f"{'/'.join(sourceurl)}/{path_l[-1]}"

    return (sourceurl, path_l)


def download_page(site_url: str):
    '''
        Download page and save to file.
    '''
    # request url
    REQ = requests.get(site_url)
    SOUP = BeautifulSoup(REQ.content, 'html.parser')

    TITLE = None
    if SOUP.head.title is not None:
        TITLE = SOUP.head.title.contents[0]
    elif SOUP.title is not None:
        TITLE = SOUP.title.contents[0]
    else:
        TITLE = site_url.split('/')[2]

    CWD = os.getcwd()
    FOLDER = os.path.join(CWD, get_valid_filename(TITLE))

    if os.path.exists(FOLDER):
        rmtree(FOLDER)

    os.mkdir(FOLDER)

    # get links, dereference, download and save
    for link in SOUP.find_all('link'):
        if link.get('rel', [''])[0].lower() == 'stylesheet':

            source_url = link.get('href', '')

            (source, path) = prep_url(source_url, site_url)
            link['href'] = '/'.join(path)

            save_file(path, source, FOLDER)

    for script in SOUP.find_all('script'):
        if script.get('src', '') != '':
            source_url = script.get('src')

            (source, path) = prep_url(source_url, site_url)

            script['src'] = '/'.join(path)

            save_file(path, source, FOLDER)

    # fix relative links
    for link in SOUP.find_all('a'):
        href = link.get('href', '')
        if href.startswith('./'):
            link['href'] = f"{'/'.join(site_url.split('/')[:-1])}{href.replace('./','/')}"

        elif href.startswith('/'):
            link['href'] = f"{site_url.split('/')[0]}//{site_url.split('/')[2]}{href}"

        elif href.startswith('..'):
            href = href.split('/')
            dot_cnt = href.count('..')
            source_url = f"{'/'.join(site_url.split('/')[:-1])}"

            source_url = source_url.split('/')
            source_url = source_url[:-(dot_cnt)]
            source_url = f"{'/'.join(source_url)}/{'/'.join(href[dot_cnt:])}"

            link['href'] = source_url

    with open(os.path.join(FOLDER, 'index.html'), 'wb') as index_file:
        index_file.write(SOUP.encode())

    print()
    print(f"    Website '{TITLE}' saved to {FOLDER}")


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description='Download a website with html & css')
    PARSER.add_argument('url', metavar='URL', type=str,
                        nargs='?', help='full url to website')
    PARSER.add_argument('-f', '--file', metavar='FILE', type=str,
                        nargs='?', dest='file', help='specify input file')

    URL = PARSER.parse_args().url
    FILE = PARSER.parse_args().file

    if not URL:
        if FILE:
            print(f"Reading URLs from file {FILE}")
            with open(FILE, 'r') as file:
                for line in file.readlines():
                    URL = line.strip()
                    download_page(URL)
            sys.exit(0)

        else:
            URL = input("Please enter a url: ")

            if not URL:
                PARSER.print_help()
                sys.exit(1)

    download_page(URL)
