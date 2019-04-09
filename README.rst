*******************
Divio Telemetry APM
*******************

Setup
#####

Head over to elastic.co and signup for an APM instance. 

Configuration
#############

Following environment variables are available for configuration

``DEFAULT_APM_DSN`` (should look like ``https://myapp:SECRET_TOKEN@ELASTIC_HOSTNAME.co:443``)

``ENABLE_ELASTIC_APM`` (default ``True``)

``ENABLE_ELASTIC_LOGGING`` (default ``False``)

``ELASTIC_LOG_LEVEL`` (default ``INFO``)

``ELASTIC_SEND_DEBUG`` (default ``True`` for local & test servers)

``ELASTIC_SERVICE_NAME`` 

