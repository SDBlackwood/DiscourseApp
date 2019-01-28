echo 


## Crete the unique index for the reddit_ids
self.ids.create_index([('reddit_id', ASCENDING)],unique=True)