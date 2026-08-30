FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY api ./api
COPY src ./src
COPY artifacts/segmentation_pipeline.pkl ./artifacts/
COPY artifacts/item_similarity.pkl ./artifacts/

COPY data/features/customer_features.csv ./data/features/
COPY data/features/user_item_features.csv ./data/features/

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]