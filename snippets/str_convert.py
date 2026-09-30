def str_convert(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    '''
    Takes a list of columns and converts their data type to type(str).

    Args:
    - user_list = list of columns to convert

    Outputs:
    - type "str" columns into df
    '''

    for col in columns:

        # raise error if name not found
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame.")

        # convert
        df[col] = df[col].astype(str)

    return df
