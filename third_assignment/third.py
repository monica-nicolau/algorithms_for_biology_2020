import sys
# If you want to run the code with on a specific text file,
# use the following syntax: $ python3 MONICA_NICOLAU.py inputfile.txt

# If the input sequence is a genomic (DNA) one use the following alphabet:
genomic_alphabet = 'ATCG'
# For prokaryotic genomes, gene transcripts, RNA sequences use the following alphabet:
# alphabet_with_uracile = 'AUGC'  


def read_instance(file_name, alphabet):

  # Given a text file and the proper alphabet, the function
  # returns the pattern length, the maximum Hamming distance
  # and the string to be analysed (variables that correspond 
  # to the three lines of the text file).

    with open(file_name, "r") as file:
        pattern_length = int(file.readline())
        max_distance = int(file.readline())
        string = file.readline().strip()

    if pattern_length <= 0 or max_distance <= 0: raise ValueError
    for character in string:
        if character not in alphabet: raise ValueError

    return (pattern_length, max_distance, string)

def check_hamming_distance(string1, string2, allowed_distance):

  # Given two strings of the same length and the allowed Hamming 
  # distance (an integer), the function computes the value of the 
  # Hamming distance and return True if the computed distance is
  # less or equal than the allowed one, False otherwise.

    distance = 0
    for character1, character2 in zip(string1, string2):
        if character1 != character2:
            distance += 1
            if distance > allowed_distance:
                return False
    return True


def patterns_generator(pattern_length, alphabet):  # wrapper function

  # Given the pattern_length and the alphabet from which our main
  # string is taken, successively generates all permutations (of length
  # equal to pattern_length) of the characters belonging to the selected
  # alphabet.

    pattern = ''

    def sub_patterns_generator():

      # To every pattern a nucleotide is added until pattern_length
      # becomes 0, i.e there are no more nucleotides to be added. 
      # When this condition is satisfied, the pattern is yielded.
      # The recursive nature of this generator guarantees that all
      # the possibile permutations of length pattern_length of the
      # characters belonging to the alphabet are generated. 

        nonlocal pattern_length, pattern

        if pattern_length == 0:
            yield pattern

        else:
            for nucleotide in alphabet:
                pattern += nucleotide
                pattern_length -= 1

                yield from sub_patterns_generator()

                pattern = pattern[:-1]
                pattern_length += 1

    yield from sub_patterns_generator()

def count_approximate_occurrences(pattern, genome, maximum_distance):

  # Given a single pattern, the genome string and the allowed
  # Hamming distance, the function return the number of approximate
  # occurrences of the input pattern in the genome string.

    approximate_occurrences = 0  # initialization of the number of approximate occurrences
    pattern_length = len(pattern)

    for index in range(len(genome) - pattern_length + 1):
      # Creates one k-mer of the genome string at the time. 
        k_mer = genome[index : index + pattern_length]

        if check_hamming_distance(pattern, k_mer, maximum_distance):
          # Checks if the distance between the input pattern and the
          # current k-mer is less or equal to the maximum allowed Hamming
          # distance. If this is the case, increases the number of
          # approximate occurrences by one.
            approximate_occurrences += 1

    return approximate_occurrences

def find_recurrent_pattern(pattern_length, genome, maximum_distance, alphabet):

  # Given the pattern length, the genome string, the maximum Hamming
  # distance allowed and the alphabet from which the genome string is 
  # taken, the function selects the pattern that is mostly repeated in
  # the genome string, with up to maximum_distance modification(s).
  # This happens by means of a dictionary having as keys the increasingly 
  # frequent patterns and as values the number of times that the pattern 
  # is present in the genome string, and then selecting the key 
  # corresponding to the higher value.

    dictionary_of_recurrent_patterns = dict()  # initialization of the dictionary
    best_number_of_occurrences = 0  # initialization of the numerical variable that will store the highest number of approximate occurrences

    for pattern in patterns_generator(pattern_length, alphabet):
        number_of_approximate_occurrences = count_approximate_occurrences(pattern, genome, maximum_distance)
        
        if number_of_approximate_occurrences > best_number_of_occurrences:
            dictionary_of_recurrent_patterns[pattern] = number_of_approximate_occurrences
          # Updates the highest number of occurrences whenever the condition (of the if statement) is satisfied.
            best_number_of_occurrences = number_of_approximate_occurrences

  # Gets the key (of dictionary_of_recurrent_patterns) corresponding to the maximum value, i.e. number_of_approximate_occurrences.
    mostly_repeated_pattern = max(dictionary_of_recurrent_patterns, key=dictionary_of_recurrent_patterns.get)
    
    # If you want to visualise how many times the most frequent pattern
    # is present in the genome string, un-comment the following line.
    # print(f'The pattern {mostly_repeated_pattern} is present {dictionary_of_recurrent_patterns[mostly_repeated_pattern]} times.')
    return mostly_repeated_pattern


