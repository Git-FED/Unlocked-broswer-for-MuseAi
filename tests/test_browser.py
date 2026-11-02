import importlib.util
import tempfile
import unittest
from pathlib import Path
from urllib.parse import quote

from src.core.browser import BrowserSession


PLAYWRIGHT_AVAILABLE = importlib.util.find_spec("playwright") is not None


@unittest.skipUnless(PLAYWRIGHT_AVAILABLE, "Playwright is not installed")
class TestChromiumBrowser(unittest.TestCase):
    def test_javascript_typing_clicking_and_screenshot(self):
        html = """
        <!doctype html><title>Browser test</title>
        <input id='name'><button id='go' onclick="document.title = document.querySelector('#name').value">Go</button>
        """
        url = "data:text/html," + quote(html)
        with tempfile.TemporaryDirectory() as profile, tempfile.TemporaryDirectory() as output:
            screenshot = Path(output) / "page.png"
            with BrowserSession(user_data_dir=Path(profile), headless=True) as session:
                result = session.navigate(url)
                self.assertEqual(result.title, "Browser test")
                session.type("#name", "session-ready")
                session.click("#go")
                self.assertEqual(session.page.title(), "session-ready")
                session.screenshot(screenshot)
            self.assertTrue(screenshot.exists())
            self.assertGreater(screenshot.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
