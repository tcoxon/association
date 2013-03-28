# The Association Game

The player chooses a word to start the game with, and then the computer and the player take turns to choose a word that relates to the previous one.

An example game might go like this:

    > dog
    # cat
    > fur
    # coat
    > enshroud
    # night
    > moon
    # sun

The game continues until one or the other cannot find an association.

Normally this game is played by two humans, but in this case you can play against Google.

## Usage

Play the game by starting it on the command line like this:

```bash
$ python association.py
```

If 'Failed! Retrying query...' shows up during play, it's best to send the program the interrupt signal (Ctrl-C) and try again in 5-10 minutes. This happens because the game uses the deprecated search API for validating user input. Google limits the number of queries you can make in a certain amount of time for this API.

## Requirements

Python 2.7 and a working Internet connection.

## How it works

### Validating user input

The game checks user input is related to the previous word the computer gave. If it determines the word is unrelated, the game ends. How does it know if two words are related?

User input is validated by querying Google for the number of search results where the two words occur together and comparing this to the result counts where the words appear alone.

In this implementation of the game, given prior word X, the relevancy of word Y is computed as the ratio `f(XY) / min(f(X), f(Y))`, where `f(X)` is the number of search results for query X. A higher ratio means a greater relevance.

Of note in this area is the [Google Similarity Distance (Cilibrasi, Vitanyi, IEEE Transactions on Knowledge and Data Engineering, 2007)](http://arxiv.org/abs/cs.CL/0412098). A partial implementation of this exists in the `google.py` file, but it needs a bit more work before it will function better than the ratio technique (the value of the `N` constant needs tweaking).

### Generating associated words

After user input has been validated, the 'AI' (Google) must choose an associated word or give up.

To generate new words associated to the one the player just chose, the game queries the Google autocomplete API for `"{previous word} and "` and `"{previous word} vs "`. The results for queries like these often provide associated words (but sometimes nonsense).

## See also

* [Google Similarity Distance (Cilibrasi, Vitanyi, IEEE Transactions on Knowledge and Data Engineering, 2007)](http://arxiv.org/abs/cs.CL/0412098)
* [From Conceptual "Mash-ups" to "Bad-ass" Blends: A Robust Computational Model of Conceptual Blending (Veale, ICC2012)](http://computationalcreativity.net/iccc2012/wp-content/uploads/2012/05/001-Veale.pdf)
* [RogueDream](https://github.com/cutgarnetgames/roguedream) - the inspiration for this experiment
