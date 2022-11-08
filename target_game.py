'''target eng game'''
from typing import List
import random
import sys
import string

def letter(word):
    '''
    list -> set

    Creates a set of existing letters in a word'''
    res = []
    ablen = len(word)
    for i in range(0, ablen):
        count = 1
        for j in range(0, ablen):
            if i != j:
                if word[i] == word[j]:
                    count += 1
                let = (word[i], count)
                res.append(let)
        let = (word[i], count)
        res.append(let)
    res = [*set(res)]
    return set(res)

def validate_words(words, letters):
    '''
    (list, list) -> list

    Check or words fall under the rules
    >>> validate_words(['aide', 'idea', 'kike', 'kioea', 'koae', 'wake', 'weak', 'weki', \
'wife', 'wode'], ['a', 'd', 'e', 'i', 'w', 'f', 'k', 'i'])
    ['wake', 'weak', 'weki', 'wife']
    >>> validate_words(['aide', 'idea', 'kike', 'kioea', 'koae', 'wake', 'weak', 'weki', \
'wife', 'wode'], ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'])
    []'''
    wordslen = len(words)
    res = []
    letterset = letter(letters)
    for i in range(0, wordslen):
        if len(words[i]) >= 4 and letters[4] in words[i]:
            wordset = letter(words[i])
            if wordset.issubset(letterset):
                res.append(words[i])
    return res

def generate_grid() -> List[List[str]]:
    """
    Generates list of lists of letters - i.e. grid for the game.
    e.g. [['I', 'G', 'E'], ['P', 'I', 'S'], ['W', 'M', 'G']]
    """
    letlist = []
    letters = string.ascii_letters
    for _ in range(9):
        let = random.choice(letters)
        let = let.lower()
        letlist.append(let)
    return letlist

def get_words(openfile: str, letters: List[str]) -> List[str]:
    """
    Reads the file f. Checks the words with rules and returns a list of words.
    """
    with open(openfile, 'r', encoding='UTF-8') as file:
        file.readline()
        file.readline()
        file.readline()
        words = file.readlines()
    words = [word.strip() for word in words]
    res = validate_words(words, letters)
    return res

def get_user_words() -> List[str]:
    """
    Gets words from user input and returns a list with these words.
    Usage: enter a word or press ctrl+d to finish for *nix or Ctrl-Z+Enter
    for Windows.
    Note: the user presses the enter key after entering each word.
    """
    user = sys.stdin.read()
    lst = user.split('\n')
    lstlen = len(lst)
    for i in range(0, lstlen):
        lst[i] = lst[i].lower()
        lst[i] = lst[i].replace('\x1a', '')
    lst = list(set(lst))
    lst.remove('')
    return lst

def get_pure_user_words(user_words: List[str], lttrs: List[str], dictwords: List[str]) -> List[str]:
    """
    (list, list, list) -> list

    Checks user words with the rules and returns list of those words
    that are not in dictionary.

    """
    userwords = validate_words(user_words, lttrs)
    userwordslen = len(userwords)
    res = []
    for i in range(0, userwordslen):
        if userwords[i] not in dictwords:
            res.append(userwords[i])
    return res

def samewords(userwords, tablewords):
    '''
    (list, list) -> list

    Check if the words entered by the user are in the dictionary
    >>> samewords(['idea', 'kike','weak', 'wife', 'wode'], ['aide', 'idea', 'kike', 'kioea', \
'koae', 'wake', 'weak', 'weki', 'wife', 'wode'])
    ['idea', 'kike', 'weak', 'wife', 'wode']
    >>> samewords(['idea', 'keki','waek', 'wife', 'edow'], ['aide', 'idea', 'kike', 'kioea', \
'koae', 'wake', 'weak', 'weki', 'wife', 'wode'])
    ['idea', 'wife']
    '''
    userwordslen = len(userwords)
    res = []
    for i in range(0, userwordslen):
        if userwords[i] in tablewords:
            res.append(userwords[i])
    return res

def notsamewords(userwords, tablewords):
    '''(list, list) -> list

    Checks the dictionary for words entered by the user. Returns words that the player did not type

    >>> notsamewords(['idea', 'keki','waek', 'wife', 'edow'], ['aide', 'idea', 'kike', 'kioea', \
'koae', 'wake', 'weak', 'weki', 'wife', 'wode'])
    ['aide', 'kike', 'kioea', 'koae', 'wake', 'weak', 'weki', 'wode']
    >>> notsamewords(['aide', 'idea', 'kike', 'kioea', 'koae', 'wake', 'weak', 'weki', 'wife', \
'wode'], ['aide', 'idea', 'kike', 'kioea', 'koae', 'wake', 'weak', 'weki', 'wife', 'wode'])
    []'''
    tablewordslen = len(tablewords)
    res = []
    for i in range(0, tablewordslen):
        if tablewords[i] not in userwords:
            res.append(tablewords[i])
    return res

def results():
    '''The game board is generated, the data entered by the player and the dictionary are processed.
    Returning the result to the terminal and the file 'result.txt'
    If there are no word formation variations, the function returns None'''
    generatetbale = generate_grid()
    print(generatetbale)
    dictlist = get_words('targetdict.txt', generatetbale)
    print(dictlist)
    if len(dictlist) == 0:
        return None
    userwords = get_user_words()
    pureuserwords = get_pure_user_words(userwords, generatetbale, dictlist)
    userwordsindict = samewords(userwords, dictlist)
    userwordsnotindict = notsamewords(userwords, dictlist)
    print(userwordsindict)
    print(dictlist)
    print(userwordsnotindict)
    print(pureuserwords)
    with open('result.txt', 'w', encoding='UTF-8') as file:
        file.write(f'Правильні слова -{userwordsindict}\n')
        file.write(f'Усі можливі слова-{dictlist}\n')
        file.write(f'Пропущені слова -{userwordsnotindict}\n')
        file.write(f'Слова, які є відсутніми в словнику -{pureuserwords}')
results()
