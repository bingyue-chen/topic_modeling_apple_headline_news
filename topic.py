# -*- coding: utf-8 -*-

from gensim import corpora, models
from pprint import pprint
import csv
import pyLDAvis.gensim
import warnings
import logging

warnings.filterwarnings("ignore", category=DeprecationWarning)
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

# read doc words
print("read doc words...")
doc_words = list(csv.reader(open('cut_news.csv')))
len_doc_words = len(doc_words)

# cout words in doc frequent and doc words frequent
print("cout words in doc frequent and doc words frequent...")
dictionary = corpora.Dictionary(doc_words)
dictionary.filter_extremes(no_below=round(len_doc_words * 0.001), no_above=0.33, keep_n=round(len_doc_words * 0.1))
bow_corpus = [dictionary.doc2bow(doc) for doc in doc_words]

# tf-idf
print("compute tf-idf...")
tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]

# training best lda mdel
print("training best lda model...")
best_score = 0
m_n_t = len_doc_words * 0.001
for n_t in range(round(m_n_t * 0.5), round(m_n_t * 1.6), round(m_n_t * 0.2)):
    print(n_t, "start...")
    # lda training
    lda_model_tfidf = models.LdaModel(corpus_tfidf, num_topics=n_t, id2word=dictionary, passes=20, iterations=400, eval_every = None)

    # compute coherence score
    coherence_model_lda = models.CoherenceModel(model=lda_model_tfidf, texts=doc_words, dictionary=dictionary, coherence='c_v')
    coherence_score = coherence_model_lda.get_coherence()
    print(n_t, coherence_score)
    if coherence_score > best_score:
        best_score = coherence_score
        optimal_lda_model_tfidf = lda_model_tfidf

lda_model_tfidf = optimal_lda_model_tfidf
'''

# training lda mdel
n_t = round(len(doc_words) * 0.001)
print("training lda model...")
lda_model_tfidf = models.LdaModel(corpus_tfidf, num_topics=n_t, id2word=dictionary, passes=20, iterations=400, eval_every = None)
coherence_model_lda = models.CoherenceModel(model=lda_model_tfidf, texts=doc_words, dictionary=dictionary, coherence='c_v')
coherence_score = coherence_model_lda.get_coherence()
print(n_t, coherence_score)
'''

for idx, topic in lda_model_tfidf.print_topics(-1):
    pprint('Topic: {} Word: {}'.format(idx, topic))

#pprint('===============================================')

#pprint(lda_model_tfidf.get_document_topics(bow_corpus[0]))

#for index, score in sorted(lda_model_tfidf[bow_corpus[0]], key=lambda tup: -1*tup[1]):
#    pprint("\nScore: {}\t \nTopic: {}".format(score, lda_model_tfidf.print_topic(index, 10)))

data = pyLDAvis.gensim.prepare(lda_model_tfidf, bow_corpus, dictionary)
pyLDAvis.save_html(data,'vis.html')
