How to use pytorch-kaldi

# train multi-label PF DNN model using TIMIT

- generate the mapping from pdf to PF label
  - phonology/pdf_to_pf.py
  - also need phone_pdf, which is from Kaldi egs
    
    `
    show-transitions ../phones.txt ../final.mdl > hmminfo
    cat hmminfo | grep 'pdf =' > phone_pdf
    `  
  - the generated pdf2pf.pickle file stores mapping from pdf->pf label
  - **found pdfs generated on local darwin and remote AWS are diff, have to use ONE kaldi system**
   
- follow pytorch-kaldi instructions
  - run FA on train, dev, and test  
  - see prep_test_bell.sh to know how to setup data/test_bell dir and then can use tri3 GMM AM to do FA.
  - see dnnfa_test_bell.sh to know how to use DNN AM to do FA
    - pdfs are determined by tri-phone model 
  - define cfg, see cfg/multi_label.cfg
  - call multi_label.sh cfg/multi_label.cfg to use 1 GPU to train PF DNN model  

# apply on forger_mp dataset
  - use bell_prep_cfg.sh, which generates cfg file for each chunk and apply the trained PF DNN model.
  - see cfg/bell_mp.cfg
  - the saved pickle files cotain PF vectors for each audio frame
 
