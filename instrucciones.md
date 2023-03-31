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


# Agregar los archivos sin usar --to-remote para evitar problemas con md5**
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
## Que no agregar Aun
Recordar no agregar full_data.csc a DVC, ya que aun no corresponde y de hacerlo luego en el paso de crearlo se genera un error


# Ramas creadas
git branch
git checkout -b model-revision
git checkout -b implementating_dvc
git checkout -b continuous_training_pipeline
git checkout -b testing_api
git checkout -b creating_dockerfile
git checkout -b workflow_testing_api
git checkout -b workflow_continuous_training
git checkout -b workflow_CI_CD


# Install dependencias
pip install -r requirements.txt
## banderas que se pueden usar
-q esta bandera no genera salida, por lo que no veremos los tipicos menesajes de instalacion de las dependencia, usar a criterio.
## Usar un requirement dentro de otro requirement (ejemplo)
-r api/requirements.txt


# Mejores practicas para pasar las llaves de acceso a nuestro servicio cloud (Local)
Pueden definir sus llaves en un .env y pasarlo al .gitignore asi evitan subirlas al git y no necesitan estar borrandolas, tambien pueden generar un usuario en aws que solo le den permisos sobre el bucket pero tampoco es recomendable que se suba al repositorio, esto para cuando trabajan en local.
Esto para evitar el problema que tenia el profesor que cada rato tenia que estar colocando las credenciales.
Pero usando:
"aws configure" y colocando nuestras credenciales al ser solicitadas queda configurado siempre.


# CCon esto creamos nuestro flujo continuo de entrenamiento
## con dvc run creamos un scripts
dvc run -n prepare -o dataset/full_data.csv python src/prepare.py
dvc run -n training -d dataset/full_data.csv python src/train.py
## Comandos adicionales que se usaron en esta parte
dvc repro
dvc dag


# correr servidor de uvicorn
uvicorn api.main:app


# hacer pruebas con pytest
pytest tests/tests_api.py
Aqui pidio: instalar pip install httpx, luego corri la linea anterior y funciono (yo trabaje con python 3.9.15)


# crear dockerfile de nuestra API
DOCKER_BUILDKIT=1 docker build . -t model-api:v1  (Aqui definimos la version de nuestra api)
docker run -p 8000:8000 model-api:v1


# Push al repositorio
git push origin workflow_testing_api
git push --all origin


# Crear IAM roles en AWS para los repositorios
https://www.youtube.com/watch?v=HEOU6o-Eazs
## Arreglar rol luego del video (neccesario)
https://github.com/aws-actions/configure-aws-credentials/issues/318
## Usar secretos
usar secretos de action, no el dependabot ya que no funciona ya.


# Solucion al problema de certificados al hacer push desde Ubuntu WSL2
sudo apt-get install --reinstall ca-certificates
sudo update-ca-certificates
https://stackoverflow.com/questions/35821245/github-server-certificate-verification-failed


# Creacion en AWS de lo requerido para Flujo CI/CD, no usa github action, usar google para eso
https://www.youtube.com/watch?v=NF8iZp6rqps&list=PLWQmZVQayUUI5RinDqpoIXiRYWy5YZKjs&index=4


# Documentation of IAM Permisos requeridos to CI/CD AWS FARGATE
## Permisos:
- AmazonECS_FullAccess: Este permiso lo agregue ya que no me permitia el paso (Deploy Amazon ECS task definition)
- AmazonS3FullAccess: Este permiso lo agregue para tener acceso al S3 que defini
- Me parece bien, que partiendo de estos dos, permisor, ir contruyendo mi proxima flujo con un proyecto de clasificacion, y probar en definitiva, cueal otro permiso requiero, pero posiblemente falte el del task y ECR


# Documentation Actions secrets and variables (No pasar espacios o lineas en blanco no requeridas)
- AWS_IAM_ROLE:
Aqui va el ARN de tu Rol usar.
- AWS_REGION:
Aqui se recomienda usar una sola ubicacion por ejemplo(us-east-2 o us-east-1), el rol no tiene ubicacion ya que es global, asi que estar pendiente al cambiar de esta ventana a otras ya que puede cambiar a la primera que es us-east-1, y confundirte en la creacion de todo lo demas. 

- ECR_REGISTRY:
Este es un valor que proviene de la union del ID de tu cuenta, la region usada para loguear y un link web de ECR. Por lo tanto, puede ser obtenido del paso en que logueamos ECR (metodo usado) o simplemente colocandolo con codigo duro.

- ECR_REPOSITORY:
Este es el nombre del repositorio ECR que creamos.

- ECS_CLUSTER:
Nombre del cluster

- ECS_CONTAINER_NAME:
nombre que le dimos al contenedor al crear la tarea

- ECS_SERVICE:
nombre del servicio

- ECS_TASK_DEFINITION:
Definición de tarea mas su revisión
ejemplo: tarea-ejemplo:1 tarea-ejemplo:2


# Readme documentation of project
Buena documentacion, adaptar con esta:
https://github.com/ahmednkhan24/AWS-ECS-Pipeline