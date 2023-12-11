import glob
import numpy as np

rank_files = glob.glob("*_rank.npy")
suffix_len = len("_rank.npy")

RERANK = int(open("RERANK.int").read())

ranks = []
casenumbers = []
Xs = []
ys = []
for rank_file in rank_files:
    X = np.load(rank_file[:-suffix_len] + "_X.npy")
    casenumbers.append(rank_file[:suffix_len])
    if X.shape[0] != RERANK:
        print(rank_file[:-suffix_len])
        continue

    rank = np.load(rank_file)[0]
    ranks.append(rank)
    y = np.load(rank_file[:-suffix_len] + "_y.npy")
    Xs.append(X)
    ys.append(y)

ranks = np.array(ranks)
total_queries = len(ranks)
print("Total Queries: {0}".format(total_queries))
print("Top 1: {0}".format((ranks == 1).sum() / total_queries))
print("Top 3: {0}".format((ranks <= 3).sum() / total_queries))
print("Top 5: {0}".format((ranks <= 5).sum() / total_queries))
print("Top 10: {0}".format((ranks <= 10).sum() / total_queries))