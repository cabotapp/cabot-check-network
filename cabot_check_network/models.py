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

    # if set, this message will be sent to the server after the connection
    # is established
    message_to_send = None
    message_to_send_b64 = False

    # if set, we shall expect the server to respond with this message, for
    # the test to be considered successful
    expected_reply = None
    expected_reply_b64 = False


    # General note on the format of these messages. Typically you want to
    # send a string, but for some protocols you might want to send a binary
    # message consisting of non-printing characters. If that is your case,
    # encode the strings in base64, they will be decoded and used further
    # in the check

    def _run(self):
        result = StatusCheckResult(status_check=self)

        try:
            s = socket.create_connection((self.host, self.port), self.timeout)
        except Exception as e:
            result.error = u'Error occurred: %s' % (e.message,)
            result.succeeded = False
        else:
            # the connection was successful, refine the check by verifying
            # if there are any other success criteria and if they are satisfied


            # here we verify whether the check consists of sending a message to
            # the server or not, and whether it is a binay payload or not
            if self.message_to_send:
                if self. message_to_send_b64:
                    self.message_to_send = self.message_to_send.decode('base64')
                s.send(self.message_to_send)

            if self.expected_reply:
                if self.expected_reply_b64:
                    self.expected_reply = self.expected_reply.decode('base64')

                received_response = s.read()
                if received_response == self.expected_reply:
                    result.succeeded = True
                else:
                    result.succeeded = False

            result.succeeded = True
        finally:
            s.shutdown(socket.SHUT_RDWR)
            s.close()

        return result
