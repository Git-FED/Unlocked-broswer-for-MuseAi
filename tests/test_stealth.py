import unittest
from unittest.mock import patch

from src.network.proxy import ProxyPool
from src.stealth.fingerprint import ClientProfile
from src.stealth.human import polite_delay


class TestAuthorizedClientHelpers(unittest.TestCase):
    def test_profile_is_stable_and_descriptive(self):
        profile = ClientProfile(name="test-client", version="1.2", platform="test-os")
        self.assertIn("test-client/1.2", profile.user_agent)
        self.assertIn("test-os", profile.user_agent)

    def test_proxy_pool_cycles_configured_values(self):
        pool = ProxyPool(["http://one", "", "http://two"])
        self.assertEqual(pool.next(), "http://one")
        self.assertEqual(pool.next(), "http://two")
        self.assertEqual(pool.next(), "http://one")

    def test_empty_proxy_pool_returns_none(self):
        self.assertIsNone(ProxyPool([]).next())

    @patch("src.stealth.human.time.sleep")
    @patch("src.stealth.human.random.uniform", return_value=0.75)
    def test_polite_delay_is_bounded(self, uniform, sleep):
        self.assertEqual(polite_delay(0.5, 1.0), 0.75)
        uniform.assert_called_once_with(0.5, 1.0)
        sleep.assert_called_once_with(0.75)


if __name__ == "__main__":
    unittest.main()
