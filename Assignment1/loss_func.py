import tensorflow as tf
import numpy as np

def cross_entropy_loss(inputs, true_w):

    """
    ==========================================================================

    inputs: The embeddings for context words. Dimension is [batch_size, embedding_size].
    true_w: The embeddings for predicting words. Dimension of true_w is [batch_size, embedding_size].

    Write the code that calculate A = log(exp({u_o}^T v_c))

    A =


    And write the code that calculate B = log(\sum{exp({u_w}^T v_c)})


    B =

    ==========================================================================
    """

    A = tf.matmul(inputs, tf.transpose(true_w))
    print("diag elem", tf.diag_part(A))
    A = tf.diag_part(A)
    A = tf.cast(A, tf.float32)
    A = tf.exp(A)
    A = tf.log(A)
    print("A", A)



    B = tf.matmul(true_w, tf.transpose(inputs))
    print("B", B)
    B = tf.cast(B, tf.float32)
    B = tf.exp(B)
    B = tf.reduce_sum(B, 1, keep_dims=True)
    B = tf.log(B)
    print("B", B)

    print("tf.subtract(B, A)", tf.subtract(B, A))

    return tf.subtract(B, A)



def nce_loss(inputs, weights, biases, labels, sample, unigram_prob):
    """
    ==========================================================================

    inputs: Embeddings for context words. Dimension is [batch_size, embedding_size].
    weigths: Weights for nce loss. Dimension is [Vocabulary, embeeding_size].
    biases: Biases for nce loss. Dimension is [Vocabulary, 1].
    labels: Word_ids for predicting words. Dimesion is [batch_size, 1].
    samples: Word_ids for negative samples. Dimension is [num_sampled].
    unigram_prob: Unigram probability. Dimesion is [Vocabulary].

    Implement Noise Contrastive Estimation Loss Here

    ==========================================================================
    """
    k = len(sample)

    weights_o = tf.nn.embedding_lookup(weights, labels)
    weights_o = tf.reshape(weights_o, [-1, labels.shape[0]])
    print("weights_o", weights_o, labels.shape[0])

    biases_o = tf.nn.embedding_lookup(biases, labels)
    biases_o = tf.reshape(biases_o, [-1, labels.shape[1]])
    print("biases_o", biases_o)

    unigram_prob_o = tf.gather(unigram_prob, labels)
    unigram_prob_o = tf.reshape(unigram_prob_o, [-1, labels.shape[1]])
    print("unigram_prob_o", unigram_prob_o)


    s_o = tf.matmul(inputs, tf.transpose(weights_o))
    s_o = tf.add(s_o, biases_o)
    print("s_o", s_o)

    prob_o = tf.scalar_mul(k, unigram_prob_o)
    prob_o = tf.log(prob_o)
    print("prob_o", prob_o)

    z_o = tf.subtract(s_o, prob_o)
    z_o = tf.cast(z_o, tf.float64)
    print("z_o", z_o)

    sigma_o = tf.sigmoid(z_o)
    print("sigma_o", sigma_o)

    #sigma_o = tf.add(tf.cast(1e-24, tf.float64), sigma_o)
    sigma_o = tf.log(sigma_o)
    print("sigma_o", sigma_o)








    '''
    weights_x = tf.gather(weights, sample)
    print("weights", weights_x)

    biases_x = tf.gather(biases, sample)
    print("biases_x", biases_x)

    unigram_prob_x = tf.gather(unigram_prob, sample)
    print("unigram_prob_x", unigram_prob_x)
    '''


    weights_x = tf.nn.embedding_lookup(weights, sample)
    weights_x = tf.reshape(weights_x, [-1, k])
    weights_x = tf.transpose(weights_x)
    print("weights_x", weights_x)

    biases_x = tf.nn.embedding_lookup(biases, sample)
    biases_x = tf.reshape(biases_x, [-1, k])
    print("biases_x", biases_x)

    unigram_prob_x = tf.gather(unigram_prob, sample)
    print("unigram_prob_x", unigram_prob_x)


    s_x = tf.matmul(inputs, tf.transpose(weights_x))
    s_x = tf.add(s_x, biases_x)
    print("s_x", s_x)

    prob_x = tf.scalar_mul(k, unigram_prob_x)
    prob_x = tf.log(prob_x)
    print("prob_x", prob_x)

    z_x = tf.subtract(s_x, prob_x)
    z_x = tf.cast(z_x, tf.float64)
    print("z_x", z_x)

    sigma_x = tf.sigmoid(z_x)
    print("sigma_x_1", sigma_x)

    sigma_x = tf.subtract(tf.cast(1.0, tf.float64), sigma_x)
    #sigma_x = tf.add(tf.cast(1e-24, tf.float64), sigma_x)
    sigma_x = tf.reduce_sum(tf.log(sigma_x), 1, keep_dims=True)
    print("sigma_x_updated", sigma_x)





    cost_o = tf.add(sigma_o, sigma_x)
    cost = tf.negative(cost_o)
    print("cost", cost)


    return cost
