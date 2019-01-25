def read_classification_from_file(path):
    """
    Method already used in previous submission
    :param path: path towards an email
    :return: a dictionary of email names and their classification
    """
    dictionary = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()  # removing end-of-string characters
            if line:
                key, value = line.split(" ")    # splitting individual line reads with space
                dictionary[key] = value     # each name becomes a key and its status OK/SPAM, respective  dict. value
    return dictionary   # returning dictionary with classifications of each file
