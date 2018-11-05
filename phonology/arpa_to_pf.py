# arpa_to_pf.py
#
#
#
import panphon
import pandas as pd
import numpy as np
import pickle

def load_cmu():
    df = pd.read_csv('en-US.csv')
    df.drop(df.index[range(0,19)], inplace=True) # pandas DF uses 0-based index
    dict = {}
    for arpa, ipa in zip(df['Arpabet'], df['IPA']):
        dict[arpa.lower()] = ipa
    return dict


pft = panphon.FeatureTable()

phones = pd.read_csv('phones.txt', sep=' ', header=None)
#ps = phones.drop([0,1,49,50]) # remove <eps> sil, #0, #1
phones.columns = ['arpabet', 'idx']
arpa_to_ipa_dict = load_cmu()

arpa_to_pf_dict = {}
#
# cl, epi, vcl has no IPA label
# er pft is empty
# sil
# all these are mapped to [-1] * 22
for arpa, idx in zip(phones['arpabet'], phones['idx']):
    ipa = arpa_to_ipa_dict.get(arpa, '')
    if ipa:
        pf_vec = pft.word_to_vector_list(ipa, numeric=True)
        if not pf_vec:
            pf_vec = [[-1] * 22]
    else:
        pf_vec = [[-1] * 22]
    print('{}\t{}\t{}\t{}'.format(idx, arpa, ipa, [1 if x > 0 else 0 for x in pf_vec[0]]))
    arpa_to_pf_dict[idx] = [1 if x > 0 else 0 for x in pf_vec[0]]

# testing convert an idx numpy arry to 2D
labs = np.array([1,3,2,5])
mats = np.array([arpa_to_pf_dict[x] for x in labs])
print(mats.shape)
print(mats)

# pickle
with open('phone2pf.pickle', 'wb') as handle:
    pickle.dump(arpa_to_pf_dict, handle)