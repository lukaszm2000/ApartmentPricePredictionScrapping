# ApartmentPricePredictionScrapping

##Overview
This project scrapes housing offers from the Otodom (https://www.otodom.pl/) portal based on user input for location and price range. The scraped data is then cleaned and visualized using Streamlit. 
Additionally, several machine learning models are employed to predict the selling prices of apartments based on the scraped data.
Note: The state of the website used for scraping is accurate as of July 10, 2024.

##Features
-User Input for Custom Search: Users can specify the desired location and price range to scrape housing offers directly from the Otodom website.
-Data Cleaning: The scraped data undergoes a cleaning process to ensure accuracy and relevance.
-Data Visualization: The cleaned data is visualized using Streamlit to help users gain insights into the housing market. To run the visualization, simply enter in terminal: streamlit run visualization.py
-Price Prediction: Several machine learning models are used to predict housing prices based on the features extracted from the scraped data.

##Machine Learning Models
The project leverages multiple machine learning models to predict housing prices.
Each model is evaluated based on its performance, and the best-performing model is selected for making predictions.

##Future Work
-Enhancing Model Accuracy: Experiment with more advanced models and feature engineering techniques.
-Expanding the Search Criteria: Allow users to specify additional criteria such as apartment size, etc.
-Deploying the Prediction Model: Integrate the model into a web application for real-time predictions.

