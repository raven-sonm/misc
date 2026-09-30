def find_value(df, user_value):
    '''
    Searches an entire dataframe for a specific value.

    Args:
    - user_value = the value to find (use apostraphes to define ALL types, e.g., '505')
    - df = the dataframe to search

    IMPORTANT:
    - When inserting "user_value", ensure quotations unless the value unless numeric.
    '''

    result = df[df.apply(lambda row: row.astype(str).str.strip().eq(user_value)).any(axis=1)]

    if len(result) > 0:
        print('Value found:')
        return result.head(5)
    else:
        print('No value was found.')
