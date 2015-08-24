"""List & download versions available on BibleGateway"""
from lxml.html import parse


versions = parse('versions.html')


def list_versions():
    print('The following versions are available from BibleGateway:\n')
    for link in versions.findall('//a'):
        try:
            if link.attrib['href'].endswith('#booklist'):
                print(link.text)
        except KeyError:
            pass
    print('\nTo download version use `$ python download.py version`.')


def download(version):
    luke2 = parse('luke2.html').xpath('string()').split(version)[6]
    luke3 = parse('luke3.html').xpath('string()').split(version)[6]
    print(luke2, luke3)


if __name__ == '__main__':
    # download('LUTH1545')
    list_versions()
