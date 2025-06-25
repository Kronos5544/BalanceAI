from algorithms.resampling_algorithm import ResamplingAlgortihmUtils
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso

class SMOTERL(ResamplingAlgortihmUtils):
    def _generate_instance(self, scaler, min_max: dict, lasso_model : Lasso) -> np.ndarray:
        """Generate single synthetic instance with Lasso regression and clipping"""
        noise = np.random.normal(scale=0.3, size=(1, lasso_model.coef_.shape[0]))
        instance = scaler.inverse_transform(lasso_model.predict(noise))[0]
    
        # Apply bounds based on percentiles
        for i, col in enumerate(min_max.keys()):
            instance[i] = np.clip(instance[i], min_max[col]['p1'], min_max[col]['p99'])
    
        return np.round(instance, 2)
    
    def _generate_synthetic_instances(self, scaler, n_instances: int, n_jobs: int, lasso_model : Lasso, dataset : pd.DataFrame, minority_class_name : str) -> np.ndarray:
        """Parallel generation of synthetic instances"""
        min_max = self._get_percentiles(dataset, minority_class_name)
        return Parallel(n_jobs=n_jobs)(
            delayed(self._generate_instance)(scaler, min_max, lasso_model)
            for _ in range(n_instances)
        )
    
    def fit_resample(self, x: np.ndarray, y : np.ndarray, alpha: float = 1.0, n_jobs: int = -1):
        """Main method: Generates synthetic samples using Lasso regression"""
        dataset = self._in_out_to_dataframe(x, y)
        class_stats = self._get_class_stats(dataset)

        # Preparing data
        minority_data = self._get_minority_class_data(dataset, class_stats["minority_class_name"])
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(minority_data)
        
        # Fitting model
        lasso_model = Lasso(alpha=alpha)
        lasso_model.fit(X_scaled, X_scaled)
        
        # Generate instances
        n_synthetic = class_stats["majority_class_count"] - class_stats["minority_class_count"]
        synthetic_data = self._generate_synthetic_instances(scaler, n_synthetic, n_jobs, lasso_model, dataset, class_stats["minority_class_name"])
        
        # Returning balanced data
        return self._get_balanced_data(synthetic_data, dataset)