"""         ------------------------------------------------------         """
# The following section of the code makes it more user-friendly executable,
# since it allows to run the code entirely from the command line by typing
# the name of the input text file right next to the name of the Python file.
# If the input text file is not provided in the command line, 'inputdata.txt'
# is the default value for it.

if __name__ == '__main__':

    if len(sys.argv) != 2:
        pattern_length, maximum_distance, genome = read_instance('inputdata.txt', genomic_alphabet)
    else:
        inputdata = str(sys.argv[1])
        pattern_length, maximum_distance, genome = read_instance(inputdata, genomic_alphabet)
    print(find_recurrent_pattern(pattern_length, genome, maximum_distance, genomic_alphabet))

"""There follow some additional tests I have made:
1)  pattern_length = 7
    maximum_distance = 2
    genome = 'GGTAGTTGGCAGAAAACGGCCTAGTTTATCAGCGGCCGTACAATGACGCTCCGTTACGGCTACGACTCGATCCTGGTGGTTGAGTAACAAACGTTATCGTTAGACGCTGGCGTAGTTGGGTGATAATCAAGCCGTTGATGCTCTCTCGGTGCAACGTGGCGCCCGTCTCACAATTCGACTAAGGATCTTATGTACAATTTCGTAGCGCGGGGTGCCCATGTCGGGAAATGGAAAGCCACCCTTACGATCGGACAGTATTCAAGCAGCGGTGGCTTGTGTAATGATCGTTTTTACGCAGGCGTCATGAGCCGTCAGCATTAAGCTAGTATGCGGACTTCATTGTGCTATGGTCTGAAGTACATACTCGCACGATCTACTGTTGAAGGAGGCGTTGGCTGCGACAAAAAGTAGAGGGAGAAGATGACTAAATTTTGCTGCAACATTTGTTCCCTAACCTTTGCAGGACAGCCTCTAAGGGTGCCTACCACACAGCAACAATGGGGACACGGAGCATCGGTCGCTTGCATCGCAGCGGCCGAGGTGCTAAACAGGTATCAGCATTGCCAGCATGTAGAACACCGGCCGAATTACTAGGTGGTCGGTAATCCTTTCCTACCGGGAAGGGCCAGGGAGCTTTACTCCCCGAAAGTGGTTTGGTACGGACACAATTCATACGGGATAACGAACAGACTCGTGGGGATCCGTAATCTTCCGCCAATACAGCCATTCCCCAGCCGCATGGCGCCCGTGGAGTTCCCGATGTCAAGGGGGGTATTTCCCCGGTTCCTCCGTCGGCAATGAGGACAGGAAGCAACCAACAGCATATGTGTTTCCGACGAACGCCTAAGTATTGTTCAATACGTTCGCCGAAGTTGACCGGGGGGGGAGGGACTTAGGACGCGCATCTACGCAGTACTAGACCATCATAAGGTAGCACGGCGCAAGGTGCACTGGCTGAACGTCTCGCTGTCGAATCTATTCGGATTCTTGTGTGGTCACA'
    mostly_repeated_pattern = 'AGGGGGC'

2)  pattern_length = 6
    maximum_distance = 3
    genome = 'CCTAGCTACCTTGCCCATCACGCCCCGATTGGTCACAAGTCGAGCTTCGCGGTAAGAAGTGCACGACCTAAAGTCAGCTTCGCTTAACGTGACATCACTCAGGGGTTGTCTCAATTCGGCTAGTCTTGTCCGACGCGAAGGTCACCAAGCCCAACCTGAGCCATCTCTGTGTATATGATCCACCTGTCTATAGATCGAGGGGTAGTTTGGGTCTGGAGCTCTACTCCGCTTTAACACCATCTGGCACGCTGCTGTGAGGCTCACGGCTGTCCTTCTTGACTCACTCACCTCTCCACTAGTGAGTTCGATGCAGAGATCCGCGGATCTTTAAGGTTCTCCTGACTCATAGCTGATTGTTGTACTTGCGCCTAGGAGGCCTTAACATGGAGCGATGGATACCACCCCAAATTAGGAAATAAGCGCGCCAAAAATAGGTGAAGGTTTATGCAAGTTGACAACCTCCAAAGTCTTAATTACTCACTTACTAGATCGTTCGCAGGCTGCCGCGTAATGACCCCAGTAGTCACGGCGAGTTAGCATCAGTACGGCCGGTTAAACGTATCAGTCATCCTCGGCAGACCGATTGCAATACTAAACTAAGTACACTATGATGGATTCGATCGCAGTACCAACCGTGTCTTCCCAGGTGTACATTGTATTCATTGTAAGTCAATGATTGTCTATTTAGGAGCCATCCATGCCTTGTTTAGGGGGTTCTCACCTAAGCTCCTGGTGGTTTCCACCTCGCACCCCCGTTGTGACGTAGCTCTCGACGGGAGGTACGCTGACTCGTTTCTCGTGGATCTATTGTCAACGTTTCAGGTCAGGCTTTCGTGACTACAGTGCAACCATCTAGGTGGATGTCTCGACGATAAGATTCCTATAGAGGAGAATCTGCCATTCATATCATCCCTTTTACTAGGAACCAAGAGATTATTACGCTTCCCTGAAGATCTATATAATACGCCTAGTCTCTACAGACTGTTTCATACATACAGAA'
    mostly_repeated_pattern = 'TCTCTC'

3)  pattern_length = 5
    maximum_distance = 3
    genome = 'GGCTATAGTTGGCAGAAATGACGGCCTAGTTTATCAGCGGCCGTACAATGACGCTCCGTTACGGCTACGACTCGATCCTGGTGGTTGAGTAACAAACGTTATCGTTAGACGCTGGCGTAGTTGGGTGATAATCAAGCCGTTGATGCTCTCTCGGTGCAACGTGGCGCCCGTCTCACAATTCGACTAAGGATCTTATGTACAATTTCGTAGCGCGGGGTGCCCATGTCGGGAAATGGAAAGCCACCCTTACGATCGGACAGTATTCAAGCAGCGGTGGCTTGTGTAATGATCGTTTTTACGCAGGCGTCATGAGCCGTCAGCATTAAGCTAGTATGCGGACTTCATTGTCACGTTGCTATGGTCTGAAGTACATACTCGCACGATCTACTGTTGAAGGAGGCGTTGGCTGCGACAAAAAGTAGAGGGAGAAGATGACTAAATTTTGCTGCAACATTTGTTCCCTAACCTTTGCAGGACAGCCTCTAAGGGTGCCTACCACACAGCAACAATGGGGACACGGAGCATCGGTCGCTTGCATCGCAGCGGCCGAGGTGCTAAACAGGTATCAGCATTGCCAGCATGTAGAACACCGGCCGAATTACTAGGTGGTCGGTAATCCTTTCCTACCGGGAAGGGCCAGGGAGCTTTACTCCCCGAAAGTGGTTTGGTACGGACACAATTCATACGGGATAACGAACAGACTCGTGGGGATCCGTAATCTTCCGCCAATACAGCCATTCCCCAGCCGCATGGCGCCCGTGGAGTTCCCGATGTCAAGGGGGGTATTTCCCCGGTTCCTCCGTCGGCAATGAGGACAGGAAGCAACCAACAGCATATGTGTTTCCGACGAACGCCTAAGTATTGTTCAATACGTTCGCCGAAGTTGACCGGGGGGGGAGGGACTTAGGACGCGCATCTACGCAGTACTAGACCATCATAAGGTAGCACGGCGCAAGGTGCACTGAACGTCTCGCTGCCCCCCGATATCTATTCGGACTCTTCTTGTGTGGTCACA'
    mostly_repeated_pattern = 'GCGGG'

4)  pattern_length = 7
    maximum_distance = 3
    genome = 'CCATTGCATTCTCTTCGAAATGCAGAGAAGGCTCTTCTTCCAGGTTTCCATCCTTTTGAGTGGCAACCTCCTTTAAAAAATGTGTCCAGTACAACTGAAGTTGGCATCATTGATGGAATGTCTGGAATGACACAGTTTGTTGATGAATACCCACTAGACACAATTTCAAAAAGATTCAGGTATGATGCAGCTTTGGTTTCAGCCTTAAAGGACCTTGAGGAAGAGTTACTTAAGGGACTGATAGAGGAAGACCTGGAAGACTATCTAAGTGGCCCGTTCACAGTCATAATTAAAGAGTCTTGTGATGGTATGGGAGATGTCAGTGAGAAGCATGGAAGTGGGCCAGCAGTCCCTGAAAAAGCAGTAAGGTATTCTTTTACAATCATGACCATCAGTGTGGCAAACAGTCATAATGAGAATGTAACCATTTTTGAAGAAGGCAAGCCAAACTCAGAGCTGTGTTGCAAGCCCCTATGTCTCATGCTTGCTGACGAATCTGATCATGAGACACTGACTGCCATCTTGGGTCCTGTCATTGCTGAAAGAGAGGCAATGAAAAACAGTGAACTGTTCCTTGAAATGGGGGGAATCCTCAGGTCCTTCAAATTTATCTTCCGAGGCACTGGATATGATGAAAAGCTCATAAGAGATGTTGAAGGTCTCGAGGCTTCAGGTTCAAGTTATATTTGCACCCTCTGTGATTCCACACGCAGTGAAGCTTCACAAAACTTCATTCTTCATTCTATAACGAGGAGTCATAAAGAGAATCTGGAAAGGTATGAAATTTGGAGGTCCAACCCATACCAAGAGCCAGTAGAAGAACTGCGTGACAGAGTTAAGGGGGTTTCAGCCAAACCATTCATTGAAACTCTGCCTTCAATAGATGCCTTACATTGCGATATTGGGAATGCAACTGAGTTCTACAAAATATTCCAAGATGAGATAGGGGAAATTTACAAAAACCCTAACCCTTCCAGAGAAGAAAAAAAGAGATGGCATTCAGTTCTTGATAAACATCTCAGGAAAAATATGAATTTAAAGCCGGTCATGAGAATGAATGGGAATTATGCAAGGAAATTAATGACAAAGGAGACAGTGAATGCAGTATGTGAGTTGATTCCTTCTGAAGAGAGACAGGAAGCCCTCAAGGAACTGGTGGACCTCTATTTGAAAATGAAACCAGTATGGCGTTCCACCTGCCCAGCCAAAGAATGCCCAGAGTTGTTATGCCAATACAGCTTCCACTCTCAACGATTTGCTGAGCTTCTGTCTACAATGTATAGGTATAGATATGAAGGGAAAATCACAAACTATCTTCACAAAACTCTGGCTCATGTTCCAGAAATTATTGAAAGAGATGGCTCCATTGGGGCCTGGGCAAGCGAGGGTAATGAGTCAGGGAACAAACTATTTAGACGCTTCAGAAAAATGAATGCCCGGCAGTCCAAGTATTATGAACTGGAGGATGTCCTA'
    mostly_repeated_pattern = 'AAAGAAA'

5)  pattern_length = 10
    maximum_distance = 2
    genome = 'GGAACAACAAGCCACAGCTTAAAACTCAAAGGACTTGGCGGTGCTTCATACCCCCTAGAGGAGCCTGTTCTAGAACCGATAAACCCCGATCAACCTCAACCACACTTGCTATTTCAGCCTATATACCGCCGTCGCCAGCCCACCCTGTGAAGGAAATACAATGGGCAAAAATAAAAAAATTAAAAACGTCAGGTCGAGGTGTAGCAAATGAGATGGGAAGAAATGGGCTACATTTTCTAAATATAGAATATTACGAAAAAAACAGCGAAACCTGTACTTTGAAGGAGGATTTAGCAGTAAAAGGGGAATAGAGAGCCCCTCT'
    mostly_repeated_pattern = 'AAAAAAAAAA'
"""
