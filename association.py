
import random
import google


_QUERIES = [
    '{word} vs ',
    '{word} and ',
]

def choose_next_word(prev_word):
    words = []
    for q in _QUERIES:
        q = q.format(word=prev_word)
        words.extend([x[len(q):].strip()
            for x in google.autocomplete(q)[:5]])
    if len(words) == 0:
        return None
    return random.choice(words)


_RELEVANCY_THRESHOLD = 0.05

def main():
    player_word = None
    npc_word = None
    print 'You start:'
    try:
        while True:

            player_word = raw_input('> ')

            if npc_word is not None:
                if (google.relevancy(npc_word, player_word) <
                        _RELEVANCY_THRESHOLD):
                    print 'Unrelated word!'
                    break

            print '#',
            npc_word = choose_next_word(player_word)
            if npc_word is None:
                print 'I give up!'
                break
            print npc_word

    except EOFError:
        print
        print 'Bye!'


if __name__ == '__main__':
    main()
