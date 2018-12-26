# pdf_to_pf.py
#
# based on arpa_to_pf.py
#
# - load phone_pdf to get phone hmm-idx pdf
# - for each phone, if len(pf_vec) > 1
#       if idx=0 use pf_vec[0]
#       if idx=1 use averaged
#       if idx=2 use pf_vec[1]
#
#
import panphon
import pandas as pd
import numpy as np
import pickle
import re

def load_cmu():
    df = pd.read_csv('en-US.csv')
    df.drop(df.index[range(0,19)], inplace=True) # pandas DF uses 0-based index
    dict = {}
    for arpa, ipa in zip(df['Arpabet'], df['IPA']):
        dict[arpa.lower()] = ipa
    return dict


def load_pdf():
    """
    Transition-state 2: phone = sil hmm-state = 1 pdf = 49

    :return:
    """
    pdf_dict = {}
    with open('phone_pdf', 'r') as PDF:
        lns = [ln.rstrip() for ln in PDF.readlines()]
        for ln in lns:
            m = re.match('^Transition-state \d+: phone = (\S+) hmm-state = (\d+) pdf = (\d+)', ln)
            if m:
                phone = m.group(1)
                state = m.group(2)
                pdf = m.group(3)
                pdf_dict[pdf] = [phone, state]
    return pdf_dict


if __name__ == '__main__':

    pft = panphon.FeatureTable()

    # load TIMIT phone file, note that TIMIT used several ARPANET phones beyond CMU
    # phones = pd.read_csv('phones.txt', sep=' ', header=None)
    # ps = phones.drop([0,1,49,50]) # remove <eps> sil, #0, #1
    # phones.columns = ['arpabet', 'idx']

    arpa_to_ipa_dict = load_cmu()

    pdf_dict = load_pdf()

    pdf_to_pf_dict = {}
    #
    # cl, epi, vcl has no IPA label
    # er pft is empty
    # sil
    # all these are mapped to [-1] * 22
    for pdf, phone_state in pdf_dict.items():
        phone = phone_state[0]
        state = phone_state[1]

        ipa = arpa_to_ipa_dict.get(phone, '')
        if ipa:
            pf_vec = pft.word_to_vector_list(ipa, numeric=True)
            if not pf_vec:
                pf_vec = [[-1] * 22]
        else:
            pf_vec = [[-1] * 22]

        if len(pf_vec) > 1:  # state 0,1 => pf_vec[0], state 2 => pf_vec[1]
            idx = 0 if int(state) < 2 else 1
        else:
            idx = 0
        print('{}\t{}\t{}\t{}\tidx={}\t{}'.format(pdf, phone, ipa, state, idx, [1 if x > 0 else 0 for x in pf_vec[idx]]))
        pdf_to_pf_dict[pdf] = [1 if x > 0 else 0 for x in pf_vec[idx]]

    # pickle
    with open('pdf2pf.pickle', 'wb') as handle:
        pickle.dump(pdf_to_pf_dict, handle)