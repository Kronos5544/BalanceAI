from algorithms.resampling_algorithm import ResamplingAlgortihmUtils
import numpy as np
import pandas as pd
from numpy import random as np_random
import numpy.linalg as la
from typing import Union, Tuple

class SMOTECOVLW(ResamplingAlgortihmUtils):
    def __init__(self):
        """Initialize constants for sampling and regularization"""
        self.SPACES = 100
        self.BASE_BATCH_SIZE = 2000
        self.REGULARIZATION_EPS = 1e-6

    def _get_attribute_stats(self, stat: str, dataset : pd.DataFrame, minority_class_name : str) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
      """Compute statistical properties (min, max, mean, std) of minority class features"""
      
      # Load minority data
      minority_data = self._get_minority_class_data(dataset, minority_class_name).values.astype(np.float32)
    
      # Vectorized Calculations
      mins = np.min(minority_data, axis=0)
      maxs = np.max(minority_data, axis=0)
      means = np.mean(minority_data, axis=0)
    
      # Selection of required static
      if stat == "mean":
          return means
      elif stat == "min_max":
          return (mins, maxs)
      elif stat == "std":
          return np.std(minority_data, axis=0)
      else:
          return {
              'min': mins,
              'max': maxs,
              'mean': means,
              'std': np.std(minority_data, axis=0)
          }

    def _compute_covariance_matrix(self, method: str, dataset : pd.DataFrame, minority_class_name : str, n_features) -> np.ndarray:
      """Compute regularized covariance matrix using Ledoit-Wolf shrinkage"""
      min_class_data = self._get_minority_class_data(dataset, minority_class_name)
    
      if method == "sklearn":
          from sklearn.covariance import LedoitWolf
          lw = LedoitWolf().fit(min_class_data)
          covariance_matrix = lw.covariance_.astype(np.float32)
      else:
          raise ValueError("Method not implemented")
    
      # Dimension validation    
      if covariance_matrix.shape != (n_features, n_features):
          raise RuntimeError("Covariance Matrix has incorrect dimensions")
      return covariance_matrix
      
    def _precompute_cholesky(self, covariance_matrix : np.ndarray) -> np.ndarray:
        """Compute Cholesky decomposition with regularization for numerical stability"""
        
        try:
            L = la.cholesky(covariance_matrix + self.REGULARIZATION_EPS * np.eye(
                covariance_matrix.shape[0], dtype=np.float32))
            return L
        except la.LinAlgError:
            # Fallback SVD for bad conditioned matrix
            U, s, _ = la.svd(covariance_matrix)
            L = U @ np.diag(np.sqrt(s + self.REGULARIZATION_EPS))
            return L
        
    def _vectorized_generate(self, mean: np.ndarray, n_samples: int, n_features : int, L : np.ndarray) -> np.ndarray:
        """Generate synthetic samples using multivariate normal distribution"""
        std_samples = np_random.normal(size=(n_samples, n_features)).astype(np.float32)
        return mean + std_samples @ L.T
    
    def _process_ranges(self, data: np.ndarray, mins: np.ndarray, maxs: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Clip values to feature ranges and adjust outliers with random offsets"""
        
        # Data within the range
        in_range = np.clip(data, mins, maxs)
        
        # Data out of range (optimized)
        mask = (data >= mins) & (data <= maxs)
        rows, cols = np.where(mask)
        
        if rows.size > 0:
            offsets = np.abs(np_random.normal(
                scale=0.1*(maxs[cols] - mins[cols]),
                size=len(rows)).astype(np.float32))
            
            choices = np_random.choice([-1, 1], size=len(rows))
            data[rows, cols] = np.where(
                choices == -1,
                mins[cols] - offsets,
                maxs[cols] + offsets
            )
        
        return in_range, data
    
    def fit_resample(self, x : np.ndarray, y : np.ndarray, method: str = "sklearn", use_gpu: bool = False):
        """Main method: Generates synthetic samples using covariance-based approach"""
        dataset = self._in_out_to_dataframe(x, y)
        class_stats = self._get_class_stats(dataset)

        n_synthetic = class_stats["majority_class_count"] - class_stats["minority_class_count"]

        # Optimization setup
        n_features = dataset.shape[1] - 1
        dynamic_batch_size = max(1, self.BASE_BATCH_SIZE // n_features)
        covariance_matrix = self._compute_covariance_matrix(method, dataset, class_stats["minority_class_name"], n_features)
        L = self._precompute_cholesky(covariance_matrix)

        #Initial setup
        mean = self._get_attribute_stats("mean", dataset, class_stats["minority_class_name"])
        mins, maxs = self._get_attribute_stats("min_max", dataset, class_stats["minority_class_name"])

        # Preallocated buffers
        in_range_data = np.empty((n_synthetic, n_features), dtype=np.float32)
        free_range_data = np.empty((n_synthetic, n_features), dtype=np.float32)

        # Batch generation
        generated = 0
        while generated < n_synthetic:
            current_batch = min(dynamic_batch_size, n_synthetic - generated)
            
            # Optimized generation
            synthetic = self._vectorized_generate(mean, current_batch, n_features, L)
            
            # Range processing  
            batch_slice = slice(generated, generated + current_batch)
            in_range_data[batch_slice], free_range_data[batch_slice] = \
                self._process_ranges(synthetic, mins, maxs)
            
            generated += current_batch

        # Returning results
        in_range = self._get_balanced_data(in_range_data, dataset)
        free_range = self._get_balanced_data(free_range_data, dataset)
        datasets = {
            "in_range" : in_range,
            "free_range" : free_range
        }
        return datasets
