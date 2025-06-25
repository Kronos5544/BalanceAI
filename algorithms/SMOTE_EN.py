import numpy as np
from sklearn.linear_model import ElasticNet
from joblib import Parallel, delayed
from sklearn.preprocessing import StandardScaler
from algorithms.resampling_algorithm import ResamplingAlgortihmUtils

class SMOTEEN(ResamplingAlgortihmUtils):
    def fit_resample(self, x : np.ndarray, y : np.ndarray, alpha: float = 0.5, l1_ratio: float = 0.5, n_jobs: int = -1) -> tuple:
        """Main method: Generates synthetic samples using ElasticNet regression"""
           
        dataset = self._in_out_to_dataframe(x, y)
        class_stats = self._get_class_stats(dataset)

        # Preparing data
        minority_data = self._get_minority_class_data(dataset, class_stats["minority_class_name"])
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(minority_data)
        
        # fitting model
        elastic_net_model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio)
        elastic_net_model.fit(X_scaled, X_scaled)
        
        # Genering instances
        n_synthetic = class_stats["majority_class_count"] - class_stats["minority_class_count"]
        percentiles = self._get_percentiles(dataset, class_stats["minority_class_name"])
        
        synthetic_instances = Parallel(n_jobs=n_jobs)(
            delayed(self._generate_instance)(scaler, percentiles, minority_data.columns, elastic_net_model)
            for _ in range(n_synthetic)
        )
        
        # Returning data
        return self._get_balanced_data(synthetic_instances, dataset)
    
    def _generate_instance(self, scaler, percentiles: dict, columns, elastic_net_model):
        """Generate single synthetic instance with percentile-based clipping"""
        noise = np.random.normal(scale=0.3, size=(1, elastic_net_model.coef_.shape[0]))
        instance = scaler.inverse_transform(elastic_net_model.predict(noise))[0]
        
        # Apply bounds based on percentiles
        for i, col in enumerate(columns):
            p1 = percentiles[col]['p1']
            p99 = percentiles[col]['p99']
            instance[i] = np.clip(instance[i], p1, p99)
            instance[i] = round(instance[i], 2)
        return instance
