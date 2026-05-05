from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.neural_network import MLPClassifier
from imblearn.under_sampling import NearMiss
from imblearn.pipeline import Pipeline

def train_model(X_train, y_train, feature_range, k, version, hidden_layer_sizes, alpha, max_iter, random_state):
  steps = [
    ('normalization', MinMaxScaler(
      feature_range=tuple(feature_range))), 
    ('features', SelectKBest(
      score_func=f_classif, 
      k=k)), 
    ('rebalancing', NearMiss(version=version)), 
    ('classification', MLPClassifier( 
      hidden_layer_sizes=tuple(hidden_layer_sizes), 
      alpha=alpha, 
      max_iter=max_iter, 
      random_state=random_state))
  ]
  pipeline = Pipeline(steps)
  pipeline.fit(X_train, y_train)
  return pipeline
