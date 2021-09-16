#from fabric.api import settings, run, get, put
from fabric import Connection,Config
import logging

progress_log = logging.getLogger("progress")
class RunCmdError(Exception):
    pass


class Machine(object):
    """"""

    def __init__(self, host_string, host_user, host_passwd):
        self.host_string = host_string
        self.host_user = host_user
        self.host_passwd = host_passwd

        self.config = Config(overrides={'user': self.host_user, 'connect_kwargs': {'password': self.host_passwd}})
        self.cxn = Connection(host=self.host_string, config=self.config, connect_timeout=120)

    def execute(self, cmd, timeout=60, raise_exception=True):
        # with settings(
        #         host_string=self.host_string,
        #         user=self.host_user,
        #         password=self.host_passwd,
        #         disable_known_hosts=True,
        #         connection_attempts=60):
        #     ret = run(cmd, quiet=True, timeout=timeout)

        try:
            ret = self.cxn.run(cmd, hide=True)
            if ret.ok:
                progress_log.info('Run cmd "%s" succeeded', cmd)
                return True, ret.stdout.strip()
            else:
                progress_log.error('Run cmd "%s" failed, ret is "%s"', cmd, ret)
                return False, ret.stdout.strip()
        except Exception as e:
            progress_log.error('Run cmd "%s" failed with exception "%s"', cmd, e)
            return False, e

    def get_file(self, src_path, dst_path):
        # with settings(
        #         host_string=self.host_string,
        #         user=self.host_user,
        #         password=self.host_passwd,
        #         disable_known_hosts=True,
        #         connection_attempts=120):
        #     ret = get(src_path, dst_path)
        #     if not ret.succeeded:
        #         raise RunCmdError(
        #             "ERR: Get file {} to {} failed".format(src_path, dst_path))

        try:
            ret = self.cxn.get(src_path, dst_path)

        except Exception as e:
            progress_log.error("Can't get {} from remote server:{}.".format(
                src_path, self.host_string))

    def put_file(self, src_path, dst_path):
        # with settings(
        #         host_string=self.host_string,
        #         user=self.host_user,
        #         password=self.host_passwd,
        #         disable_known_hosts=True,
        #         connection_attempts=120):
        #     ret = put(src_path, dst_path)
        #     if not ret.succeeded:
        #         raise RunCmdError(
        #             "ERR: Put file {} to {} failed".format(src_path, dst_path))

        try:
            ret = self.cxn.put(src_path, dst_path)
            
        except Exception as e:
            progress_log.error("Can't put {} to remote server:{}.".format(
                src_path, self.host_string))
