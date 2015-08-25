"""List & download versions available on BibleGateway"""
from lxml.html import parse


version_trs = parse('versions.html').xpath('//tr[@data-language]')


def list_versions():
    print('The following versions are available from BibleGateway:')
    for tr in version_trs:
        for span in tr.findall('.//span[@class="language-display"]'):
            print('\n' + span.text)
        for link in tr.findall('.//a[@href]'):
            # TODO: Print * if already downloaded
            if link.attrib['href'].endswith('#booklist'):
                print(link.text)
    print('\nTo download version use `$ python download.py version`.')


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
    # list_versions()
    download('LUTH1545')
