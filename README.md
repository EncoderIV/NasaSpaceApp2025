# NasaSpaceApp2025 - Team Aventura

Over the last few years, advancements in tehcnology have allowed scientists, engineers, and space enthusiasts to extract lots of data from several different space-based exoplanet surveying missions. However, it is difficult to manually analyze trends in such large dataset to identify exoplanets. Our project leverages these large datasets, specifically the Kepler Object of Interest dataset from NASA, to train a Stacking Ensemble machine learning model with a RandomForest and GradientBoosting estimators to identify exoplanets with 81% accuracy. The project aims to automate and accelerate the discovery of thousands of new exoplanets outside our solar system and advance scientific research.

Our project [demo]() demo walks you through the user interface of the project and expected inputs and outputs. You can run this script yourself using the notebooks on google colab or by cloning this package and installing it locally.

## Project Organization

```
├── LICENSE              <- Open-source license if one is chosen
├── .gitignore           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── ml
│   ├── data        <- Raw and transformed data.
│   ├── models      <- The model.
│   ├── notebooks      <- The Jupyter notebooks used for R analysis.
│   └── visualizations            <- The visualziations generated during EDA
│
├── frontend               <- A default mkdocs project; see www.mkdocs.org for details
│
├── backend             <- Trained and serialized models, model predictions, or model summaries
    
```

--------

