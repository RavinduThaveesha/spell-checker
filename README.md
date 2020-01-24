# spell-checker
This class can detect incorrectly spelled words and suggest fixes.

It takes a given text string and checks its words against a dictionary of words known to be valid to determine if they are correct.

For words that seem to be incorrect, it suggest words that are similar and seem to be correct versions of those words.

This is a part of post graduate module project and bigram,unigram,dictionary lookup and probability techniques used to develop this class. 

## Process

![Image of Process](https://user-images.githubusercontent.com/5220867/73066472-0e7f2a00-3ee1-11ea-8fa6-e8b222868b1b.png)

## How to use

Initialize SpellChecker class and call check method and provide text you want to check.

```
spellChecker = SpellChecker()
w = spellChecker.check('I am ol')
print('1 %s' % w)
```

## Real world implementation

Final solution develiered as a web app using django.

![Image of Screenshot](https://user-images.githubusercontent.com/5220867/73066475-0f17c080-3ee1-11ea-812b-49f49132ffab.png)


PHP non word error impletation of this class can be found here: https://www.phpclasses.org/package/11420-PHP-Detect-incorrectly-spelled-words-and-suggest-fixes.html




