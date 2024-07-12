import unittest
from datetime import datetime
from modules.main_funcs import check_date


def get_time():
    return datetime.now().strftime('%d.%m.%Y')


class TestCheckDateFunction(unittest.TestCase):
    def test1(self):
        self.assertEqual(check_date("1234"), get_time(), "Test 1")

    def test2(self):
        self.assertEqual(check_date("11.11.1111"), "11.11.1111", "Test 2")

    def test3(self):
        self.assertEqual(check_date("99.999.9999"), get_time(), "Test 3")

    def test4(self):
        self.assertEqual(check_date("1111.11.11"),  "11.11.1111", "Test 4")

    def test5(self):
        self.assertEqual(check_date("1111/11/11"),  "11.11.1111", "Test 5")

    def test6(self):
        self.assertEqual(check_date("1111/11,11"),  "11.11.1111", "Test 6")

    def test7(self):
        self.assertEqual(check_date("1111,11,11"),  "11.11.1111", "Test 7")

    def test8(self):
        self.assertEqual(check_date("11/11/1111"), "11.11.1111", "Test 8")

    def test9(self):
        self.assertEqual(check_date("11,11,1111"), "11.11.1111", "Test 9")

    def test10(self):
        self.assertEqual(check_date("11 11 1111"), "11.11.1111", "Test 10")

    def test11(self):
        self.assertEqual(check_date("11/11/11"), "11.11.2011", "Test 11")

    def test12(self):
        self.assertEqual(check_date("11.11"), get_time(), "Test 12")

    def test13(self):
        self.assertEqual(check_date("11/11"), get_time(), "Test 13")

    def test14(self):
        self.assertEqual(check_date("11.11.11"), "11.11.2011", "Test 14")

    def test15(self):
        self.assertEqual(check_date("11 11 11"), "11.11.2011", "Test 15")

    def test16(self):
        self.assertEqual(check_date("2020/02/29"), "29.02.2020", "Test 16")

    def test17(self):
        self.assertEqual(check_date("2020-02-29"), get_time(), "Test 17")

    def test18(self):
        self.assertEqual(check_date("29/02/2020"), "29.02.2020", "Test 18")

    def test19(self):
        self.assertEqual(check_date("29,02,2020"), "29.02.2020", "Test 19")

    def test20(self):
        self.assertEqual(check_date("  29.02.2020  "), "29.02.2020", "Test 20")

    def test21(self):
        self.assertEqual(check_date("31.04.2020"), get_time(), "Test 21")

    def test22(self):
        self.assertEqual(check_date("29.02.2019"), get_time(), "Test 22")

    def test23(self):
        self.assertEqual(check_date("2019.02.29"), get_time(), "Test 23")

    def test24(self):
        self.assertEqual(check_date("29.02.2021"), get_time(), "Test 24")

    def test25(self):
        self.assertEqual(check_date("00.00.0000"), get_time(), "Test 25")

    def test26(self):
        self.assertEqual(check_date("0000.00.00"), get_time(), "Test 26")

    def test27(self):
        self.assertEqual(check_date("31.12.2020"), "31.12.2020", "Test 27")

    def test28(self):
        self.assertEqual(check_date("32.01.2020"), get_time(), "Test 28")

    def test29(self):
        self.assertEqual(check_date("01.13.2020"), get_time(), "Test 29")

    def test30(self):
        self.assertEqual(check_date("01.00.2020"), get_time(), "Test 30")

    def test31(self):
        self.assertEqual(check_date("00.01.2020"), get_time(), "Test 31")

    def test32(self):
        self.assertEqual(check_date("31.09.2020"), get_time(), "Test 32")

    def test33(self):
        self.assertEqual(check_date("2020.09.31"), get_time(), "Test 33")

    def test34(self):
        self.assertEqual(check_date("01 01 2020"), "01.01.2020", "Test 34")

    def test35(self):
        self.assertEqual(check_date("31 12 1999"), "31.12.1999", "Test 35")

    def test36(self):
        self.assertEqual(check_date("29 02 2020"), "29.02.2020", "Test 36")

    def test37(self):
        self.assertEqual(check_date("29 02 2019"), get_time(), "Test 37")

    def test38(self):
        self.assertEqual(check_date("29/02/19"), "19.02.2029", "Test 38")

    def test39(self):
        self.assertEqual(check_date("2020/29/02"), get_time(), "Test 39")

    def test40(self):
        self.assertEqual(check_date("2020.29.02"), get_time(), "Test 40")

    def test41(self):
        self.assertEqual(check_date("Feb 29, 2020"), get_time(), "Test 41")

    def test42(self):
        self.assertEqual(check_date("2020/Feb/29"), get_time(), "Test 42")

    def test43(self):
        self.assertEqual(check_date("2020/2/29"), "29.2.2020", "Test 43")

    def test44(self):
        self.assertEqual(check_date("02/29/2020"), get_time(), "Test 44")

    def test45(self):
        self.assertEqual(check_date("February 29, 2020"), get_time(), "Test 45")

    def test46(self):
        self.assertEqual(check_date("29 Feb 2020"), get_time(), "Test 46")

    def test47(self):
        self.assertEqual(check_date("2020 Feb 29"), get_time(), "Test 47")

    def test48(self):
        self.assertEqual(check_date("2020.2.29"), "29.2.2020", "Test 48")

    def test49(self):
        self.assertEqual(check_date("2.29.2020"), get_time(), "Test 49")

    def test50(self):
        self.assertEqual(check_date("2020.02.29"), "29.02.2020", "Test 50")


if __name__ == '__main__':
    unittest.main()
