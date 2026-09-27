RecommendIQ
AI-Powered Recommendation & Personalization Engine

RecommendIQ is an end-to-end Machine Learning project that builds an intelligent recommendation system using the RetailRocket e-commerce dataset.

The project follows a production-oriented workflow, starting from raw data ingestion into MySQL and continuing through data preprocessing, exploratory analysis, feature engineering, customer segmentation, recommendation generation, feedback-based score updating, personalization, model evaluation, API development, and deployment.

The system combines customer behavior, recommendation scores, feedback signals, and personalization logic to generate relevant product recommendations for customers.

Live Demo
Frontend

RecommendIQ Web Application:
https://recommendiq-frontend.onrender.com

Backend API

FastAPI Backend:
https://recommendiq-api.onrender.com

API Documentation

Swagger UI:
https://recommendiq-api.onrender.com/docs

Project Objectives
Build an intelligent recommendation system
Analyze customer behavior using interaction data
Engineer meaningful behavioral features
Segment customers using K-Means clustering
Generate item-based product recommendations
Incorporate customer feedback into recommendation scores
Personalize recommendations using customer behavior and feedback
Evaluate the recommendation system
Serve the ML system through FastAPI
Build an interactive HTML/CSS/JavaScript dashboard
Maintain a modular and reusable project architecture
Containerize the application using Docker
Deploy the application to the cloud
System Workflow
RetailRocket Dataset
        │
        ▼
Load Raw Data into MySQL
        │
        ▼
Data Understanding
        │
        ▼
Data Cleaning
        │
        ▼
Cleaned Data in MySQL
        │
        ▼
Exploratory Data Analysis
        │
        ▼
Feature Engineering
        │
        ▼
Customer Features
        │
        ▼
Customer Segmentation
        │
        ▼
Recommendation Engine
        │
        ▼
Feedback-based Score Updating
        │
        ▼
Personalization
        │
        ▼
Final Recommendation Results
        │
        ▼
Model Evaluation
        │
        ▼
FastAPI Backend
        │
        ▼
Frontend Dashboard
        │
        ▼
Docker
        │
        ▼
Cloud Deployment
Key Components
1. Data Storage

Raw RetailRocket data is loaded into MySQL before downstream processing.

The main raw datasets include:

events.csv
item_properties_part1.csv
item_properties_part2.csv
category_tree.csv

The project also creates cleaned MySQL tables for downstream processing.

2. Data Preprocessing

The preprocessing pipeline handles tasks such as:

Timestamp conversion
Duplicate handling
Missing-value analysis
Transaction validation
Category hierarchy processing
Item-property processing
Creation of cleaned datasets

The preprocessing logic is implemented as reusable Python modules inside src/.

3. Feature Engineering

Customer interaction behavior is converted into numerical features that can be used by the ML pipeline.

Interaction strengths are assigned as follows:

Event	Weight
View	1
Add to Cart	3
Transaction	5

The resulting customer-level features are used for customer segmentation and downstream recommendation logic.

4. Customer Segmentation

RecommendIQ uses K-Means clustering to group customers according to their behavioral patterns.

The segmentation pipeline uses:

Log Transformation
       ↓
Standard Scaling
       ↓
K-Means Clustering

The final segmentation model is stored as:

artifacts/segmentation_pipeline.pkl

The project uses five customer segments:

Cluster	Segment
0	Browsers
1	Inactive
2	Regular Users
3	Buyers
4	Cart Users

The segmentation pipeline can then be used by the API to identify the segment of a visitor.

5. Recommendation Engine

RecommendIQ uses item-based collaborative filtering to generate product recommendations.

The recommendation engine uses item interaction patterns and cosine similarity to identify items that are related to products a customer has previously interacted with.

The main recommendation artifact is:

artifacts/item_similarity.pkl
Existing Users

For an existing user, the system:

Identifies items the user has interacted with
Finds similar items
Calculates recommendation scores
Removes already-seen items
Returns the top recommendations
New Users

For users without sufficient interaction history, the system can fall back to popular items.

6. Feedback System

The recommendation system incorporates user feedback into recommendation scores.

Feedback values are mapped as:

Feedback	Score
Like	1
Neutral	0
Dislike	-1
No Feedback	0

The feedback score is used to update the original recommendation score.

The update uses a learning rate of:

0.10

The updated recommendation score is clipped to the range:

0 → 1

This allows customer feedback to influence future recommendation ranking.

7. Model Evaluation

The project includes a model evaluation stage for assessing the recommendation and segmentation components.

For customer segmentation, the project evaluates clustering quality using the Silhouette Score.

Evaluation is included as part of the project's ML workflow rather than treating deployment as the only objective.

8. FastAPI Backend

The trained models and recommendation logic are exposed through a FastAPI backend.

The backend provides API endpoints for functionality such as:

Customer segmentation
Product recommendations
Recommendation-related processing

Swagger documentation is available at:

https://recommendiq-api.onrender.com/docs

Example segmentation request:

GET /segment/{visitor_id}

Example:

GET /segment/12

Example response:

{
  "visitorid": 12,
  "cluster": 1,
  "customer_segment": "Inactive"
}
9. Frontend Dashboard

