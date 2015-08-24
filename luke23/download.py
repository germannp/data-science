"""List & download versions available on BibleGateway"""
from lxml.html import parse


version_trs = parse('versions.html').xpath('//tr[@data-language]')


def list_versions():
    print('The following versions are available from BibleGateway:')
    for tr in version_trs:
        for span in tr.findall('.//span[@class="language-display"]'):
            print('\n' + span.text)
        for link in tr.findall('.//a[@href]'):
            if link.attrib['href'].endswith('#booklist'):
                print(link.text)
    print('\nTo download version use `$ python download.py version`.')


def download(version):
    print('Downloading ' + version)
    luke2 = parse('luke2.html').xpath('string()').split(version)[6]
    luke3 = parse('luke3.html').xpath('string()').split(version)[6]
    print(luke2, luke3)

    for tr in version_trs:
        if version in tr.xpath('string()'):
            lang = tr.attrib['data-language']
            break
    print(lang + '-' + version)


if __name__ == '__main__':
    # download('LUTH1545')
    list_versions()
