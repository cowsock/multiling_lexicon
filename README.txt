=======Generating German sentiment lexicon via random walk model=========

 Dependencies: 
 -------------

 python 2.7.12 

 Wordnet (here, interfaced via NLTK)
 
 GermaNet

 An English sentiment lexicon (positive, negative)

 A German-English dictionary file

 A German sentiment lexicon (for evaluation)



 Modules:
 --------

MakeEngWordnet.py  -->
        Interfaces with Wordnet via NLTK and builds a list of edges
        suitable for the network needed in the Main module. 
        Extracts word pairs that occur in synsets, words with 
        hypernym relations and words with similar-to relations.

        output: eng_wordnet.txt

Main.py  -->

    depends on: WordnetParser.py, DictParser.py, Util.py

        Main module. Requires that all resources are present. No
        command-line arguments required


        output: out.txt (list of German-word, sentiment label pairs)

Evaluation.py  -->

    depends on: Util.py, German sentiment lexicon

        Command-line argument: output file produced by Main.py.



Other Files:
------------

WordnetParser.py  -->
    
    depends on: English wordnet edges file (obtained by MakeEngWordnet),
                German wordnet file

        loads each resource into a dictionary
        

DictParser.py  -->

    depends on: German-English dictionary 

        loads resource into a dictionary structure

Util.py  -->

        Defines Vertex type used in most code relating to network structure.

        Defines POS notatation-conversion function.

