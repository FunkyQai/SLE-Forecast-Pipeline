AIAP Batch 18 Technical Assessment

## Contributor Information
- **Full Name:** Abdul Qaiyum Lee Bin Abdul Aziz
- **Email Address:** abdulqaiyumlee@gmail.com


## Overview
1. [Folder Structure](#folder-structure)
2. [Execution Instructions](#execution-instructions)
3. [Pipeline Design and Logical Flow](#pipeline-design-and-logical-flow)
4. [EDA](#eda)
5. [Feature Processing](#feature-processing)
6. [Model Selection](#model-selection)
7. [Model Evaluation](#model-evaluation)
8. [Deployment Considerations](#deployment-considerations)


### Folder Structure

The project folder has the following structure:

```
aiap18-Abdul-Qaiyum-Lee-Bin-Abdul-Aziz-057I/
├── .github/
├── src/
│   ├── features/
│   │   ├── constants.py
│   │   ├── preprocessing.py
│   │   └── utils.py
│   ├── model/
│   │   ├── config.py
│   │   └── train.py
│   └── main.py
├── eda.ipynb
├── run.sh
├── requirements.txt
└── README.md
```


## Detailed Descriptions

- **.github/**: This directory is used to store GitHub-specific files, such as GitHub Actions workflows, which automate tests, builds, and deployment processes.

- **src/**: Contains all the source code. It is organized into different subdirectories for better modularity.

  - **features/**: This subdirectory contains scripts that are crucial for feature engineering, including preprocessing and utility functions.
    - **constants.py**: Stores constants that are used throughout the feature engineering process, ensuring consistency and ease of maintenance.
    - **preprocessing.py**: Defines a Preprocessing class to for data cleaning, feature engineering, handling missing values, normalization, and encoding.
    - **utils.py**: Provides utility functions for logging and a Database class to query the database.

  - **model/**: Contains the scripts necessary for model configuration and training.
    - **config.py**: Defines the configuration parameters for the machine learning models and hyperparameter tuning (GridSearchCV).
    - **train.py**: Defines a ModelTrainer class for training and evaluating machine learning models.

- **main.py**: The main executable script for the project. It orchestrates the data processing, feature engineering, and model training steps.

- **eda.ipynb**: A Jupyter notebook that contains the exploratory data analysis. It provides insights into the data through visualizations and statistical analysis.

- **run.sh**: A shell script that provides a simple way to run the entire pipeline with a single command. It can include environment setup, data downloading, and executing the `main.py` script.

- **requirements.txt**: Lists all the Python packages required to run the project. This file is used with `pip` to install dependencies in a consistent environment.

- **README.md**: Provides an overview of the project, including how to set up and run the pipeline, a description of the project structure, and any other relevant information for users or contributors.


## Execution Instructions

This section details the steps required to execute the pipeline, including how to run scripts and modify parameters for customization.

To execute the pipeline, run the following command in the terminal:

```bash
./run.sh
```
The pipeline can be configured using the following command line arguments:
```
usage: main.py [-h] [--tune] [--pca]

Run the end-to-end pipeline with configurable parameters.

optional arguments:
  -h, --help  show this help message and exit
  --pca       Perform PCA on the data before training the models. The number of components can be determined using the PCA variance threshold defined in models/config.py.        
  --tune      Perform hyperparameter tuning for the models using GridSearchCV. The parameters can be configured in models/config.py.

```

To change the parameters of the machine learning models, edit the 'config.py' file in the 'src/model' directory. The list of configurables include:

1. `MODEL_PARAMETERS`: a Python dictionary containing nested dictionaries, where each top-level key represents a model name and its value is another dictionary of parameters specific to that model.
2. `pca_variance_threshold`: Variance threshold for PCA
3. `param_grid_svc`, `param_grid_rf`, `param_grid_gb`, `param_grid_xgb`: Dictionary of parameters to be run with GridSearchCV to find the best parameters for model tuning.


## Pipeline Design and Logical Flow

The pipeline follows these logical steps:

1. **Initialization**: Parse command-line arguments to determine if PCA and/or hyperparameter tuning should be performed.
2. **Setup Logging**: Initialize logging to track the pipeline's progress and any potential issues.
3. **Data Querying**: Retrieves weather and air quality data from the database. Performed using `Database` class in `utils.py`.  
4. **Data Preprocessing**: Performed using `Preprocessing` class in `preprocessing.py`
   - Clean weather and air quality data.
   - Merge datasets.
   - Perform feature engineering:
   - Remove outliers.
   - Normalize numerical data.
   - Encode ordinal columns.
5. **PCA (Optional)**: If specified, perform Principal Component Analysis (PCA) to reduce dimensionality based on the variance threshold. Performed using `ModelTrainer` class in train.py.
6. **Model Training**: Train SVM, Random Forest, Gradient Boosting, and XGBoost models with the preprocessed data. Performed using `ModelTrainer` class in train.py.
7. **Hyperparameter Tuning (Optional)**: If specified, perform hyperparameter tuning for each model using GridSearchCV with predefined parameter grids. Performed using `ModelTrainer` class in train.py.


## EDA

*Note*: This section focuses exclusively on the features incorporated into the machine learning pipeline.

### Key Findings from EDA

1. Duplicate entries based on `data_ref` in both weather and air quality data.
2. Numerous numerical columns within the weather and air quality datasets exhibited missing values, denoted by '-' or '--'. To address this, we employed bidirectional data interpolation, a method that estimates missing values by considering the nearest points in both forward and backward directions. This approach is grounded in the understanding that weather and air quality metrics typically follow a continuous trend.
3. Negative values in `Max Wind Speed (km/h)` in weather data.
4. Inconsistent catergorical names for `Wind Direction` in weather data.

### Feature Engineering

1. `Average Wind Speed (km/h)`: Calculated by taking the average of `Min Wind Speed (km/h)` and `Max Wind Speed (km/h)`
2. `pm25_northeast`, `pm25_northwest`, `pm25_southeast`, `pm25_southwest`: These features are derived by averaging PM2.5 measurements from adjacent cardinal directions. For example, `pm25_northeast` is calculated as the mean of `pm25_north` and `pm_25east`. This approximation method is employed in the absence of direct regional data, providing a simplified yet effective way to estimate PM2.5 concentrations across different sectors.
3. `pm25`: Derived from merging data from the weather and air quality datasets, selecting PM2.5 values that align with the wind's direction.
4. `month`, `quarter` and `week of the year`: Dervied from the `date` feature to capture seasonal and periodic trends in the data.

### Choices to be made

- The inclusion of the `pm25` feature, despite its marginal significance (p-value=0.089), is justified by its potential interaction with wind speed—a factor crucial for solar panel efficiency. Wind speed directly impacts solar panels and may also indirectly affect their efficiency by transporting particulate matter (`pm25`). This can lead to the accumulation or removal of pm25 on the panels, thereby influencing their operational efficiency.

### Features to be used:

Numerical:
1. `Highest 60 Min Rainfall (mm)`
2. `Highest 120 Min Rainfall (mm)`
3. `Maximum Temperature (deg C)`
4. `Cloud Cover (%)`
5. `Air Pressure (hPa)`
6. `Sunshine Duration (hrs)`
7. `Average Wind Speed (km/h)`
8. `pm25`

Catergorical:
1. `month`
2. `quarter`
3. `week of the year`
(The categorical features are further processed in the machine learning pipeline. Details will be shared in the next section)


## Feature Processing

The following table summarizes the feature processing steps from the `Preprocessing` class in the pipeline:
<table border="1">
  <thead>
    <tr>
      <th>Method</th>
      <th>Description</th>
      <th>Comments</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>clean_weather_data</code></td>
      <td>Cleans the data by:
        <ol>
          <li>Removing duplicate entries based on <code>data_ref</code></li>
          <li>Dropping irrelevant columns: <code>Wet Bulb Temperature (deg F)</code>, <code>Daily Rainfall Total (mm)</code>, <code>Highest 30 Min Rainfall (mm)</code>, <code>Min Temperature (deg C)</code>, <code>Relative Humidity (%)</code>, <code>Dew Point Category</code>, <code>data_ref</code>.</li>
          <li>Converting selected columns from object to numeric types. <code>Highest 60 Min Rainfall (mm)</code>, <code>Highest 120 Min Rainfall (mm)</code>, <code>Maximum Temperature (deg C)'</code>, <code>Min Wind Speed (km/h)</code>, <code>Max Wind Speed (km/h)</code></li>
          <li>Handling missing numerical values through interpolation.</li>
          <li>Taking the absolute value of <code>Max Wind Speed (km/h)</code>.</li>
          <li>Standardizing <code>Wind Direction</code> categories.</li>
        </ol>
      </td>
      <td>Columns are dropped early on to ensure smaller data size and quicker operations.</td>
    </tr>
    <tr>
      <td><code>clean_air_quality_data</code></td>
      <td>Cleans the data by:
        <ol>
          <li>Removing duplicate entries based on <code>data_ref</code></li>
          <li>Dropping irrelevant columns: <code>psi_north</code>, <code>psi_south</code>, <code>psi_east</code>, <code>psi_west</code>, <code>psi_central</code>, <code>pm25_central</code>, <code>data_ref</code></li>
          <li>Handling missing numerical values through interpolation: <code>pm25_north</code>, <code>pm25_south</code>, <code>pm25_east</code>, <code>pm25_west</code></li>
        </ol>
      </td>
      <td>Columns are dropped early on to ensure smaller data size and quicker operations.</td>
    </tr>
    <tr>
      <td><code>merge_data</code></td>
      <td>Merges weather data and air quality data on <code>date</code> column</td>
      <td></td>
    </tr>
    <tr>
      <td><code>feature_engineering</code></td>
      <td>Creates two new features:
        <ol>
          <li>Create <code>Average wind speed (km/h)</code> by taking the average of <code>Min Wind Speed (km/h)</code> and <code>Max Wind Speed (km/h)</code> </li>
          <li>Create <code>pm25_northeast</code>, <code>pm_25northwest</code>, <code>pm_25southeast</code>, <code>pm_25southwest</code> by averaging PM2.5 measurements from adjacent cardinal directions.</li>
          <li>Create <code>pm25</code> column based on <code>Wind Direction</code></li>
          <li>Create <code>Month</code>, <code>quarter</code>, <code>week of the year</code> from <code>date</code></li>
          <li>Add cyclical features for month, quarter, and week of the year</li>
          <li>Drop irrelevant columns: <code>Max Wind Speed (km/h)</code>, <code>Min Wind Speed (km/h)</code>, <code>date</code>, <code>Wind Direction</code>, <code>pm25_north</code>, <code>pm25_south</code>, <code>pm25_east</code>, <code>pm25_west</code>, <code>pm25_northeast</code>, <code>pm25_northwest</code>, <code>pm25_southeast</code>, <code>pm25_southwest</code>, <code>month</code>, <code>quarter</code>, <code>week of the year</code></li>
        </ol>
      </td>
      <td>Opted for adding cyclical features for date-related categories, such as <code>month</code>, <code>quarter</code>, and <code>week of the year</code>, to avoid the sparse matrix issue inherent in one-hot encoding, which could complicate model training. Cyclical features effectively capture the inherent cyclical nature of these time units, illustrating that, for instance, week 1 is closer to week 52 than to week 26, thereby preserving the continuity and proximity of temporal data.</td>
    </tr>
    <tr>
      <td><code>remove_outliers</code></td>
      <td>Removes outliers from specified columns using the IQR method. <code>Highest 60 Min Rainfall (mm)</code>, <code>Highest 120 Min Rainfall (mm)</code>, <code>pm25</code>, <code>Maximum Temperature (deg C)</code>, <code>Average Wind Speed (km/h)</code>, <code>Cloud Cover (%)</code>, <code>Air Pressure (hPa)</code>, <code>Sunshine Duration (hrs)</code></td>
      <td>Outliers can skew the data and negatively impact the model's performance. Removing them makes the model more robust.</td>
    </tr>
    <tr>
      <td><code>normalize_data</code></td>
      <td>Standardizes numerical columns to have mean 0 and standard deviation 1.</td>
      <td>Standardizing the data ensures that the model treats all features that are on different scales equally. For example, the Rainfall and Air Pressure features might shift differently. This is important for models such as Support Vector Machine where it uses Euclidean distance to compare two different samples. If every feature has a different scale, the euclidean distance only take into account the features with highest scale  It also helps the model converge faster.</td>
    </tr>
    <tr>
      <td><code>ordinal_encoding</code></td>
      <td>Ordinal encodes ordinal columns based on the provided order. Namely, <code>Daily Solar Panel Efficiency</code></td>
      <td>Ordinal encoding preserves the natural order of the categories so that the model can leverage on them. For example, the model should be able to learn that 'Low' is less than 'Medium' and 'Medium' is less than 'High'.</td>
    </tr>
  </tbody>
</table>


## Model Selection

In the development of predictive models for classifying solar panel efficiency as 'Low', 'Medium', or 'High', four primary classifiers were evaluated: RandomForest Classifier, XGBoost Classifier, Gradient Boost Classifier, and SVM Classifier. Each model has its unique advantages and challenges, as outlined below:

### RandomForest Classifier
- **Pros:**
  - Excellent at handling both categorical and numerical data, making it suitable for weather data's diverse nature.
  - Offers insights into feature importance, crucial for identifying which weather factors most affect solar panel efficiency.
  - Resilient against overfitting, ensuring reliable predictions even with complex weather data patterns.
- **Cons:**
  - Its complexity and computational demands can escalate with the number of trees, potentially slowing down model training and prediction phases.

### SVM Classifier
- **Pros:**
  - Performs well in high-dimensional spaces, such as when dealing with extensive weather data features.
  - Effective when there's a clear margin of separation, aiding in distinguishing between the different efficiency levels accurately.
- **Cons:**
  - Not suited for large datasets due to poor performance and speed, which could be a limitation given the extensive historical weather data involved.
  - Sensitive to kernel parameter choices, demanding thorough fine-tuning.

### XGBoost Classifier
- **Pros:**
  - Known for its high performance and speed, enabling timely efficiency predictions.
  - Capable of handling missing data, a common issue in weather datasets.
  - Incorporates regularization to curb overfitting, ensuring that our model generalizes well to unseen data.
- **Cons:**
  - Risk of overfitting if hyperparameters are not meticulously tuned, necessitating careful optimization to achieve the best results.
  - More complex and potentially more computationally intensive than other models, which could be a consideration if computational resources are limited.

### Gradient Boost Classifier
- **Pros:**
  - Provides top-notch accuracy, a critical factor in correctly classifying efficiency levels to optimize operational planning.
  - Highly flexible, allowing for customization to our specific needs through loss function optimization and hyperparameter tuning.
  - Often used as a baseline for comparison due to its simplicity and effectiveness in a wide range of tasks.
- **Cons:**
  - Its sequential nature makes training time-consuming, which could delay the deployment of our predictive models.
  - While it offers high accuracy, if results are comparable to more complex models like XGBoost, the preference might lean towards Gradient Boost due to its lower computational demands.


## Model Evaluation
Discuss how the models were evaluated, including the metrics used. Provide insights into the performance of each model and any optimizations or adjustments made.

## Deployment Considerations
Outline any considerations for deploying the models developed, including potential challenges and how they might be addressed.

