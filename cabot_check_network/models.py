import socket

from django.db import models

from cabot.cabotapp.models import StatusCheck, StatusCheckResult


class NetworkStatusCheck(StatusCheck):
    check_name = 'network'
    edit_url_name = 'update-network-check'
    duplicate_url_name = 'duplicate-network-check'
    icon_class = 'glyphicon-transfer'
    host = models.TextField(
        help_text='Host to check.',
    )
    port = models.PositiveIntegerField(
        help_text='Port to check.',
    )

    def _run(self):
        result = StatusCheckResult(status_check=self)

        try:
            s = socket.create_connection((self.host, self.port), self.timeout)
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        except Exception as e:
            result.error = u'Error occurred: %s' % (e.message,)
            result.succeeded = False
        else:
            result.succeeded = True

        return result
