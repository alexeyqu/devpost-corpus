# Devpost corpus
Collecting and analyzing Devpost project descriptions

## About Devpost

Devpost is widely used as a platform for posting descriptions of software projects from various hackathons.
These descriptions contain the actual description and lots of metadata (listed below).

Currently there are about 100k projects and 10% of them won something.

This corpus contains project descriptions and metadata.

## About the corpus

Data is stored in SQLite database (planning to switch to Redis) and is crawled with Scrapy framework. Project descriptions in corpus are splitted by sentences, tokenized and (currently only English descriptions) have POS-tags where appliable ([Penn Treebank POS Tags](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html)), tokenization data is stored in the SQLite database too.

Currently (as of 11 Oct 2018) there are 99665 project pages, 11171 of them are marked as winners.

The corpus contains projects in English (about 80%), Spanish, Arabic, Russian, Chinese and some others (TODO: accurate statistics and mark the entries of each language).

Mean text length: 11 (sentences, [nltk.punkt](https://github.com/mhq/train_punkt)), 235 (words, `nltk.tokenize.RegexTokenizer('\w+')`), 1387 (symbols).

# Metadata

Data | Description | Example
--- | --- | ---
**url** | Url of the project | `https://devpost.com/software/i-scream-you-scream-we-scream`
**title** | Title | `ScreemyBird`
**headline** | Short description of the project  | `A twilio-powered game of flappy bird which you operate by yelling at your phone`
**hackathon** | Hackathon where the project was built | `Anvil Hack 2017`
**text** | Long description of the project | `ShoutyBird We set out to create a multiplayer game system which is . . .`
**builtwith** | List of technologies used to build the projects | `javascript html twilio`
**likes** | Number of likes | `2`
**winner** | If the project won the hackathon | `Winner`

# Collecting and processing

### Crawling

```bash
$ python main.py crawler
```

### Tokenizing and tagging


```bash
$ python main.py tagger
```

# Fun facts

* [Door Hack](https://devpost.com/software/door-prop)
