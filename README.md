# Deep Learning Fandom Wizard

**This project brings NLP and Deep Leaning to the Fandom community.**

**We want to change how users interact with fandom-related platforms and bring them a personalized experience using the latest AI, while also deepening meaningful interactions between fandom communities.**

## BASE method

Data source: AO3

neural network fundation: 
- word embeddings
  - pre-trained on `conceptNet numberbatch` (https://github.com/commonsense/conceptnet-numberbatch)
  - contextual embeddings in the future
- RNN for sentiment analysis?
- MLP: a simpler solution for now

## Feature: Fanfiction Digestion

- First step: fanfiction classifying
  - ratings/fandoms/tags prediction (with MLP)
  - sentiment classifying

- Writing styles
  - Is the vocabulary rich? Would it be considered "well-written" in a common sense? What is the literature value?
  - what makes a fanfiction good (e.g. receive a lot of kudos)? is there lietrature evidance we can find?
  - author identification (can we recognize the writing styles of some of the prolific authors in the community?)
 
- Recommend similar content
  - finding out similar fanfictions in terms of sentiment/writing styles/vocabulary usage/fandoms
  - in the future, we will also add *user-user* and *user-item* recommendation system

- Compile music playlist
  - Give us a fanfic, we will compile a Spotify playlist, with Lyrics and Audio both match the fanfics
  - Are there artists that specifically macth a fandom (e.g. Glass Animals for mcyt)
  - Demo (live version): https://fanfic-playlist.herokuapp.com/

## Analysis

- Differences between fanfics from different fandoms? Differences between pairings?
- Sexual content is prevailing, what information can we extract from it?
- `Fluff/Angst/Smut` are some traditional tags people use, can we make any other archtypes that offer more varieties? 

## What do we need from the community?

1. Provide us with more data (fill out these Google forms we have)!
 - link to Google form:
2. Provide feedbacks on our beta website!
 - TODO: need feedback button (need a twitter account)
3. Suggest more features!
 - link to Google form:

*Next step:*

1. More data
2. More labaled data
3. Front-end
4. More feature/use-case discoveries
