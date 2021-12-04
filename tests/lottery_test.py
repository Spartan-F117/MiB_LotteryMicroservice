import unittest

class LotteryTest(unittest.TestCase):
    """
    This class should be implemented by
    all classes that tests resources
    """
    lottery = None

    @classmethod

    def setUpClass(self):
        from mib import create_app
        app = create_app()
        from mib import create_celery
        celery = create_celery()
        self.lottery = app.test_client()
    
    def test_join_lottery(self):
        payload = dict(id='1')
        
        response = self.lottery.post("/join_lottery",json=payload)

        assert response.status_code == 201

    def test_z_is_partecipant(self):
        payload = dict(id='1')

        response = self.lottery.post("/is_participant",json=payload)

        assert response.status_code == 201

    def test_z_is_partecipant_without_correct_user_id(self):
        payload = dict(id='2')

        response = self.lottery.post("/is_participant",json=payload)

        assert response.status_code == 202