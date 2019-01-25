def count_rows_and_words(path):
  lines = 0
  words = 0
  with open(path, "r", encoding = "utf-8") as f:
    for line in f.readlines():
        lines = lines + 1
 
        words_in_line = line.split()
        words = words + len(words_in_line)
 
  return(lines, words)
