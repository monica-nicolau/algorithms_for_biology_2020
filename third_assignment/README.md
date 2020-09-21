# Third Assignment - Approximate String Matching - fuzzy string searching

You’re given a long strand of DNA, i.e., a string *s* of *n* characters in the four-letter alphabet **{A, C, T, G}**, and you want to know if there are particular *patterns* that are repeated often in *s*, possibly with small modifications.
  
  
More precisely, you’re given a *pattern length* *m ≤ n* and a *maximum distance* *k*, and you want to know the string *t* of length *m* that is repeated most often in *s*, with up to *k* modifications.
  
  
For **example**, if the strand of DNA is *s* = “GATTACA”, the pattern length is *m* = 3 and the maximum distance is *k* = 1, then the best pattern is *t* = “ATA”, has 3 approximate occurrences, at indices 1 (“ATT”), 1 (“TTA”) and 4 (“ACA”). Note that, paradoxically, in this case, the best pattern does not appear *exactly* anywhere in the strand.


Check if the sys module is installed and now you are ready to run the "third.py" python code!

###### Note that for this assignment, only the Python implementation is requested
