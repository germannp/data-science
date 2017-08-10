"""Dendrogram & heatmap for texts

usage: cluster.py [-h] [-l] [-a] [-v VERSION ...]

optional arguments:
  -h, --help        show this help message and exit
  -l, --list        list available versions
  -a, --all         use all available versions
  -v, --version  VERSION ...
                    use specified versions only

If no selection is specified, a mix is used
"""
import sys
import zlib
import itertools

import pandas as pd


def zipstance(text0, text1):
    """Similarity of texts based on compressability"""

    def zipsize(text):
        return sys.getsizeof(zlib.compress(bytes(text, 'UTF-8'), 9))

    return 2 * zipsize(text0 + text1) / (zipsize(text0) + zipsize(text1)) - 1


def dist_matrix(texts, metric):
    dm = pd.DataFrame()
    for combo in itertools.combinations_with_replacement(texts.keys(), 2):
        dist = metric(texts[combo[0]], texts[combo[1]])
        dm.loc[combo[0], combo[1]] = dist
        dm.loc[combo[1], combo[0]] = dist
    return dm


if __name__ == '__main__':
    from docopt import docopt

    import seaborn as sns
    import matplotlib.pyplot as plt

    from luke23 import texts

    args = docopt(__doc__)

    if args['--list']:
        selected_texts = None
        for key in texts:
            print(key)
    elif args['--all']:
        selected_texts = texts
    elif args['--version']:
        selected_texts = {
            key: texts[key] for key in texts
            if key.startswith(tuple(args['VERSION']))}
    else:
        selected_texts = {
            key: texts[key] for key in texts
            if key in [
                'cat-BCI', 'gsw-ZH', 'es-CST', 'gsw-BE', 'es-CST', 'es-NBD',
                'no-DNB1930', 'de-HOF', 'de-LUTH1545', 'nds-REIMER', 'gsw-VS',
                'fr-BDS']}

    if selected_texts:
        dm = dist_matrix(selected_texts, zipstance)
        hm = sns.clustermap(
            dm, standard_scale=None, method='single', cmap='viridis',
            annot=True)
        plt.setp(
            hm.ax_heatmap.xaxis.get_majorticklabels(), rotation='vertical')
        plt.setp(
            hm.ax_heatmap.yaxis.get_majorticklabels(), rotation='horizontal')
        plt.savefig('map.png')
        plt.show()
