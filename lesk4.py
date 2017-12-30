from nltk.corpus import wordnet
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
import sys

stop_words = set(line.strip() for line in open('stopwords.txt'))

def simplified_lesk( word, sentence ):
    final = None
    maxoverlap = 0
    word=wordnet.morphy(word)

    print("Total senses are")
    print("------------------------")
    for sense in wordnet.synsets(word):
        print sense
        overlap = overlap_func(sense,sentence)
        for hyponyms in sense.hyponyms():
            overlap += overlap_func( hyponyms, sentence )

        if overlap > maxoverlap:
                maxoverlap = overlap
                final = sense
        print overlap
    print ("--------------------------------")
    print("\nFinal Chosen Sense")
    return final

def overlap_func( synset, sentence ):
    x=synset.definition()
    gloss = set(tokenizer.tokenize(x))
    for example in synset.examples():
         gloss=gloss.union(example)
    gloss = gloss.difference( stop_words )

    sentence = set(sentence.split(" "))
    sentence = sentence.difference( stop_words )
    gloss=gloss.intersection(sentence)
    return len( gloss )

def main():
    sentence = raw_input("Enter the Sentence :")
    word = raw_input("Enter the word :")

    lesk = simplified_lesk(word,sentence)
    print (lesk)
    if lesk is not None:
        print "Definition: ",lesk.definition()
        example=0
        print "\nExamples:"
        for i in lesk.examples():
            example=example+1
            print str(example)+'.',i

if __name__=='__main__':
    main()