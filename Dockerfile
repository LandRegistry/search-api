# Set the base image to the base image
FROM hmlandregistry/dev_base_python_flask:3

RUN yum install -y postgresql-devel

ENV APP_NAME="search-api" \
    SQL_HOST="postgres" \
    LOG_LEVEL="DEBUG" \
    COMMIT="LOCAL" \
    SQL_DATABASE="search_api_db" \
    SQL_PASSWORD="password" \
    APP_SQL_USERNAME="search_api_db_user" \
    ALEMBIC_SQL_USERNAME="alembic_user" \
    SQL_USE_ALEMBIC_USER="false" \
    ADDRESS_API_URL="http://address-api:8080" \
    INDEX_MAP_API_URL="http://index-map-api:8080" \
    MAX_HEALTH_CASCADE=6 \
    FEEDER_SQL_USERNAME="maintain_feeder_user" \
    FEEDER_SQL_PASSWORD="password" \
    AUTHENTICATION_API_URL="http://authentication-api:8080/v2.0" \
    AUTHENTICATION_API_ROOT="http://authentication-api:8080" \
    ACCTEST_SQL_USERNAME="acceptance_test_user" \
    ACCTEST_SQL_PASSWORD="password" \
    REPORT_API_SQL_USERNAME="report_api_user" \
    REPORT_API_SQL_PASSWORD="password" \
    SQLALCHEMY_POOL_RECYCLE="3300"

ADD requirements_test.txt requirements_test.txt
ADD requirements.txt requirements.txt

RUN pip3 install -q -r requirements.txt && \
    pip3 install -q -r requirements_test.txt
