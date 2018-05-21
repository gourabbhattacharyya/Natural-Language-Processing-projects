import numpy as np

def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):
    """Run the Viterbi algorithm.

    N - number of tokens (length of sentence)
    L - number of labels

    As an input, you are given:
    - Emission scores, as an NxL array
    - Transition scores (Yp -> Yc), as an LxL array
    - Start transition scores (S -> Y), as an Lx1 array
    - End transition scores (Y -> E), as an Lx1 array

    You have to return a tuple (s,y), where:
    - s is the score of the best sequence
    - y is the size N array/seq of integers representing the best sequence.
    """
    L = start_scores.shape[0]
    assert end_scores.shape[0] == L
    assert trans_scores.shape[0] == L
    assert trans_scores.shape[1] == L
    assert emission_scores.shape[1] == L
    N = emission_scores.shape[0]


    scores = np.zeros_like(emission_scores)
    back_pointers = np.zeros_like(emission_scores, dtype=np.int32)

    emission_scores += start_scores
    trans_scores += start_scores

    scores[0] = emission_scores[0] + start_scores

    # Generate most likely scores and paths for each step in sequence
    for i in range(1, N):
        score_with_transition = np.expand_dims(scores[i-1], 1) + trans_scores
        scores[i] = emission_scores[i] + np.max(score_with_transition, 0)
        back_pointers[i] = np.argmax(score_with_transition, 0)



    # Generate the most likely path
    viterbi = [np.argmax(scores[-1] + end_scores)]
    for bp in reversed(back_pointers[1:]):
        viterbi.append(bp[viterbi[-1]])


    viterbi.reverse()
    viterbi_score = np.max(scores[-1] + end_scores)

    return viterbi_score, viterbi
