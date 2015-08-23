import unittest
import processer
import helpers

class TestUM(unittest.TestCase):

    def setUp(self):
        self.NUM_FIELDS = 5
        pass

    def test_swap(self):
        entry = ['first', 'last', 'red', '08743', '9999999999']
        swapped_entry = ['last', 'first', 'red', '08743','9999999999']
        helpers.swap(0, 1, entry)
        self.assertEqual(entry, swapped_entry)

    def test_standardize_entry(self):
        original_entry = 'Ria Tillotson, aqua marine, 97671, 196 910 5548'
        output = ['Ria', 'Tillotson', 'aquamarine', '97671', '1969105548']
        NUM_FIELDS = 5
        self.assertEqual(processer.standardize_entry(original_entry, NUM_FIELDS)
                                                    ,output)

    def test_standardize_names(self):
        original_entry = ['FirstLast', '1112223333', '09821', 'red']
        expected_output = ['First', 'Last', '1112223333', '09821', 'red']
        self.assertEqual(processer.standardize_names(original_entry),
                                                     expected_output)

    def handle_capital_names(self):
        names = ['first', 'middle', 'last']
        entry = ['first', 'middlelast', 'red', '1112223333', '09875']
        self.assertRaises(processer.handle_capital_names(names), entry)

    def test_in_first_last_name_order(self):
        entry = ['first', 'last', '9999999999','red', '09832']
        self.assertEqual(processer.in_first_last_name_order(entry), False)

    def test_parse_info(self):
        entry = ['red', '9999999999', '08743']
        output = {
          'color': 'red',
          'phonenumber': '9999999999',
          'zipcode': '08743'
        }
        self.assertEqual(processer.parse_info({}, entry), output)

    def test_parse_names(self):
        entry = ['first', 'last']
        output = {'firstname': 'first','lastname': 'last'}
        self.assertEqual(processer.parse_names({}, entry), output)

    def test_output_results(self):
        self.assertEqual(1,1)

    def test_format_user_data(self):
        data = {'firstname': 'first', 'lastname': 'last', 'zipcode': '09832', 
               'phonenumber': '1112223333'}
        formatted_phone = '111-222-3333'
        processer.format_user_data(data)
        self.assertEqual(data['phonenumber'], formatted_phone)


    def test_format_json(self):
        data = [{'firstname': 'first', 'lastname': 'last', 'zipcode': '00011', 
                'phonenumber': '111-222-3333'}]
        output = {
          'entries': [{'firstname': 'first', 'lastname': 'last', 
                       'zipcode': '00011', 
                       'phonenumber': '111-222-3333'}],
          'errors': []
        }
        self.assertEqual(processer.format_json(data), output)

if __name__ == '__main__':
    unittest.main()
