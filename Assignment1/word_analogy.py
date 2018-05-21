import os
import pickle
import numpy as np
from scipy import spatial


model_path = './models/'
#loss_model = 'cross_entropy'
loss_model = 'nce'

model_filepath = os.path.join(model_path, 'word2vec_%s.model'%(loss_model))

dictionary, steps, embeddings = pickle.load(open(model_filepath, 'r'))

"""
==========================================================================

Write code to evaluate a relation between pairs of words.
You can access your trained model via dictionary and embeddings.
dictionary[word] will give you word_id
and embeddings[word_id] will return the embedding for that word.

word_id = dictionary[word]
v1 = embeddings[word_id]

or simply

v1 = embeddings[dictionary[word_id]]

==========================================================================
"""

#for test
fp = open("word_analogy_test.txt", "r")


#for dev
#fp = open("word_analogy_dev.txt", "r")


if loss_model == 'cross_entropy':
    resultFile = open("word_analogy_test_predictions_cross_entropy.txt","wb")
elif loss_model == 'nce':
    resultFile = open("word_analogy_test_predictions_nce.txt","wb")

for line in fp:
    #print(line.strip())
    lineVal = line.strip()
    wordVal = lineVal.split("||")
    examples = wordVal[0].split(",")
    choices = wordVal[1].split(",")
    #print("examples", examples)
    #print("choices", choices)

    exampleWordList = list()
    exampleDiffList = list()

    for example in examples:
        example = example.replace("\"", "")
        words = example.split(":")
        exampleWordList.append(words)
        #print("words", words)
        v1 = embeddings[dictionary[words[0]]]
        v2 = embeddings[dictionary[words[1]]]

        #print(v2 - v1)
        wordDiff = v2 - v1
        diffList = list()

        for diff in wordDiff:
            diffList.append(diff)
        exampleDiffList.append(diffList)

    #print(len(exampleDiffList))
    exampleDiffArr = np.asarray(exampleDiffList)
    #print(exampleDiffArr)


    choiceWordList = list()
    choiceDiffList = list()

    for choice in choices:
        choice = choice.replace("\"", "")
        chWords = choice.split(":")
        choiceWordList.append(chWords)
        #print("choice", words)
        c1 = embeddings[dictionary[chWords[0]]]
        c2 = embeddings[dictionary[chWords[1]]]

        chWordDiff = c2 - c1
        #print(chWordDiff)
        chDiffList = list()

        for diff in chWordDiff:
            chDiffList.append(diff)

        choiceDiffList.append(chDiffList)

    #print(len(choiceDiffList))
    choiceDiffArr = np.asarray(choiceDiffList)
    #print(choiceWordList)

    sim = 1 - spatial.distance.cdist(exampleDiffArr, choiceDiffArr, 'cosine')

    #print(sim)

    meanVal = np.mean(sim, axis = 1)
    #print(meanVal)
    maxPos = np.argmax(meanVal, axis=0)
    #print(maxPos)
    minPos = np.argmin(meanVal, axis=0)
    #print(minPos)

    ans = ""
    q = ""

    length = len(choiceWordList)

    if((length - 1) > maxPos and (length - 1) > minPos):
        for i in range(len(choiceWordList)):
            #print(choiceWordList[i][0])
            ans += q + "\"" + choiceWordList[i][0] + ":" + choiceWordList[i][1] + "\"" + q + "\t"
        ans += q + "\"" + choiceWordList[minPos][0] + ":" + choiceWordList[minPos][1] + "\"" + q + "\t" + q + "\"" + choiceWordList[maxPos][0] + ":" + choiceWordList[maxPos][1] + "\"" + q + "\n"

        resultFile.write(ans)


print("Prediction file generated.")
resultFile.close()
fp.close()




