melingo
=======
Compression algorithms have been used in information theoretical studies before. Here we explore their potential to quantify diversity of languages, by compressing different versions of biblical texts together:

![Clustering bible versions](clusters.png)

The bible is probably the text available in most varieties of the germanic and romanic languages we are interested in. To minimize interpretation and theology we picked Luke 2 (and parts of 3) as this nativity story is arguably the most popular biblical narration.

To install the required python libraries run `$ pip install -r requirements.txt`, to download additional versions checkout `$ python luke23/download.py --help`, and to play with clustering `$ python cluster.py --help`.
