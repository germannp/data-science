"""List & download versions available on BibleGateway"""
import os
from lxml.html import parse


version_trs = parse('versions.html').xpath('//tr[@data-language]')


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
    print('\nDownloaded versions are marked with an *. To download any version ' \
        'use `$ python download.py version`.')


def download(version):
    """Download version of Luke 2 & 3 and save as lang-version.txt"""
    print('Downloading ' + version)
    luke2 = parse('luke2.html').xpath('string()').split(version)[6][2:]
    luke3 = parse('luke3.html').xpath('string()').split(version)[6][2:]

    luke2 = luke2.split('\n')[0] # Remove copyright note
    luke3 = luke3.split('23')[0] # Cut off at verse 22.

    for tr in version_trs:
        if version in tr.xpath('string()'):
            lang = tr.attrib['data-language']
            break

    with open(lang + '-' + version + '.txt', 'w') as file:
        file.write((luke2 + luke3).replace(u'\xa0', u' '))


if __name__ == '__main__':
    list_versions()
    # download('LUTH1545')
