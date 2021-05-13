
**A recap of the old method**:

Word Embeddings
1. get static word embeddings from ConcetNet Numberbatch (dimension = 300) (the current best performing static word embeddings)
2. intersect Numberbatch with vocabularies from fanfic corpus, expand the word embeddings size
3. Re-train a CBOW model on fanfic corpus with expanded word embeddings
4. get new static word embeddings that has embedded fanfic specific vocabularies (character names, etc.)

Doc2Vec
1. Do a mean-pooling: for each document $d_i$ with $n$ tokens, for each token $t$ in that document, get its word embedding vector $w_{t}$. The document embedding is expressed as
$$
Emb(d_i) = \frac{1}{n} \sum_{k=1}^{n} w_{t_k}
$$

Classifiers
1. In the old method, the class set $C$ is ``{'romantic', 'sexual', 'sad'}``. For each class $c_j$ in class set $C$, the class value could either be 1 or 0 (1 means it belongs to the class, 0 otherwise).
2. Then for each document $d_i$, assign it a binary label $l_{i,j} (i \in |d|, j \in |C|)$ for each class $c_j$
  - *this labeling is done semi-manually. We pre-define a set of tags $T_{c_j}$ that "represent" this class $c$, then $l_{i,j}$ is 1 if $tags(d_i)$ intersect with $T_{c_j}$ (along with some pre-defined rule $P_{c_j}$), otherwise 0.*
3. For each class $c$, build a binary classifer using a feedforward Neutral Network (MLP) with hidden size 100, call it $MLP_c$. $MLP_c$ takes in document embeddings as input and output the $softmax$ layer (with dimension 2).
4. Use this $softmax$ layer (class probability) as the score of $d_i$ for class $c_j$. The total score of $d_i$, $s_i$, is represented as a vector of its concatenated scores (dimension = $|C| * 2$).

Similarity Ranking
1.  For word embeddings match, compare cosine similarity of $Emb(d_i)$ witch each pair of $i \in |D|$. For "class" match, compare cosine similarity of $s_i$.

**A bit reflection:**

What went well
1. Static word embeddings are surprisingly accurate. Preprocessing and training does not even require GPU (but does need lots of RAM without chunking)
2. Given the architecture of the MLPs are very simple (without dropout, without activation functions, only one hidden layer, almost no tuning), and the data is clumsily labeld (semi-manual, largely depends on user's tags), the accuracy of the MLP is pretty good.
3. Speed and simplicity. No NN model involved in vetorizing documents once the word embeddings are trained and stored.

What could be imporved (what is a bit scatchy)
1. Basically a fancier version of BOW. No continuous relationship is captured between words, sentences and paragraphs. For example, a story that went "sad->happy ending" could be the same as a story that went "happy->sad ending".
2. This way of labaling data restricts the class size and is not a scalable solution in the long run. Frankly, the current set $C$ already contains all the "easy" predictions. To add on it, for exmaple, adding "violent" or "dark", would be difficulty, because these features are not well-labeled by the users.

**BERT** (as the next step base model)

Pros
1. Generally speaking it's more accurate, contextual embedding. Out-perform static embeddings on many tasks
2. Many resources and research available online and free (Huggingface)
3. Many possibilities

Cons
1. Training time and cost. Not possible to train new word embeddings from scratch, meaning no custom vocabulary.
2. Other than that, even fine tuning it will probably cost a lot of time (imagine all the back-prop it needs to go through lol). Plus, we hardly have any labeled data to fine-tune it with. The most realistic/easy way is to only use it as a service.
3. High dimension (768), PCA to 300 will drag down the accuracy
4. Better suited for sentence analysis, not long document (?)

