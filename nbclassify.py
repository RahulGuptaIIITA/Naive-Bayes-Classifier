import re
import sys
import json
import math
import string


class NBClassify:
    
    def __init__(self):
        
        self.pos_prior_prob = 0
        self.neg_prior_prob = 0
        self.fake_prior_prob = 0
        self.true_prior_prob = 0
        self.word_conditional_prob = dict()
        self.tr = string.maketrans(string.punctuation, ' ' * len(string.punctuation))
        
        with open("nbmodel.txt") as file:
            lines = file.readlines()
            for line in lines:
                var_obj = json.loads(line)
                if var_obj['type'] == "prior":
                    for prob in var_obj['prob']:
                        if prob[0] == 'neg':
                            self.neg_prior_prob = prob[1]
                        elif prob[0] == 'pos':
                            self.pos_prior_prob = prob[1]
                        elif prob[0] == 'true':
                            self.true_prior_prob = prob[1]
                        elif prob[0] == 'fake':
                            self.fake_prior_prob = prob[1]
                
                elif var_obj['type'] == "condp":
                    word = var_obj['word']
                    self.word_conditional_prob[word] = dict()
                    for prob in var_obj['prob']:
                        if prob[0] == 'neg':
                            self.word_conditional_prob[word]['neg'] = prob[1]
                        elif prob[0] == 'pos':
                            self.word_conditional_prob[word]['pos'] = prob[1]
                        elif prob[0] == 'true':
                            self.word_conditional_prob[word]['true'] = prob[1]
                        elif prob[0] == 'fake':
                            self.word_conditional_prob[word]['fake'] = prob[1]
                            
        return
 
    def cal_pos_prob(self, words):
        pos = math.log10(self.pos_prior_prob)
        neg = math.log10(self.neg_prior_prob)
        true = math.log10(self.true_prior_prob)
        fake = math.log10(self.fake_prior_prob)
        
        for word in words:
            
            if word in self.word_conditional_prob:
                pos = pos + math.log10(self.word_conditional_prob[word]['pos'])
                neg = neg + math.log10(self.word_conditional_prob[word]['neg'])
                true = true + math.log10(self.word_conditional_prob[word]['true'])
                fake = fake + math.log10(self.word_conditional_prob[word]['fake'])
        
        label1 = 'True' if true > fake else 'Fake'
        label2 = 'Pos' if pos > neg else 'Neg'
        
        return label1, label2
 
    def classify_sentence(self, sentence, file_object):
        sentence = sentence.strip()
        #sentence = re.sub(r'[^\w\s]', '', sentence)
        sentence = sentence.translate(self.tr)
        tokens = sentence.split(" ")
        
        hash = tokens[0]
        words = tokens[1:]
        words = [word.lower() for word in words]
        
        label1, label2 = self.cal_pos_prob(words)
        file_object.write(hash + " " + label1 + " " + label2 + "\n")
        
        return
    
    def run(self, infile):
        try:
            file_object = open("nboutput.txt", "w")
            with open(infile) as file:
                sentences = file.readlines()
                for sentence in sentences:
                    self.classify_sentence(sentence, file_object)
                    
            file_object.close()
        
        except Exception as e:
            print (e)
        
        return


if __name__ == "__main__":
    infile = sys.argv[1]

    nb_classify_object = NBClassify()
    nb_classify_object.run(infile)

