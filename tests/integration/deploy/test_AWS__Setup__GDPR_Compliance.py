from unittest import TestCase

from genai_agent_gdpr_compliance.deploy.AWS__Setup__GDPR_Compliance import AWS__Setup__GDPR_Compliance


class test_AWS__Setup__GDPR_Compliance(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.aws_setup = AWS__Setup__GDPR_Compliance()


    def test__init__(self):
        with self.aws_setup as _:
            assert type(_) is AWS__Setup__GDPR_Compliance