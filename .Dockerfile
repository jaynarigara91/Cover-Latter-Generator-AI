FROM python:3.10.15
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 1000
CMD ["streamlit","run","main.py"]
