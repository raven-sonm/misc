def cols_to_drop( dataframe ):
  '''Given a dataframe, returns columns that should likely be dropped'''
  md = metadata( dataframe )
  filter = md["Nulls_pct"] >= 75
  return md[ filter ]["Nulls_pct"].to_dict()
