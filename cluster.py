"""Dendrogram & heatmap for texts"""
import sys
import zlib


def zipstance(text0, text1):
    """Similarity of texts based on compressability"""
    def zip_size(text):
        return sys.getsizeof(zlib.compress(bytes(text, 'UTF-8'), 9))

    return zip_size(text0 + text1) - (zip_size(text0) + zip_size(text1))/2


if __name__ == '__main__':
    from luke23 import texts

    print(zipstance(texts['gsw-BE'], texts['gsw-BE']))
    print(zipstance(texts['gsw-VS'], texts['gsw-VS']))
    print(zipstance(texts['de-HOF'], texts['de-HOF']))
    print(zipstance(texts['gsw-BE'], texts['gsw-VS']))
    print(zipstance(texts['gsw-BE'], texts['de-HOF']))
    print(zipstance(texts['gsw-BE'], texts['de-LUTH1545']))
    print(zipstance(texts['gsw-BE'], texts['cat-BCI']))
    print(zipstance(texts['no-DNB1930'], texts['cat-BCI']))
    print(zipstance(texts['gsw-BE'], texts['no-DNB1930']))
