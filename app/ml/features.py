def create_features(df):
    return df.groupby("user_id").agg(
        accuracy=("correct", "mean"),
        attempts=("problem_id", "count"),
        avg_time=("time_taken", "mean")
    ).reset_index()