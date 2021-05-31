FROM python:3
COPY . .
RUN ls -al
RUN pip install -r requirements.txt
CMD ['python','main.py']