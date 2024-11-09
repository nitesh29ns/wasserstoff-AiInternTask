FROM python:3.12.0

WORKDIR /app

COPY . ./

ADD domain_keywords_obj.pkl domain_keywords_obj.pkl
ADD stop_word_obj.pkl stop_word_obj.pkl

RUN pip install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"] 