#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the TrainingCorpus class.

TrainingCorpus assumes that the !truth.txt file exists 
in the corpus directory and uses the contained information 
to provide additional functionality.
"""

import unittest

from trainingcorpus import TrainingCorpus

import os
import random
from collections import Counter
from test_readClassificationFromFile import (
    save_classification_to_file,
    replaced_open)
from test_corpus import (
    create_corpus_dictionary,
    create_corpus_dir_from_dictionary,
    delete_corpus_directory,
    CORPUS_DIR
    )

HAM_TAG = 'OK'
SPAM_TAG = 'SPAM'
TRUTH_FILENAME = '!truth.txt'

class TrainingCorpusTest(unittest.TestCase):
    
    def setUp(self):
        """Prepare fake corpus with !truth.txt file."""
        self.email_dict = create_corpus_dictionary()
        self.true_class = create_classification_for(self.email_dict.keys())
        create_corpus_dir_from_dictionary(self.email_dict)
        truth_filepath = os.path.join(CORPUS_DIR, TRUTH_FILENAME)
        save_classification_to_file(self.true_class, fname=truth_filepath)
        with replaced_open():
            self.tc = TrainingCorpus(CORPUS_DIR)
        
    def tearDown(self):
        delete_corpus_directory()
        
    def test_getClass(self):
        """Test the get_class method."""
        for key, exp_class in self.true_class.items():
            with replaced_open():
                obs_class = self.tc.get_class(key)
            self.assertEqual(
                exp_class, obs_class,
                'The expected class of email {} is {}, but {} was observed'.format(
                    key, exp_class, obs_class)
            )

    def test_isSpam(self):
        """Test the is_spam method."""
        for key, exp_class in self.true_class.items():
            exp_spam = (exp_class==SPAM_TAG)
            with replaced_open():
                obs_spam = self.tc.is_spam(key)
            self.assertEqual(
                exp_spam, obs_spam,
                'The email {} spamminess: expected {}, observed {}.'.format(
                    key, str(exp_spam), str(obs_spam))
            )

    def test_isHam(self):
        """Test the is_ham method."""
        for key, exp_class in self.true_class.items():
            exp_ham = (exp_class==HAM_TAG)
            with replaced_open():
                obs_ham = self.tc.is_ham(key)
            self.assertEqual(
                exp_ham, obs_ham,
                'The email {} hamminess: expected {}, observed {}.'.format(
                    key, str(exp_ham), str(obs_ham))
            )

    def test_spams(self):
        """Test spams() method."""
        obs_num_spams = 0
        with replaced_open():
            for fname, contents in self.tc.spams():
                obs_num_spams += 1
                # Validate results
                self.assertEqual(self.true_class[fname], SPAM_TAG,
                                 'Non-spam email returned by spams() method.')
                self.assertEqual(self.email_dict[fname], contents,
                                 'The read file contents are not equal to the expected contents.')
        c = Counter(self.true_class.values())
        exp_num_spams = c[SPAM_TAG]
        self.assertEqual(exp_num_spams, obs_num_spams,
                         'The spams() method did not return the right number of spams.')        
    
    def test_hams(self):
        """Test hams() method."""
        obs_num_hams = 0
        with replaced_open():
            for fname, contents in self.tc.hams():
                obs_num_hams += 1
                # Validate results
                self.assertEqual(self.true_class[fname], HAM_TAG,
                                 'Spam email returned by hams() method.')
                self.assertEqual(self.email_dict[fname], contents,
                                 'The read file contents are not equal to the expected contents.')
        c = Counter(self.true_class.values())
        exp_num_hams = c[HAM_TAG]
        self.assertEqual(exp_num_hams, obs_num_hams,
                         'The hams() method did not return the right number of hams.')        

def create_classification_for(keys):
    """Create a fake classification dictionary for the email filenames in keys."""
    d = {}
    TRUTH_VALUES = [HAM_TAG, SPAM_TAG]
    for key in keys:
        d[key] = random.choice(TRUTH_VALUES)
    return d
    
if __name__=="__main__":
    unittest.main()
