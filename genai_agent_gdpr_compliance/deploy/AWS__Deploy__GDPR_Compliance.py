from osbot_aws.aws.cloud_front.Cloud_Front import Cloud_Front
from osbot_utils.decorators.methods.cache_on_self import cache_on_self

import genai_agent_gdpr_compliance
from os.path                                                        import relpath
from typing                                                         import List
from osbot_utils.helpers.safe_str.Safe_Str__File__Path              import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.utils.Files                                        import path_combine, files_list, files_recursive, file_exists
from osbot_utils.utils.Http                                         import url_join_safe
from genai_agent_gdpr_compliance.deploy.AWS__Setup__GDPR_Compliance import AWS__Setup__GDPR_Compliance

FOLDER__GDPR_COMPLIANCE__NO_CODE_DEV = 'no-code-dev'
CLOUD_FRONT__DISTRIBUTION_ID         = 'E2C4SBV6XN6T3C'                 # todo: move to .env var

class Schema__GDPR_Compliance__No_Code_Dev__Files_To_Deploy(Type_Safe):
    folder__local_root: Safe_Str__File__Path
    files__no_code_dev: List[Safe_Str__File__Path]

class AWS__Deploy__GDPR_Compliance(Type_Safe):
    aws_setup : AWS__Setup__GDPR_Compliance

    @cache_on_self
    def cloud_front(self):
        return Cloud_Front()

    def cloud_front__distribution_id(self):
        return CLOUD_FRONT__DISTRIBUTION_ID

    def cloud_front__invalidate_paths(self):
        distribution_id    = self.cloud_front__distribution_id()
        path_to_invalidate = '/*'
        return self.cloud_front().invalidate_paths(distribution_id=distribution_id, paths= [path_to_invalidate])

    def no_code_dev__folder__full_path(self):
        folder_name = FOLDER__GDPR_COMPLIANCE__NO_CODE_DEV
        repo_path   =  genai_agent_gdpr_compliance.path
        full_path   = path_combine(repo_path, folder_name)
        return full_path

    def no_code_dev__files_to_copy(self) -> Schema__GDPR_Compliance__No_Code_Dev__Files_To_Deploy:
        local_root = self.no_code_dev__folder__full_path()
        with (Schema__GDPR_Compliance__No_Code_Dev__Files_To_Deploy() as _):
            _.folder__local_root =  self.no_code_dev__folder__full_path()
            for file_path in files_list(local_root):
                virtual_path = relpath(file_path, _.folder__local_root)
                _.files__no_code_dev.append(Safe_Str__File__Path(virtual_path))
            return _

    def s3(self):
        return self.aws_setup.s3()

    def s3__copy_files__no_code_dev(self):
        s3_bucket          = self.aws_setup.s3__bucket__name()
        s3_root_folder     = self.s3__folder__no_code_dev()
        files_to_copy      = self.no_code_dev__files_to_copy()
        local__root_folder = files_to_copy.folder__local_root
        files_copied       = []
        for file_to_copy in files_to_copy.files__no_code_dev:
            local__file_path = path_combine(local__root_folder, file_to_copy)
            s3__file_key     = url_join_safe(s3_root_folder, file_to_copy)
            if file_exists(local__file_path):
                kwargs        = dict(file             = local__file_path,
                                     bucket           = s3_bucket    ,
                                     key              = s3__file_key ,
                                     set_content_type = True         )
                upload_status =  self.s3().file_upload_to_key(**kwargs)
                file_copied = dict(local__file_path = local__file_path,
                                   s3__file_path    = s3__file_key    ,
                                   upload_status    = True            )
                files_copied.append(file_copied)
        return files_copied

    def s3__folder__no_code_dev(self):
        return FOLDER__GDPR_COMPLIANCE__NO_CODE_DEV
