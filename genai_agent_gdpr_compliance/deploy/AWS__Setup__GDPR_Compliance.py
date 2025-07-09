from osbot_aws.AWS_Config                           import AWS_Config
from osbot_aws.aws.s3.S3                            import S3
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.type_safe.Type_Safe                import Type_Safe

#dns_entry                    = 'https://gdpr-compliance.dev.aws.cyber-boardroom.com'       # todo: add workflow to set this up (note the hosted zone for dev.aws.cyber-boardroom.com is already configured in the 654654216424 aws account)

GDPR_COMPLIANCE__PROJECT_NAME = "gdpr-compliance"

class AWS__Setup__GDPR_Compliance(Type_Safe):

    @cache_on_self
    def s3(self):
        return S3()

    @cache_on_self
    def aws_config(self):
        return AWS_Config()

    def aws__account_id(self):
        return self.aws_config().account_id()

    def aws__configured(self):
        return self.aws_config().aws_configured()

    def aws__region_name(self):
        return self.aws_config().region_name()

    def s3__bucket__name(self):
        return f"{GDPR_COMPLIANCE__PROJECT_NAME}--{self.aws__account_id()}--{self.aws__region_name()}"

    def s3__bucket__exists(self):
        return self.s3().bucket_exists(self.s3__bucket__name())