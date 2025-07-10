from osbot_utils.helpers.safe_str.Safe_Str__File__Path import Safe_Str__File__Path
from osbot_utils.utils.Dev import pprint

import genai_agent_gdpr_compliance
from unittest                                                        import TestCase
from osbot_utils.utils.Files                                         import folder_name, parent_folder, folder_exists, file_name, file_exists
from genai_agent_gdpr_compliance.deploy.AWS__Deploy__GDPR_Compliance import AWS__Deploy__GDPR_Compliance, \
    FOLDER__GDPR_COMPLIANCE__NO_CODE_DEV, Schema__GDPR_Compliance__No_Code_Dev__Files_To_Deploy


class test_AWS__Deploy__GDPR_Compliance(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.aws_deploy = AWS__Deploy__GDPR_Compliance()

    def test__init__(self):
        with self.aws_deploy as _:
            assert type(_) is AWS__Deploy__GDPR_Compliance

    def test_no_code_dev__files_to_copy(self):
        with self.aws_deploy.no_code_dev__files_to_copy() as _:
            assert type(_) is Schema__GDPR_Compliance__No_Code_Dev__Files_To_Deploy
            assert _.folder__local_root == Safe_Str__File__Path(genai_agent_gdpr_compliance.path + f'/{FOLDER__GDPR_COMPLIANCE__NO_CODE_DEV}')
            assert _.files__no_code_dev == ['2025/07/04/claude__gdpr-compliance-assistant.html']

    def test_no_code_dev__folder__full_path(self):
        with self.aws_deploy as _:
            full_path = _.no_code_dev__folder__full_path()
            assert folder_name  (full_path) == FOLDER__GDPR_COMPLIANCE__NO_CODE_DEV
            assert parent_folder(full_path) == genai_agent_gdpr_compliance.path
            assert folder_exists(full_path) is True

    def test_s3__copy_files__no_code_dev(self):
        with self.aws_deploy as _:
            files_to_copy      = _.no_code_dev__files_to_copy()
            local__root_folder = files_to_copy.folder__local_root
            upload_result      = _.s3__copy_files__no_code_dev()
            assert upload_result == [{ 'local__file_path': f'{local__root_folder}/2025/07/04/claude__gdpr-compliance-assistant.html',
                                       's3__file_path'   : 'no-code-dev/2025/07/04/claude__gdpr-compliance-assistant.html'                      ,
                                       'upload_status'   : True                                                                                 }]

            # trigger cache invalidation
            _.cloud_front__invalidate_paths()

    def test_cloud_front__invalidate_paths(self):
        with self.aws_deploy as _:
            result = _.cloud_front__invalidate_paths()
            pprint(result)
