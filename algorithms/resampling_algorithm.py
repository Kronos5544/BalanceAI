import numpy as np
import pandas as pd

class ResamplingAlgortihmUtils:
    def _get_percentiles(self, dataset : pd.DataFrame, minority_class_name : str) -> dict:
            """Calculate 1st and 99th percentiles for each feature in minority class"""
            minority_data = self._get_minority_class_data(dataset, minority_class_name)
            return {
                col: {
                    'p1': np.percentile(minority_data[col], 1),
                    'p99': np.percentile(minority_data[col], 99)
                }
                for col in minority_data.columns
            }

    def _get_class_stats(self, dataset) -> dict:
            """Compute class distribution statistics (minority/majority)"""
            counts = dataset["class"].value_counts().sort_values()
            minority_class_name = counts.index[0]
            minority_class_count = counts.iloc[0]
            majority_class_count = counts.iloc[1]
            stats_dict = {
                   "minority_class_name" : minority_class_name,
                   "minority_class_count" : minority_class_count,
                   "majority_class_count" : majority_class_count
            }
            return stats_dict

    def _get_minority_class_data(self, dataset : pd.DataFrame, minority_class_name) -> pd.DataFrame:
            """Extract minority class samples excluding class column"""
            return dataset[
                dataset["class"] == minority_class_name
            ].drop("class", axis=1)
    
    def _in_out_to_dataframe(self, x : np.ndarray, y : np.ndarray) -> pd.DataFrame:
           """Convert input arrays (features + target) to DataFrame"""
           dataframe = pd.DataFrame(x)
           dataframe["class"] = y
           return dataframe
    
    def _get_balanced_data(self, synthetic_data: list, dataset):
            """Combine original data with synthetic samples"""
            synthetic_df = pd.DataFrame(
                synthetic_data,
                columns=dataset.columns.drop("class"))
            synthetic_df["class"] = self._get_class_stats(dataset)["minority_class_name"]
            
            balanced_df = pd.concat([dataset, synthetic_df], ignore_index=True)
            x_fit = np.array(balanced_df.drop("class", axis=1))
            y_fit = np.array(balanced_df["class"])
            return x_fit, y_fit
