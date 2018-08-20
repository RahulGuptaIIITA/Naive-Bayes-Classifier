# Naive-Bayes-Classifier
A Naive Bayes Classifier to identify hotel reviews as either true or fake, and either positive or negative. We will be using 
the word tokens as features for classification


# Data
A set of training and development data is given.

One file train-labeled.txt containing labeled training data with a single training instance (hotel review) per line (total 960 lines). The first 3 tokens in each line are:
a unique 7-character alphanumeric identifier
a label True or Fake
a label Pos or Neg
These are followed by the text of the review.
One file dev-text.txt with unlabeled development data, containing just the unique identifier followed by the text of the review (total 320 lines).
One file dev-key.txt with the corresponding labels for the development data, to serve as an answer key.


# Programs
Two programs: nblearn.py will learn a naive Bayes model from the training data, and nbclassify.py will use the model to classify new data.
