import genai_agent_gdpr_compliance
from unittest                      import TestCase
from osbot_utils.utils.Files       import parent_folder, file_name
from genai_agent_gdpr_compliance.utils.Version        import Version, version__genai_agent_gdpr_compliance


class test_Version(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.version = Version()

    def test_path_code_root(self):
        assert self.version.path_code_root() == genai_agent_gdpr_compliance.path

    def test_path_version_file(self):
        with self.version as _:
            assert parent_folder(_.path_version_file()) == genai_agent_gdpr_compliance.path
            assert file_name    (_.path_version_file()) == 'version'

    def test_value(self):
        assert self.version.value() == version__genai_agent_gdpr_compliance