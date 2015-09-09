"""Dendrogram & heatmap for texts"""
import sys
import zlib
import itertools

import pandas as pd


def zipstance(text0, text1):
    """Similarity of texts based on compressability"""
    def zip_size(text):
        return sys.getsizeof(zlib.compress(bytes(text, 'UTF-8'), 9))

    return zip_size(text0 + text1) - (zip_size(text0) + zip_size(text1))/2


def dist_matrix(texts, metric):
    dm = pd.DataFrame()
    for combo in itertools.combinations_with_replacement(texts.keys(), 2):
        dist = metric(texts[combo[0]], texts[combo[1]])
        dm.loc[combo[0], combo[1]] = dist
        dm.loc[combo[1], combo[0]] = dist
    return dm


if __name__ == '__main__':
    import seaborn as sns
    import matplotlib.pyplot as plt

    from luke23 import texts
    from colormaps import *

    dm = dist_matrix(texts, zipstance)
    sns.clustermap(dm, standard_scale=1, xticklabels=False, cmap=viridis)
    plt.show()
