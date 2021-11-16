# Website downloader
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![GitHub issues](https://img.shields.io/github/issues-raw/BlackFisch/website-grabber)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Blackfisch/website-grabber)
[![Pylint](https://github.com/BlackFisch/website-grabber/actions/workflows/pylint.yml/badge.svg)](https://github.com/BlackFisch/website-grabber/actions/workflows/pylint.yml)

## What can it do?
This project aims to provide an easy-to-use CLI tool for downloading whole websites. This can be useful for academic uses as well as archive purposes.

This tool however only downloads the provided HTML file as well as related CSS/JS files. Hyperlinks are retained intact to link to webpages.


## Requirements
* Python 3
* pip
* requests (see [Installation](#Installation))
* BeautifulSoup (see [Installation](#Installation))

## Installation
You can just install the dependencies using pip: `pip install -r requirements.txt`

If you want to manually install the required packages using your preferrec package manager, see [requirements.txt](requirements.txt) for a list of packages

## Usage
Run the Python script `download.py`. You can pass the URL to download as a parameter, otherwise you will be prompted to enter it.

Example: `python download.py https://google.com`

## Issues & Features
If you find any problems or have a feature request, feel free to open an Issue or Pull Request.

## License
This project is licensed under **GNU General Public License v3.0**.

[Full License Text](LICENSE.md)