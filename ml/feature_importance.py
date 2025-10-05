import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.inspection import permutation_importance

np.random.seed(42)

# Load data
train_df = pd.read_csv('data/processed_train_data.csv')
test_df = pd.read_csv('data/processed_test_data.csv')

y_train = train_df['koi_disposition'].values
X_train = train_df.drop('koi_disposition', axis=1)
y_test = test_df['koi_disposition'].values
X_test = test_df.drop('koi_disposition', axis=1)

# Train the same stacking model
base_estimators = [
    ('random_forest', RandomForestClassifier(n_estimators=500, random_state=42, n_jobs=-1)),
    ('gradient_boosting', GradientBoostingClassifier(n_estimators=200, random_state=42))
]

stacking_model = StackingClassifier(
    estimators=base_estimators,
    final_estimator=LogisticRegression(random_state=42, max_iter=1000),
    cv=5,
    n_jobs=-1
)

print("Training Stacking model...")
stacking_model.fit(X_train, y_train)

# Get feature importance from base estimators
print("\n" + "="*60)
print("FEATURE IMPORTANCE FROM BASE ESTIMATORS")
print("="*60)

# Random Forest importance
rf_importance = pd.DataFrame({
    'feature': X_train.columns,
    'rf_importance': stacking_model.named_estimators_['random_forest'].feature_importances_
})

# Gradient Boosting importance
gb_importance = pd.DataFrame({
    'feature': X_train.columns,
    'gb_importance': stacking_model.named_estimators_['gradient_boosting'].feature_importances_
})

# Combine
combined_importance = rf_importance.merge(gb_importance, on='feature')
combined_importance['avg_importance'] = (
    combined_importance['rf_importance'] + combined_importance['gb_importance']
) / 2
combined_importance = combined_importance.sort_values('avg_importance', ascending=False)

print("\nTop 20 Features (Average from both base estimators):")
print(combined_importance.head(20))

# Permutation importance on the full stacking model
print("\nCalculating permutation importance for full stacking model...")
perm_importance = permutation_importance(
    stacking_model, X_test, y_test, n_repeats=10, random_state=42, n_jobs=-1
)

perm_df = pd.DataFrame({
    'feature': X_train.columns,
    'perm_importance': perm_importance.importances_mean
}).sort_values('perm_importance', ascending=False)

# Visualize
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# RF importance
axes[0].barh(combined_importance.head(15)['feature'], 
             combined_importance.head(15)['rf_importance'])
axes[0].set_title('Random Forest Base Estimator')
axes[0].invert_yaxis()

# GB importance
axes[1].barh(combined_importance.head(15)['feature'], 
             combined_importance.head(15)['gb_importance'])
axes[1].set_title('Gradient Boosting Base Estimator')
axes[1].invert_yaxis()

# Permutation on full stack
axes[2].barh(perm_df.head(15)['feature'], 
             perm_df.head(15)['perm_importance'])
axes[2].set_title('Stacking Model (Permutation)')
axes[2].invert_yaxis()

plt.tight_layout()
plt.savefig('stacking_feature_importance.png', dpi=300, bbox_inches='tight')
plt.show()

# Save results
combined_importance.to_csv('stacking_base_estimators_importance.csv', index=False)
perm_df.to_csv('stacking_permutation_importance.csv', index=False)

print("\nResults saved!")