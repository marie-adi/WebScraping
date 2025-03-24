import unittest
from unittest.mock import patch, MagicMock
from ScraperPoo.py import HotelScraper

class TestHotelScraper(unittest.TestCase):

    @patch('ScraperPoo.webdriver.Chrome')
    def test_setup_driver(self, mock_chrome):
        scraper = HotelScraper()
        scraper.setup_driver()
        mock_chrome.assert_called_once()

    def test_clean_hotel_name(self):
        scraper = HotelScraper()
        result = scraper.clean_hotel_name("Hôtel de Ville")
        expected = {
            'original_name': "Hôtel de Ville",
            'cleaned_name': "hotel de ville",
            'name_length': 13
        }
        self.assertEqual(result, expected)

    @patch('ScraperPoo.webdriver.Chrome')
    def test_reject_cookies(self, mock_chrome):
        scraper = HotelScraper()
        scraper.driver = MagicMock()
        scraper.reject_cookies()
        scraper.driver.find_element.assert_called_with(By.ID, 'onetrust-reject-all-handler')

    @patch('ScraperPoo.webdriver.Chrome')
    def test_load_all_hotels(self, mock_chrome):
        scraper = HotelScraper()
        scraper.driver = MagicMock()
        scraper.load_all_hotels("http://example.com")
        scraper.driver.get.assert_called_with("http://example.com")

    @patch('ScraperPoo.webdriver.Chrome')
    def test_extract_hotel_names(self, mock_chrome):
        scraper = HotelScraper()
        scraper.driver = MagicMock()
        scraper.driver.find_elements.return_value = [MagicMock(text="Hotel One"), MagicMock(text="Hotel Two")]
        result = scraper.extract_hotel_names()
        expected = [
            {'original_name': 'Hotel One', 'cleaned_name': 'hotel one', 'name_length': 9},
            {'original_name': 'Hotel Two', 'cleaned_name': 'hotel two', 'name_length': 9}
        ]
        self.assertEqual(result, expected)

    @patch('ScraperPoo.webdriver.Chrome')
    def test_save_hotel_data(self, mock_chrome):
        scraper = HotelScraper()
        hotel_names = [
            {'original_name': 'Hotel One', 'cleaned_name': 'hotel one', 'name_length': 9},
            {'original_name': 'Hotel Two', 'cleaned_name': 'hotel two', 'name_length': 9}
        ]
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            scraper.save_hotel_data(hotel_names)
            mock_file.assert_any_call("hoteles.txt", "w", encoding="utf-8")
            mock_file.assert_any_call("hoteles.json", "w", encoding="utf-8")

if __name__ == '__main__':
    unittest.main()