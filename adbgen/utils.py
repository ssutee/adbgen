def camel_variable_name(name, upper=False):
    '''
    >>> print camel_variable_name('user_id')
    userId
    >>> print camel_variable_name('test_user_id')
    testUserId
    '''
    tokens = name.split('_')
    if len(tokens) == 1:
        return name.capitalize() if upper else name
    else:
        tokens[0] = tokens[0].capitalize() if upper else tokens[0]
        for i in range(1, len(tokens)):
            tokens[i] = tokens[i][0].upper() + tokens[i][1:]
    return ''.join(tokens)        
