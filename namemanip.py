import re

dateRE = re.compile('\d{6,8}')

def find_date(filename):
    """
    find_date(str) --> str
    Pulls a date out of the input and returns it

    >>> find_date('giantbombcast-020210.mp3')
    '020210'
    >>> find_date('4G1U030510.mp3')
    '030510'
    >>> find_date('Rebel_FM_Episode_54_-_031110.mp3')
    '031110'
    """
    results = dateRE.search(filename)
    if results is None:
        return '0'

    return results.group()

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
    
