## ⚙️ Backend ⚙️

### 🧙Feature Requirements

- natural language query -> search for fanfic in the database
- fanfic similarity ranking
  - this includes many subtle things, like what do you use to rank?
- fanfic [keywords/tags/or smth else?] extraction

(All of these is one single system, aka the fanfic language model?)

**📖information representation**

what info do we have?
- corpus
- title
- rating (PG-13, etc.) + warnings
- fandom
  - this can derive to the social sentiment/trending discussion around this fandom
  - the original genre/synopsis of this fandom?
- tags
  - not reliable because user-generated
  - many mislabelings and over-exaggerations
- pairing (M/M, F/F, etc.)

- *we do not have author information/ we do not have exact pairing information*


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
    2. Writing skill, **grammar** (complicated, polished grammar v.s. normal grammer, even with some wrong grammar)
    3. **Narration styles** (both fanfics can be good, but they could be presented with very different styles)
      - in classic literature, this difference be observed through authors from different eras
    4. Theme & plot. Obviously exact plot match is not possible, but can we capture the **progression of the story**, or the themes? (slow burn, friends to lovers, rough start but happy ending, enemies to lovers, etc.)
      - progression information needs sequential model to encode
    5. **mood/tone**. This is very vague, and can also be tied back to "themes". But I'm more thinking of like overall "sad", "light-hearted", "heavy", "serious", "humorous", etc.
    6. other **matadata**, for example, is it about sex (R-18) or not? is it F/F or M/M or F/M? What's the general story setting (mordern, historical era, sci-fi, etc.)


