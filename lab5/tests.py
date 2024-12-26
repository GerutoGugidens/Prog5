import time
import unittest
from main import Currency

class TestCurrency(unittest.TestCase):
    def test_get_currencies_valid_ids(self):
        currency = Currency()
        currency.set_valutes(["USD", "EUR"])
        time.sleep(2)
        rates = currency.get_currencies()
        self.assertIsNotNone(rates)
        self.assertEqual(len(rates), 2)
        usd_info = rates[0]["USD"]
        eur_info = rates[1]["EUR"]
        self.assertEqual("Доллар США", usd_info[0])
        self.assertGreater(float(usd_info[1].replace(',','.')), 0)
        self.assertEqual("Евро", eur_info[0])
        self.assertGreater(float(eur_info[1].replace(',','.')), 0)

    def test_get_currencies_invalid_id(self):
        currency = Currency()
        time.sleep(2)
        currency.set_valutes(["sdgirjt"])
        rates = currency.get_currencies()
        self.assertEqual(rates, [])

    def test_plot_currencies(self):
        currency = Currency()
        time.sleep(2)
        currency.set_valutes(["USD", "EUR"])
        rates = currency.get_currencies()

        self.assertTrue(currency.plot_currencies())  # Просто проверка, что график создается без ошибок

if __name__ == '__main__':
    unittest.main()