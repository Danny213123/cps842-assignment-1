Objective: The purpose of assignment 1 is to write programs that take a collection of documents and generate its inverted index.

Test collection:

You will use CACM collection (cacm tar file), which is a standard test collection for IR research. It is a collection of titles and abstracts from a journal - Communications of the ACM (CACM), and includes articles published between 1958 and 1979. There are altogether 3204 documents and 10446 terms. The main file you need to use for this assignment is cacm.all which contains the text of documents. You should keep the information from the following fields: .I (for document ID), .T (for title), .W (for abstract), .B (for publication date), and .A (for author list). The terms are extracted from the title and the abstract.

Requirements:

1. You need to write a program invert to do the index construction. The input to the program is the document collection. The output includes two files - a dictionary file and a postings lists file. Each entry in the dictionary should include a term and its document frequency. You should use a proper data structure to build the dictionary (e.g. hashmap or search tree or others). The structure should be easy for random lookup and insertion of new terms. All the terms should be sorted in alphabetical order. Postings list for each term should include postings for all documents the term occurs in (in the order of document ID), and the information saved in a posting includes document ID, term frequency in the document, and positions of all occurrences of the term in the document. There is a one-to-one correspondence between the term in the dictionary file and its postings list in the postings lists file.

2. You should have a component for stop word removal, using the stop word list provided in the CACM collection or a shorter stop word list (stopwords.txt). You should also have a stemming component implemented using Porter's Stemming algorithm or other stemming algorithms. Please make sure these two components can be turned on or off when you run the program.

3. You need to write the second program test to test your inverting program. The inputs to the program are the two files generated from the previous program invert. It then keeps asking user to type in a single term. If the term is in one of the documents in the collection, the program should display the document frequency and all the documents which contain this term, for each document, it should display the document ID, the title, the term frequency, all the positions the term occurs in that document, and a summary of the document highlighting the first occurrence of this term with 10 terms in its context. When user types in the term ZZEND, the program will stop (this requirement is valid only when your program doesn't have a graphical interface). Each time, when user types in a valid term, the program should also output the time from getting the user input to outputting the results. Finally, when the program stops, the average value for above-mentioned time should also be displayed.

4. Write a brief report (one or two pages) to describe the algorithms and data structures you have used for the first program. The report should also include instructions on how to run your programs.

5. You can choose any programming language such as Python, Java, C++, C#, etc.

6. You should submit a zipped file (i.e. cps842f25_a1_yourname.zip) to D2L web site, including the report, the source code of all programs, the executable programs (invert and test) and the result from a few sample runs (could be several screenshots). A demonstration is scheduled during the lab hours (or as you schedule with the TA).

Note: You can write more than two programs and generate more files if necessary.