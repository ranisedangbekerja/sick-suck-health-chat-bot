import unittest
from ssh import chatbot_response

class TestChatbot(unittest.TestCase):

    def setUp(self):
        self.user_id = "testuser"

    def test_greeting(self):
        response = chatbot_response(self.user_id, "Halo")
        self.assertIn("selamat", response.lower())
        self.assertIn("diet", response.lower())

    def test_diet_choice(self):
        chatbot_response(self.user_id, "Halo")
        response = chatbot_response(self.user_id, "Diet")
        self.assertIn("menu harian sehat", response.lower())

    def test_diet_followup(self):
        chatbot_response(self.user_id, "Halo")
        chatbot_response(self.user_id, "Diet")
        response = chatbot_response(self.user_id, "ya")
        self.assertIn("minuman sehat", response.lower())

    def test_workout_choice(self):
        chatbot_response(self.user_id, "Halo")
        response = chatbot_response(self.user_id, "Latihan")
        self.assertIn("jadwal latihan", response.lower())

    def test_workout_followup(self):
        chatbot_response(self.user_id, "Halo")
        chatbot_response(self.user_id, "Latihan")
        response = chatbot_response(self.user_id, "lanjut")
        self.assertIn("pemanasan", response.lower())

    def test_relaxation_choice(self):
        chatbot_response(self.user_id, "Halo")
        response = chatbot_response(self.user_id, "Relaksasi")
        self.assertIn("tarik napas", response.lower())

    def test_relaxation_followup(self):
        chatbot_response(self.user_id, "Halo")
        chatbot_response(self.user_id, "Relaksasi")
        response = chatbot_response(self.user_id, "boleh")
        self.assertIn("relaksasi", response.lower())

    def test_fallback(self):
        response = chatbot_response(self.user_id, "asdfgh")
        self.assertIn("pilih salah satu", response.lower())

if __name__ == "__main__":
    unittest.main()
