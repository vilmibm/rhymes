import nltk

# Set up NLTK
nltk.download('cmudict')
nltk.download('punkt')

# For getting sentences out of text:
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# For looking up word sounds:
cmudict = nltk.corpus.cmudict.dict()

def get_last_word(sentence):
    """Given a sentence, return its last word, accounting for punctuation."""
    words = sentence.split(' ')
    last_word = words[-1].rstrip() # strip any whitespace at the end
    # Leaving punctuation in will make it impossible to look up words
    for punctuation in ['!', '.', '?']:
        last_word = last_word.replace(punctuation, '')

    return last_word.lower()

def get_rhyme_sound(sentence):
    """Given a sentence, this function returns a string representing the rhyme
    sound of the last word of the sentence. If it can't figure out the sound,
    it returns None."""

    last_word = get_last_word(sentence)

    # Always take the first pronounciation option that cmudict gives. If
    # cmudict cannot find the pronounciation, have us get None back instead.
    phonemes = cmudict.get(last_word, [None])[0]

    # Give up if we found no pronounciation.
    if phonemes is None:
        return None

    # Create the rhyme sound string by combining the last three phonemes of the
    # last word:
    return ''.join(phonemes[-3:])

if __name__ == '__main__':
    # Read our book
    f = open('paradise_lost.txt')
    text = ''.join(f.readlines())
    f.close()

    # Extract sentences
    sentences = tokenizer.tokenize(text)

    # Create a corresponding list of rhyme sounds
    rhyme_sounds = list(map(get_rhyme_sound, sentences))

    couplets = []

    # Now we'll go looking for couplets.
    for counter in range(0, len(rhyme_sounds)):
        # Clean up any new lines still in the original text:
        sentence = sentences[counter].replace('\n', '')

        rhyme_sound = rhyme_sounds[counter]

        if rhyme_sound is not None:
            # enumerate() takes a list and returns a new list of pairs like [0, "a"], [1, "b"]
            # We want all the indices in rhyme_sounds that correspond to the sound
            # we're looking for, except for the index we are currently on.
            indices = [i for i, x in enumerate(rhyme_sounds) if x == rhyme_sound and i != counter]
            for index in indices:
                # Clean up any new lines still in the original text:
                rhyming_sentence = sentences[index].replace('\n', '')

                # Add the sentence we're working on and its rhyme to our list of couplets,
                # but only if the rhyming word is not the same.
                if get_last_word(sentence) != get_last_word(rhyming_sentence):
                    couplets.append([sentence, rhyming_sentence])

    for sentence, rhyming_sentence in couplets:
        print("{}\n\t{}\n".format(sentence, rhyming_sentence))
