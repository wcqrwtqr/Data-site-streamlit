FROM python:3.9-slim

COPY . /app

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir pandas Pillow plotly streamlit openpyxl plotly

EXPOSE 8501

# ENTRYPOINT ["streamlit","run"]

CMD ["streamlit","run","layout.py"]
