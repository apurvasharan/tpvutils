#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os, sys, traceback
from optparse import OptionParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0


URL = "http://anonimize.be.s3-website-eu-west-1.amazonaws.com/"

class wait_for_element_non_empty (object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            element_text = EC._find_element(driver, self.locator).text

            if len (element_text.strip ()) is not 0:
                return True
            else:
                return False
        except StaleElementReferenceException:
            return False

def main ():
    parser = OptionParser()
    parser.add_option("-s", "--serialnum", dest="serial", help="Serial Number of set")
    parser.add_option("-m", "--macaddr", dest="macaddr", help="Mac address of the set")
    parser.add_option("-d", "--deviceid", dest="deviceid", help="Device id of the set")

    (options, args) = parser.parse_args ()

    if (options.serial is not None) or (options.macaddr is not None) or (options.deviceid is not None):
        driver = webdriver.PhantomJS ()
        driver.get (URL)
    else:
        parser.print_help ()
        exit (0)


    if options.serial is not None:
        driver.find_element_by_id ("sn").send_keys (options.serial)
        driver.find_element_by_xpath ('//*[@id="main"]/div/table[1]/tbody/tr[2]/td[3]/button').click ()
    elif options.macaddr is not None:
        driver.find_element_by_id ("mac").send_keys (options.macaddr)
        driver.find_element_by_xpath ('//*[@id="main"]/div/table[1]/tbody/tr[3]/td[3]/button').click ()
    elif options.deviceid is not None:
        driver.find_element_by_id ("deviceId").send_keys (options.deviceid)
        driver.find_element_by_xpath ('//*[@id="main"]/div/table[1]/tbody/tr[4]/td[3]/button').click ()

    try:
        wait = WebDriverWait(driver, 10)
        wait.until (wait_for_element_non_empty ((By.ID, 'a_result3')))

        serial_num = driver.find_element_by_id ('result1').text
        macaddr = driver.find_element_by_id ('result2').text
        deviceid = driver.find_element_by_id ('result3').text
        anonymized_device_id = driver.find_element_by_id ('a_result3').text

        print "Serial: %s , MAC Addr: %s , Device id: %s, Anonymized Device id: %s" % (serial_num, macaddr, deviceid, anonymized_device_id)
    except Exception, e:
        pass

    driver.quit()


if __name__ == '__main__':
    main ()

