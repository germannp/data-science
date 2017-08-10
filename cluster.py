"""Dendrogram & heatmap for texts"""
import sys
import zlib
import itertools

import pandas as pd


def zipstance(text0, text1):
    """Similarity of texts based on compressability"""
    def zip_size(text):
        return sys.getsizeof(zlib.compress(bytes(text, 'UTF-8'), 9))

    return 2*zip_size(text0 + text1)/(zip_size(text0) + zip_size(text1)) - 1


def dist_matrix(texts, metric):
    dm = pd.DataFrame()
    for combo in itertools.combinations_with_replacement(texts.keys(), 2):
        dist = metric(texts[combo[0]], texts[combo[1]])
        dm.loc[combo[0], combo[1]] = dist
        dm.loc[combo[1], combo[0]] = dist
    return dm


if __name__ == '__main__':
    import argparse

    import seaborn as sns
    import matplotlib.pyplot as plt

    from luke23 import texts

    parser = argparse.ArgumentParser(description='Display a clustermap',
        epilog='If no selection is specified, a mix is used')
    parser.add_argument('-ls', '--list', action='store_true',
        help='list available versions')
    parser.add_argument('-a', '--all', action='store_true',
        help='use all available versions')
    parser.add_argument('-l', '--language', nargs='+',
        help='use versions of specified languages only')
    parser.add_argument('-v', '--version', nargs='+',
        help='use specified versions only')
    args = parser.parse_args()

    if args.list:
        selected_texts = None
        for key in texts: print(key)
    elif args.all:
        selected_texts = texts
    elif args.language:
        selected_texts = {key: texts[key] for key in texts
            if key.startswith(tuple(args.language))}
    elif args.version:
        selected_texts = {key: texts[key] for key in texts
            if key in args.version}
    else:
        selected_texts = {key: texts[key] for key in texts
            if key in ['cat-BCI', 'gsw-ZH', 'es-CST', 'gsw-BE', 'es-CST', 'es-NBD',
                'no-DNB1930', 'de-HOF', 'de-LUTH1545', 'nds-REIMER', 'gsw-VS', 'fr-BDS']}

    if selected_texts:
        dm = dist_matrix(selected_texts, zipstance)
        hm = sns.clustermap(dm, standard_scale=None, method='single', cmap='viridis', annot=True)
        plt.setp(hm.ax_heatmap.xaxis.get_majorticklabels(), rotation='vertical')
        plt.setp(hm.ax_heatmap.yaxis.get_majorticklabels(), rotation='horizontal')
        plt.savefig('map.png')
        plt.show()
