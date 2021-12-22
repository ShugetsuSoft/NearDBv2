# -*- coding: utf-8 -*-

from transformers import BertTokenizer, TFBertModel
import numpy

class Transform():
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
        self.model = TFBertModel.from_pretrained("bert-base-multilingual-cased")

    def getFeature(self, word):
        encoded_input = self.tokenizer(word, return_tensors='tf')
        output = self.model(encoded_input)
        return output[1].numpy()

    def getTagsFeature(self, words):
        return numpy.squeeze(sum([self.getFeature(word) for word in words])/len(words))
        #return numpy.squeeze(getFeature(" ||| ".join(words)))

'''
from bert_serving.client import BertClient
bc = BertClient(ip='172.16.25.211')
c = bc.encode(['First do it', 'then do it right', 'then do it better'])
'''