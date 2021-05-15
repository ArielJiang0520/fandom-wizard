## ⚙️ Backend ⚙️

### 🧙Feature Requirements

Basically a AI-powered search engine. Google + Pinterest for fandoms

- natural language query -> find relevant fanfic in the database
- fanfic similarity ranking
- fanfic [keywords/tags/or smth else?] extraction

(All of these is one single system, aka the fanfic language model?)

**📖information representation**

what info do we have?
- corpus
- title & author
- rating (PG-13, etc.) + warnings
- fandom
  - this can derive to the social sentiment/trending discussion around this fandom
  - the original genre/synopsis of this fandom?
  - IMDB data can be easily obtained. They are surprisingly up-to-date as well
- tags
  - not reliable because user-generated
  - many mislabelings and over-exaggerations
- pairing (M/M, F/F, etc.)
- relationships (e.g. Dream X George)
- kudos/hits/comments
- summary

**😬challenges**

- **unlabeled data**: is it really a challenge? frankly, this is what our entire project is built around -- labeling fanfics in our own way. Even more, it might be a *leverage* we can use to build the best available system and prove our tech novelty.
  - Many algorithms available for **unsupuervised learning** -- self-learning, semi-supervised, etc.
  - What about **topic modeling** (LDA)?
  - What exactly is it that we are trying to label? Do we just want grouping (clustering) instead? Would that be too hard? (not enough evidence)
- **feature extraction**: what is it that you want to extract from a fanfic? We already have the matadata (fandoms/tags/pairings etc.), so we are trying to extract underlying features from the **text**. What could **text** tell you that matadata can not?

**❓❓❓questions to ask anyone❓❓❓**

(the problem ultimately needs social opinons to solve; in this space, let's not care about technical feasibility)

Recall your favorite fanfic (a fanfic/book you finished reading and couldn't get enough of it), you probably want to read something similar to it, right? What are you looking for?
  - well, most people read a fanfic in the first place because of the pairing/fandom. but if they just want same **pairing/fandom**, they could just do a AO3 search. so what could our app provides that AO3/normal search engine can not
  - Personally, I want to see a fanfic with similar writing styles. Okay, what do you mean by "writing style"?
    1. The use of **vocabulary** (rare words v.s. common words)
      - more in `rare words explore.ipynb` in this directory
      - what I've learned in general is that it's a useful measurement and could potentially increase the accuracy. Also, static embeddings seem to capture it more than BERT. It's probably because static embeddings have been trained on the corpus itself
      - BERT seems like it's better for capturing the theme/subtle tone of the story. For example, if a fanfic is sexual, but it also focuses a lot on degrading the other person, then BERT can capture that
    2. **Narration styles** (both fanfics can be good, but they could be presented with very different styles)
      - in classic literature, this difference can be observed through authors from different eras
      - a story can be heavily narrated (3rd person POV, many adjectives using to describe the scene, backgroudn, etc.) v.s. a story can be expressive, or conscious stream, or abstract
    3. Theme & plot. Obviously exact plot match is not possible, but can we capture the **progression of the story**, or the themes? (slow burn, friends to lovers, rough start but happy ending, enemies to lovers, etc.)
      - progression information needs sequential model to encode
      - could this be done via applying skewed weights (like a *gamma distribution* skewed left since most important part of the story is normally at the end?) to the sentences of the document and then do a weighted average?
      - this distribution could be also learned via training (just like attention weights), but what's the objective function for this training?
      - another way to do this is to *concatenate* the hidden vectors instead of averaging them. To avoid this vector becoming too long (most fanfics will have > 150 sentences), we can divide the story to 3 equal parts, averaging the vectors of these parts and then concate them to a vector of size `3 X hid_dim`
    4. **mood/tone**. This is very vague, and can also be tied back to "themes". But I'm more thinking of like overall "sad", "light-hearted", "heavy", "serious", "humorous", etc.
      - this is a sentiment classification problem, but our data is only "weakly labeled". I did a MLP going from input size (BERT `hid_dim`) to class size (restricted to top ~50 tags), getting the `softmax` layer as a vector representation of the doc. The accuracy is okay if you just want to predict the tag of the fanfic, but for some reason it doesn't add much to the word embeddings similarity score
      - adding `class_weights` in the classifier help with clearing the noise (too many fanfics being marked as `angst`)
      - in fact having three fixed categories `{romance, sexual, sad}` somehow performs better in terms of understanding the overall tone of a fanfic -- because when you think of it, the AO3 tags themselves are not pretty good indicator of the story
    5. other **matadata**, for example, is it about sex (R-18) or not? is it F/F or M/M or F/M? What's the general story setting (mordern, historical era, sci-fi, etc.)
    6. **fandom** similarity, for example, "Marvel Universe" readers are probably more likely to want to read something US cinema/superhero related? at least you wouldn't recommend anime for them, right?

**🙅‍♀️Error Analysis🙅‍♀️**

(These are some pretty difficulty/confusing cases that the model can get wrong)

1. (1) A dark, sexual, sadistic work with no romance involved v.s. (2) kinky, role-playing sex between couples
  - both can get pretty violent (have dirty talk, dom/sub dynamics, etc)
  - the difference is that somewhere in the (2) story, the two characters probably will kiss/confess love/back to normal etc.
  - BERT somehow can not capture this if the "romance" part in (2) is too subtle/short, but static embeddings seem like it might be able to (idk why, maybe because static embeddings focus single words like "kiss" etc.)
  - example: [(1)](https://archiveofourown.org/works/30843302) [(2)](https://archiveofourown.org/works/29860926)
  - in this case, (1) should be better match with [(3)](https://archiveofourown.org/works/21908) or [(4)](https://archiveofourown.org/works/30616133).
  - what could help: BOW

2. (1) A writer who has actual good writing skill e.i. using the right word at the right time v.s. (2) someone who just puts in rare words for the sake of it
  - an example of [(2)](https://archiveofourown.org/works/30469629). The usage of words is more complicated than literature pieces like "Ulysses" or "Moby Dick", but it's definitely not as well-written.