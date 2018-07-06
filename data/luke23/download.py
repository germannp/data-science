"""List & download versions available on BibleGateway"""
import os
import string
import requests
from lxml import html


versions = requests.get('https://www.biblegateway.com/versions/')
version_trs = html.fromstring(versions.text).xpath('//tr[@data-language]')


def list_versions():
    print('The following versions are available from BibleGateway:')
    _module_path = os.path.dirname(__file__)
    if _module_path == '':
        _module_path = '.'
    downloaded = [f for f in os.listdir(_module_path) if f.endswith('.txt')]
    for tr in version_trs:
        for span in tr.findall('.//span[@class="language-display"]'):
            print('\n' + span.text)
        for link in tr.findall('.//a[@href]'):
            if link.attrib['href'].endswith('#booklist'):
                version = link.text
                shorthand = version.split('(')[-1][:-1]
                if any([shorthand in file_name for file_name in downloaded]):
                    mark = '*'
                else:
                    mark = ''
                print(link.text + mark)
    print('\nDownloaded versions are marked with an *. To download additional ' \
        'versions use `$ python download.py version version1 ...`.')


def download(version):
    """Download version of Luke 2 & 3 as lang-version.txt w/o footnotes"""
    print('Downloading ' + version)
    base_url = 'https://www.biblegateway.com/passage/?search=Luke+'
    luke2_page = requests.get(base_url + '2&version=' + version)
    luke3_page = requests.get(base_url + '3&version=' + version)

    if 'Version not found' in luke2_page.text:
        print('Version ' + version + ' not found!')
        return

    luke2 = html.fromstring(luke2_page.text).xpath('string()').split(version)[6][2:]
    luke3 = html.fromstring(luke3_page.text).xpath('string()').split(version)[6][2:]

    luke2 = luke2.split('\n')[0] # Remove copyright note
    luke3 = luke3.split('23')[0] # Cut off at verse 22.

    # Remove trailing headline (if any)
    while luke3.strip()[-1].isalnum():
        luke3 = luke3.strip()[:-1]
    luke3 = luke3.strip()

    luke23 = luke2 + luke3
    for char in string.ascii_lowercase:
        footnote = '[' + char + ']'
        if footnote in luke23:
            luke23 = luke23.replace(footnote, '')
        else:
            break

    for tr in version_trs:
        if version in tr.xpath('string()'):
            lang = tr.attrib['data-language']
            break

    with open(lang + '-' + version + '.txt', 'w') as file:
        file.write((luke23).replace(u'\xa0', u' '))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='List & download versions '
        'of Luke 2 & 3 from BibleGateway.')
    parser.add_argument('-l', '--list', action='store_true',
        help='list available versions')
    parser.add_argument('versions', metavar='versions', type=str, nargs='*',
        help='versions to download')
    args = parser.parse_args()

    if args.list == True or (args.list == False and len(args.versions) == 0):
        list_versions()
    for version in args.versions:
        download(version)