RecommendIQ includes an interactive frontend built using:

HTML
CSS
JavaScript

The dashboard allows users to enter a visitor ID and retrieve customer information and recommendations through the FastAPI backend.

The frontend communicates with the deployed API using JavaScript fetch() requests.

Frontend

https://recommendiq-frontend.onrender.com

Backend

https://recommendiq-api.onrender.com

The frontend and backend are deployed separately so that the web interface and API can be independently maintained.

10. CORS Configuration

Because the frontend and backend are deployed as separate services, the FastAPI application is configured to allow requests from the deployed frontend.

The backend allows the production frontend origin:

https://recommendiq-frontend.onrender.com

Local development is also supported through the configured local frontend origin.

Project Structure
RecommendIQ/
│
├── api/
│   ├── main.py
│   ├── routes.py
│   └── service.py
│
├── src/
│   ├── database.py
│   ├── data_preprocessing.py
│   ├── feature_engineering.py
│   ├── segmentation.py
│   ├── recommender.py
│   ├── feedback.py
│   └── personalization.py
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_EDA.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_customer_segmentation.ipynb
│   ├── 06_recommendation_engine.ipynb
│   ├── 07_personalization_engine.ipynb
│   ├── 08_model_evaluation.ipynb
│   └── 09_api_testing.ipynb
│
├── data/
│   └── features/
│
├── artifacts/
│   ├── item_similarity.pkl
│   └── segmentation_pipeline.pkl
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── Dockerfile
├── requirements.txt
└── README.md
Technology Stack
Programming
Python
SQL
JavaScript
HTML
CSS
Machine Learning
Scikit-learn
K-Means Clustering
Cosine Similarity
Collaborative Filtering
Feature Engineering
Data Processing
Pandas
NumPy
Database
MySQL
Backend
FastAPI
Uvicorn
Frontend
HTML
CSS
JavaScript
Deployment
Docker
Render
GitHub
Local Setup
1. Clone the repository
git clone https://github.com/prakhar9754/RecommendIQ.git
cd RecommendIQ
2. Create a virtual environment
python -m venv venv
Windows
venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Configure MySQL

Create the required MySQL database and configure the database connection used by the project.

The raw RetailRocket datasets can then be loaded into the appropriate MySQL tables.

5. Run the FastAPI application

From the project directory:

uvicorn api.main:app --reload

The API will be available at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs
Running the Frontend Locally

The frontend is located inside:

frontend/

The JavaScript frontend communicates with the configured FastAPI backend.

For local development, serve the frontend using a local HTTP server rather than opening the HTML file directly.

For example, using VS Code Live Server:

http://127.0.0.1:5500
Docker

The project includes Docker configuration for containerizing the application.

The Docker setup is intended to make the API environment reproducible and deployment-ready.

Build the image:

docker build -t recommendiq .

Run the container:

docker run -p 8000:8000 recommendiq

The API can then be accessed at:

http://localhost:8000
Cloud Deployment

RecommendIQ is deployed using Render.

The deployment consists of:

GitHub Repository
       │
       ├──────────────► Render Web Service
       │                      │
       │                      ▼
       │                FastAPI Backend
       │
       └──────────────► Render Static Site
                              │
                              ▼
                       Frontend Dashboard
Production Services

Frontend

https://recommendiq-frontend.onrender.com

Backend

https://recommendiq-api.onrender.com

Swagger API Documentation

https://recommendiq-api.onrender.com/docs
Example API Flow

A typical customer request follows this flow:

User enters Visitor ID
        │
        ▼
Frontend sends API request
        │
        ▼
FastAPI Backend
        │
        ├──► Customer Segmentation
        │
        └──► Recommendation Engine
                    │
                    ▼
              Recommendation Results
                    │
                    ▼
              Frontend Dashboard
Reusable Architecture

One of the main goals of RecommendIQ is to separate machine learning logic from API logic.

src/
 │
 ├── Data Processing
 │
 ├── Feature Engineering
 │
 ├── Segmentation
 │
 ├── Recommendation
 │
 ├── Feedback
 │
 └── Personalization
          │
          ▼
       FastAPI
          │
          ▼
      Frontend

This makes individual components easier to:

Test
Reuse
Maintain
Replace
Deploy
Future Improvements

Possible future improvements include:

Improving recommendation evaluation with additional ranking metrics
Adding more advanced personalization strategies
Experimenting with neural-network-based recommendation models
Adding real-time user feedback updates
Improving cold-start recommendations
Adding automated CI/CD
Expanding monitoring and logging
Improving cloud scalability
Adding authentication and user management
Conclusion

RecommendIQ demonstrates a complete machine learning workflow from raw e-commerce interaction data to a deployed recommendation application.

The project combines:

Data Engineering
      +
Machine Learning
      +
Recommendation Systems
      +
Personalization
      +
FastAPI
      +
Frontend Development
      +
Docker
      +
Cloud Deployment

The result is an end-to-end recommendation system that can analyze customer behavior, identify customer segments, generate product recommendations, incorporate feedback, personalize results, and expose the system through a deployed web application.