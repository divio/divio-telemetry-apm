from functools import partial
from aldryn_client import forms


class Form(forms.BaseForm):
    def check_threads(self):
        try:
            import threading  # NOQA
        except ImportError:
            from django.core.exceptions import ImproperlyConfigured
            raise ImproperlyConfigured(
                "Threads are required for divio-telemetry-apm. "
                "Are they enabled?"
            )

    def configure_django(self, settings, env):
        settings['INSTALLED_APPS'].append('elasticapm.contrib.django')

        key = 'MIDDLEWARE'
        if 'MIDDLEWARE_CLASSES' in settings:
            key = 'MIDDLEWARE_CLASSES'
        settings[key].insert(
            0, 'elasticapm.contrib.django.middleware.TracingMiddleware'
        )

    def configure_elastic_apm(self, settings, env):
        from aldryn_addons.utils import boolean_ish
        import yurl
        elastic_dsn = yurl.URL(env('DEFAULT_APM_DSN'))

        if elastic_dsn:
            service_name = elastic_dsn.username
            secret_token = elastic_dsn.authorization
            server_url = str(elastic_dsn.replace(userinfo=''))

            server_env = env('STAGE', 'local').lower()
            if server_env in {'live', }:
                elastic_send_debug = False
            else:
                elastic_send_debug = True
            elastic_send_debug = boolean_ish(env('ELASTIC_SEND_DEBUG',
                                                 elastic_send_debug))

            elastic_service_name = '{}-{}'.format(service_name, server_env)
            elastic_service_name = env('ELASTIC_SERVICE_NAME',
                                       elastic_service_name)

            settings['ELASTIC_APM'] = {
                'DEBUG': elastic_send_debug,
                'SERVER_URL': server_url,
                'SERVICE_NAME': elastic_service_name,
                'SECRET_TOKEN': secret_token,
            }

    def configure_elastic_logging(self, settings, env):
        from aldryn_addons.utils import boolean_ish
        enable_elastic_logging = boolean_ish(env('ENABLE_ELASTIC_LOGGING',
                                                 False))
        if enable_elastic_logging:
            log_level = env('ELASTIC_LOG_LEVEL', 'INFO').upper()
            settings['LOGGING']['handlers'].update({
                'elasticapm': {
                    'level': log_level,
                    'class': 'elasticapm.contrib.django.handlers.LoggingHandler',
                }
            })
            for k in settings['LOGGING']['loggers']:
                settings['LOGGING']['loggers'][k]['handlers'].append(
                    'elasticapm')

    def to_settings(self, data, settings):
        from aldryn_addons.utils import boolean_ish, djsenv
        env = partial(djsenv, settings=settings)
        enable_elastic_apm = boolean_ish(env('ENABLE_ELASTIC_APM', True))
        enable_elastic_apm = True

        if enable_elastic_apm:
            self.check_threads()
            self.configure_django(settings, env=env)
            self.configure_elastic_apm(settings, env=env)
            self.configure_elastic_logging(settings, env=env)

        return settings
