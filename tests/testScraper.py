import unittest
from unittest.mock import patch, MagicMock
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TestBookingComScraper(unittest.TestCase):

    @patch('selenium.webdriver.Chrome')
    def test_webdriver_initialization(self, MockWebDriver):
        # Test that the WebDriver is initialized correctly
        mock_driver = MockWebDriver.return_value
        mock_service = MagicMock()
        mock_options = MagicMock()
        
        driver = webdriver.Chrome(service=mock_service, options=mock_options)
        self.assertIsNotNone(driver)
        
        MockWebDriver.assert_called_with(service=mock_service, options=mock_options)

    @patch('selenium.webdriver.Chrome')
    def test_accept_cookies(self, MockWebDriver):
        # Simulate acceptance of cookies
        mock_driver = MockWebDriver.return_value
        mock_driver.get.return_value = None
        mock_driver.find_element_by_id.return_value.click.return_value = None
        
        # Simulate finding and clicking the reject cookies button
        mock_driver.find_element_by_id("onetrust-reject-all-handler").click()
        self.assertTrue(mock_driver.find_element_by_id("onetrust-reject-all-handler").click.called)

    @patch('selenium.webdriver.Chrome')
    def test_extract_hotel_names(self, MockWebDriver):
        # Simulate extracting hotel names
        mock_driver = MockWebDriver.return_value
        mock_elements = [MagicMock(text="Hotel A"), MagicMock(text="Hotel B")]
        mock_driver.find_elements.return_value = mock_elements

        hotel_names = set()
        for hotel in mock_driver.find_elements(By.CSS_SELECTOR, "div[data-testid='title']"):
            if hotel.text.strip():
                hotel_names.add(hotel.text.strip())

        self.assertEqual(hotel_names, {"Hotel A", "Hotel B"})

    # Add more tests as needed

if __name__ == '__main__':
    unittest.main()
