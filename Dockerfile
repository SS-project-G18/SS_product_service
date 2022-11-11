FROM python:3.8

# let's create a folder to work from 
WORKDIR /code

# copy over our requirements
COPY ./requirements.txt /code/requirements.txt

# install the python deps
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy over our source folder
COPY ./src/ /code/


CMD ["python", "uvicorn_serve.py"]