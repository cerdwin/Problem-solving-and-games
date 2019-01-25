def compute_word_frequencies(path):
  dictionary = {}
  with open(path, "r", encoding = "utf-8") as f:
    for line in f:
      line = line.rstrip()
      words = line.split()
        for word in words:
          dictionary[word]=dictionary.get(word, 0)+1
  return dictionary
