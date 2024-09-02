# Unit Test Build
echo "######  Unit Test Container Build   ##############"
echo "ENV COMPOSE_PROFILES=test" >> docker/Dockerfile-test

docker build -t housing-test -f docker/Dockerfile-test .

docker run -d \
  --name housing-unit-tests \
  housing-test

sed -i '' '/^ENV/d' docker/Dockerfile-test 



## DB Build
echo "######  DB Container Build   ##############"
docker/docker-setup.sh docker/.env/.postgres docker/Dockerfile-db
docker build -t housing-db -f docker/Dockerfile-db .

docker run -d \
  --name sampledb \
  -p 5432:5432 \
  housing-db

sed -i '' '/^ENV/d' docker/Dockerfile-db


## Migration Build
echo "######  Migration Container Build   ##############"
docker/docker-setup.sh docker/.env/.flyway docker/Dockerfile-migration

echo "ENV FLYWAY_DEFAULT_SCHEMA=housing" >> docker/Dockerfile-migration

docker build -t housing-migration -f docker/Dockerfile-migration .

docker run --rm \
  --name housing-migration \
  housing-migration \

sed -i '' '/^ENV/d' docker/Dockerfile-migration



## API Build
echo "######  API Container Build   ##############"
docker/docker-setup.sh docker/.env/.python docker/Dockerfile-api
docker/docker-setup.sh docker/.env/.postgres docker/Dockerfile-api

docker build -t housing-api -f docker/Dockerfile-api .

docker run -d \
  --name housing-api \
  -p 3003:3000 \
  housing-api

sed -i '' '/^ENV/d' docker/Dockerfile-api