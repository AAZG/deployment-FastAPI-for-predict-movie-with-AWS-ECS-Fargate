FROM python:3.9.15-slim-buster

WORKDIR /app

COPY api/requirements.txt .

RUN python -m pip install --upgrade pip

ENV PIP_ROOT_USER_ACTION=ignore

RUN pip install --root-user-action=ignore -U pip && pip install --root-user-action=ignore -r requirements.txt

COPY api/ ./api

COPY model/model.pkl ./model/model.pkl

COPY initializer.sh .

RUN chmod +x initializer.sh

EXPOSE 8000

ENTRYPOINT ["./initializer.sh"]