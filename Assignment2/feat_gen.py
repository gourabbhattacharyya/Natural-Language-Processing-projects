#!/bin/python
import sys
from num2words import num2words


def preprocess_corpus(train_sents):
    """Use the sentences to do whatever preprocessing you think is suitable,
    such as counts, keeping track of rare features/words to remove, matches to lexicons,
    loading files, and so on. Avoid doing any of this in token2features, since
    that will be called on every token of every sentence.

    Of course, this is an optional function.

    Note that you can also call token2features here to aggregate feature counts, etc.
    """

    for sent in train_sents:
        for i in xrange(len(sent)):
            sent[i] = sent[i].strip()


        for i in xrange(len(sent)):
            sent[i] = sent[i].replace("\t", " ")

        '''
        for i in xrange(len(sent)):

            if "http://" in sent[i]:
                sent[i] = sent[i].replace("http://", "URL:")
            if "https://" in sent[i]:
                sent[i] = sent[i].replace("https://", "URL:")
            if "HTTP://" in sent[i]:
                sent[i] = sent[i].replace("HTTP://", "URL:")
            if "HTTPS://" in sent[i]:
                sent[i] = sent[i].replace("HTTPS://", "URL:")
        '''
        #print(sent)

    #pass

def token2features(sent, i, add_neighs = True):
    """Compute the features of a token.

    All the features are boolean, i.e. they appear or they do not. For the token,
    you have to return a set of strings that represent the features that *fire*
    for the token. See the code below.

    The token is at position i, and the rest of the sentence is provided as well.
    Try to make this efficient, since it is called on every token.

    One thing to note is that it is only called once per token, i.e. we do not call
    this function in the inner loops of training. So if your training is slow, it's
    not because of how long it's taking to run this code. That said, if your number
    of features is quite large, that will cause slowdowns for sure.

    add_neighs is a parameter that allows us to use this function itself in order to
    recursively add the same features, as computed for the neighbors. Of course, we do
    not want to recurse on the neighbors again, and then it is set to False (see code).
    """


    ftrs = []
    # bias
    ftrs.append("BIAS")
    # position features
    if i == 0:
        ftrs.append("SENT_BEGIN")
    if i == len(sent)-1:
        ftrs.append("SENT_END")

    # the word itself
    word = unicode(sent[i])
    ftrs.append("WORD=" + word)
    ftrs.append("LCASE=" + word.lower())
    # some features of the word
    if word.isalnum():
        ftrs.append("IS_ALNUM")
    if word.isnumeric():
        ftrs.append("IS_NUMERIC")
    if word.isdigit():
        ftrs.append("IS_DIGIT")
    if word.isupper():
        ftrs.append("IS_UPPER")
    if word.islower():
        ftrs.append("IS_LOWER")




    # more added features

    # is Emoji
    emoji = {
        "&lt;3": "positive", ":D": "positive", ":d": "positive", ":dd": "positive", ":P": "positive",
        ":p": "positive",
        "8)": "positive",
        "8-)": "positive", ":-)": "positive", ":)": "positive", ";)": "positive", "(-:": "positive",
        "(:": "positive",
        ":')": "positive", "xD": "positive", "XD": "positive", "yay!": "positive", "yay": "positive",
        "yaay": "positive",
        "yaaay": "positive", "yaaaay": "positive", "yaaaaay": "positive", "Yay!": "positive",
        "Yay": "positive",
        "Yaay": "positive",
        "Yaaay": "positive", "Yaaaay": "positive", "Yaaaaay": "positive", ":/": "negative",
        "&gt;": "negative",
        ":'(": "negative",
        ":-(": "negative", ":(": "negative", ":s": "negative", ":-s": "negative", "-_-": "negative",
        "-.-": "negative"}

    isPresent = "IS_NOT_EMOJI"
    if word.split(" ")[0] in emoji:
        isPresent = "IS_EMOJI"
    ftrs.append(isPresent)

    # is HashTag
    if word.startswith("#"):
        ftrs.append("IS_HASHTAG" if len(word[1:]) != 0 else "IS_NOT_HASHTAG")

    # is URL
    if word.startswith("http://"):
        ftrs.append("IS_URL" if len(word[8:]) != 0 else "IS_NOT_URL")


    # is Header
    if word.startswith("@"):
        ftrs.append("IS_HEADER" if len(word[1:]) != 0 else "IS_NOT_HEADER")




    # has Exclamaton
    if "!" in word:
        ftrs.append("HAS_EXCLAIMATION")


    # has Question
    if "?" in word:
        ftrs.append("HAS_QUESTION")



    # ends with ed
    if word.split(" ")[0].endswith("ed"):
        ftrs.append("ED_ENDED")

    # ends with ing
    if word.split(" ")[0].endswith("ing"):
        ftrs.append("ING_ENDED")



    # POS count
    if posCount(word, sent) > 0:
        ftrs.append("HAS " + num2words(posCount(word, sent)).upper() + " COUNT")


    # avg length
    ftrs.append("HAS " + getLen(word, sent).upper() + " LENGTH")


    # word length
    ftrs.append("HAS LENGTH " + str(len(word) - 1) + " WORD")


    # POS index
    # print(posIndex(word, sent).upper())
    if posIndex(word, sent) > 0:
        ftrs.append("HAS " + num2words(posIndex(word, sent)).upper() + " INDEX")


    # byte length
    ftrs.append("HAS WORD " + num2words(sys.getsizeof(word)).upper() + " BYTELENGTH")

    # HASH length
    ftrs.append("HAS HASH_" + str(hash(word.split(" ")[0])) + "_LENGTH")

    # done adding features


    # previous/next word feats
    if add_neighs:
        if i > 0:
            for pf in token2features(sent, i-1, add_neighs = False):
                ftrs.append("PREV_" + pf)
        if i < len(sent)-1:
            for pf in token2features(sent, i+1, add_neighs = False):
                ftrs.append("NEXT_" + pf)




    return ftrs



def posCount(word, sent):
    count = 0
    values = word.split(" ")

    if len(values) > 1:
        matchWord = word.split(" ")[1]

        for i in xrange(len(sent)):
            if matchWord in sent[i]:
                count += 1

        return count

    return len(values)




def charCount(word, sent, c):
    count = 0
    values = word.split(" ")

    if len(values) > 1:
        for i in xrange(len(sent)):
                count += sent[i].count(c)

    return count




def posIndex(word, sent):
    index = 0
    values = word.split(" ")

    if len(values) > 1:
        matchWord = word.split(" ")[1]
        s = ""
        for i in xrange(len(sent)):
            s += " " + sent[i]

        #print s
        index = s.rfind(matchWord, 0, len(sent))
        return index

    return index



def getLen(word, sent):
    totalLen = 0

    for i in xrange(len(sent)):
        if word not in sent[i]:
            totalLen = len(sent[i]) - 1

    wordLen = round(totalLen * 1.0/len(word),2)
    wordLen = int(wordLen)

    return num2words(wordLen)



if __name__ == "__main__":
    sents = [
    [ "@LogUpdate",
    "What	NOUN",
"a	DET",
"productive	ADJ",
"day:D	NOUN",
":D	ADJ",
"Enjoyed	VERB",
"Walking	VERB",
"around	DET",
"Beach!!!	ADJ",
"http://beachPhotos.com	X",
"#FunUnlimited	ADJ"]
    ]
    preprocess_corpus(sents)
    for sent in sents:
        for i in xrange(len(sent)):
            print sent[i], ":", token2features(sent, i)
