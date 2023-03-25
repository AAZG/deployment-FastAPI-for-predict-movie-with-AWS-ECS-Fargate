# Pasos para DVC
https://iterative.ai/blog/aws-remotes-in-dvc/  # aguide add remote to AWS s3

pyenv install 3.9.15 #using pyenv for install varias vertions of python in your ubuntu with WSL2
makeproject (your name enviroments) --python (your version python) #using pipenvwrapper for create y managements for multics enviroments
useenv (select your enviroments create previus)
pip install 'dvc[s3]'
sudo apt install awscli
aws configure # Agregate credentials in rootkey.csv for AWS s3
*Create folders ['model', 'dataset'] in web of AWS s3*
dvc remote add -d -f model-tracker s3://model-dataset-tracker-cursemlops/model
dvc remote add -d -f dataset-track s3://model-dataset-tracker-cursemlops/dataset


# Agregar los archivos sin usar --to-remote para evitar problemas con md5
## paso 1
dvc add dataset/finantials.csv
dvc add dataset/opening_gross.csv
dvc add dataset/movies.csv
dvc add model/model.pkl

## paso 2
dvc push dataset/finantials.csv -r dataset-track
dvc push dataset/opening_gross.csv -r dataset-track
dvc push dataset/movies.csv -r dataset-track
dvc push model/model.pkl -r model-track


# Ramas creadas
git branch
git checkout -b model-revision
git checkout -b implementating_dvc
git checkout -b continuous_training_pipeline
git checkout -b testing_api
git checkout -b creating_dockerfile
git checkout -b workflow_testing_api


# Install
pip install -r requirements.txt

#
Pueden definir sus llaves en un .env y pasarlo al gitignore asi evitan subirlas al git y no necesitan estar borrandolas, tambien pueden generar un usuario en aws que solo le den permisos sobre el bucket


# con esto creamos nuestro flujo continuo de entrenamiento
## con dvc run creamos un scripts
dvc run -n prepare -o dataset/full_data.csv python src/prepare.py
dvc run -n training -d dataset/full_data.csv python src/train.py

dvc repro
dvc dag


# correr servidor de uvicorn
uvicorn api.main:app

# hacer pruebas con pytest
pytest tests/tests_api.py
Aqui pidio: instalar pip install httpx, luego corri la linea anterior y funciono


# crear dockerfile
DOCKER_BUILDKIT=1 docker build . -t model-api:v1
docker run -p 8000:8000 model-api:v1


# Push al repositorio
git push origin workflow_testing_api
git push --all origin


# Crear IAM roles en AWS para los repositorios
https://www.youtube.com/watch?v=HEOU6o-Eazs