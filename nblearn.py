import re
import sys
import json
import string


class NBLearn:
    
    def __init__(self):
        
        # variables
        self.pos_sentence = 0
        self.neg_sentence = 0
        self.fake_sentence = 0
        self.true_sentence = 0
        
        self.label_pos_dict = dict()
        self.label_neg_dict = dict()
        self.label_true_dict = dict()
        self.label_fake_dict = dict()
        self.unique_words_set = set()
        
        self.stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
            'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
            'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
            'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
            'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
            'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
            'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
            'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
            'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only'
            , 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
        ]
        
        self.tr = string.maketrans(string.punctuation, ' ' * len(string.punctuation))
        
        return
    
    def calculate_probabilities(self, word, label_dict):
        p = 0
        denom = len(self.unique_words_set) + sum(label_dict.values())
            
        if word in label_dict:
            p = (label_dict[word]+1)/float(denom)
        else:
            p = 1/float(denom)
            
        return p
    
    def save_model(self):
        prob = []
        file_object = open("nbmodel.txt", "w")
        
        # saving class prob
        p = self.neg_sentence/float(self.neg_sentence + self.pos_sentence)
        prob.append(('neg', p))
        p = self.pos_sentence/float(self.neg_sentence + self.pos_sentence)
        prob.append(('pos', p))
        p = self.fake_sentence/float(self.true_sentence + self.fake_sentence)
        prob.append(('fake', p))
        p = self.true_sentence/float(self.true_sentence + self.fake_sentence)
        prob.append(('true', p))
        
        obj = {
            'type': 'prior',
            'prob': prob
        }
        file_object.write(json.dumps(obj) + "\n")
        
        # saving conditional prob
        for word in self.unique_words_set:
            prob = []
        
            p = self.calculate_probabilities(word, self.label_pos_dict)
            prob.append(('pos', p))
            p = self.calculate_probabilities(word, self.label_neg_dict)
            prob.append(('neg', p))
            p = self.calculate_probabilities(word, self.label_fake_dict)
            prob.append(('fake', p))
            p = self.calculate_probabilities(word, self.label_true_dict)
            prob.append(('true', p))
            
            obj = {
                'type': 'condp',
                'word': word,
                'prob': prob
            }
            file_object.write(json.dumps(obj) + "\n")
            
        file_object.close()
        
        return
    
    def parse_sentence(self, sentence):
        sentence = sentence.strip()
        #sentence = re.sub(r'[^\w\s]', '', sentence)
        sentence = sentence.translate(self.tr)
        tokens = sentence.split(" ")
        
        hash = tokens[0]
        label1 = tokens[1]
        label2 = tokens[2]
        words = tokens[3:]
        
        if label1 == 'Fake':
            self.fake_sentence += 1
        elif label1 == 'True':
            self.true_sentence += 1
        
        if label2 == 'Pos':
            self.pos_sentence += 1
        elif label2 == 'Neg':
            self.neg_sentence += 1
        
        words = [word.lower() for word in words]
        for word in words:
                
            if label1 == 'Fake' and word not in self.stop_words:
                if word not in self.label_fake_dict:
                    self.label_fake_dict[word] = 0
                self.label_fake_dict[word] += 1
            
            elif label1 == 'True' and word not in self.stop_words:
                if word not in self.label_true_dict:
                    self.label_true_dict[word] = 0
                self.label_true_dict[word] += 1
            
            if label2 == 'Pos' and word not in self.stop_words:
                if word not in self.label_pos_dict:
                    self.label_pos_dict[word] = 0
                self.label_pos_dict[word] += 1
            
            elif label2 == 'Neg' and word not in self.stop_words:
                if word not in self.label_neg_dict:
                    self.label_neg_dict[word] = 0
                self.label_neg_dict[word] += 1
            
            if word not in self.stop_words:
                self.unique_words_set.add(word)
 
        return
    
    def run(self, infile):
        try:
            with open(infile) as file:
                sentences = file.readlines()
                for sentence in sentences:
                    self.parse_sentence(sentence)
            self.save_model()
            
        except Exception as e:
            print (e)
        
        return


if __name__ == "__main__":
    infile = sys.argv[1]
    nb_learn_object = NBLearn()
    nb_learn_object.run(infile)
