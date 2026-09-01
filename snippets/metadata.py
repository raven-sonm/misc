# helper functions

def metadata( dataframe ):
  '''Given a dataframe, returns a dataframe of metadata about the dataframe'''

  # define vars
  metadata_df = pd.DataFrame()
  duplicate_count = dataframe.apply(lambda col: col.duplicated().sum(), axis=0)

  # create new cols
  metadata_df["Data_types"] = dataframe.dtypes
  metadata_df["Nullable"] = dataframe.isnull().any().values
  metadata_df["Example_value"] = [dataframe[col].dropna().iloc[0] if dataframe[col].notnull().any() else None for col in dataframe.columns]
  metadata_df["Dups_pct"] = round((( duplicate_count / len(dataframe) ) * 100), 2)
  metadata_df["Nulls_pct"] = ( ( dataframe.isnull().sum() ) / ( len(dataframe) ) * 100 ).round(1)
  metadata_df["NUnique_pct"] = (dataframe.nunique() / ( len(dataframe) ) * 100).round(1)
  metadata_df["Drop_col"] = metadata_df["Nulls_pct"] >= 75
  metadata_df["Likely_ID"] = metadata_df["NUnique_pct"] > 95
  metadata_df["Memory"] = dataframe.memory_usage( deep = True)

  metadata_df = metadata_df.join( dataframe.describe( include = "all" ).transpose() )
  metadata_df = metadata_df.astype( { "count" : int } )

  if dataframe.select_dtypes(include=['number']).shape[1] :
    metadata_df["IRQ"] = metadata_df["75%"] - metadata_df["25%"]
    metadata_df["range"] = metadata_df["max"] - metadata_df["min"]
    metadata_df["sum"] = metadata_df["mean"] * metadata_df["count"]
    metadata_df = (
      metadata_df
      .rename( columns = {
        "25%" : "Q1_25%",
        "50%" : "Q2_median",
        "75%" : "Q3_75%",
        }
      )
    )
  print(f'Dataframe dimensions: {dataframe.shape}')

  # DEPRECATED
  # metadata_df["Nulls"] = dataframe.isnull().sum()
  # metadata_df["NUnique"] = dataframe.nunique()
  # metadata_df["Count"] = len(dataframe)

  return metadata_df# .sort_values(ascending=True, by=metadata_df[0])
