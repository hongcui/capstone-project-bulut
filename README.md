# capstone-project

### Title
#### Machine Learning Approach to Finding Similar Geological Samples in EarthChem-PetDB Database

### Reproducibility
- clone the repository
- on terminal: cd capstone-project
- create the conda environment from the yml file: conda env create -f environment.yml
- activate the environment: conda activate final-project
- preprocess the available data and create useful datasets: python createDataset.py
- create label distribution plots: python visuals.py
- run experiments with logistic regression model: python logisticRegression.py 
- run experiments with xgboost model: python xgb.py 
- run experiments with neural networks model: python nn.py 
- run experiments with all models but with leave one out cross validation: python leaveOneOut.py, however this takes a while due to the nature of LOOCV method
- run the model explainer to see which features matter how much: python explainer.py
- run the inference to get top n similar samples given the new samples: python inference.py, remove the break in the loop if you want the results for all new samples
