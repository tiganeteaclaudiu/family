import unittest
import wget
import configparser
from pyunitreport import HTMLTestRunner
import os, datetime, time
from uiautomator import Device
import subprocess
from holochat_adb import ADB
from holochat_helper_functions import *
from device_setup_functions import *

cfg_file = 'monkey.ini'

cfg = configparser.ConfigParser()

if not os.path.exists(cfg_file):
    print('\n[ERROR] No configuration file found. \n        Make sure there is a config.ini file.\n')
    exit()

#create campaign directory
campaigndir = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')+'_Monkey')
os.makedirs(campaigndir)

#set default parameters
screen_record = 'yes'
screen_record_time = '30'
screen_record_dir = '/sdcard/monkey.mp4'
monkey_pct_touch = '90'
monkey_pct_syskeys = '5'
monkey_file = os.path.join(campaigndir, 'output.txt')
monkey_finish_message = '// Monkey finished'
battery_level = '10'
seed = None

#load default setup
setup = {
    'wifi' : 'yes',
    'bluetooth' : 'no',
    'hotspot' : 'no',
    'airplane_mode' : 'no',
    'close_all_apps' : 'yes',
    'mute_ring_volume' : 'yes',
    'reboot' : 'yes'
}

cfg.read('monkey.ini')
app = cfg['app']
dev = cfg['dut']

#load setup from config file
for key in cfg['setup']:
    if cfg['setup'][key] in ['yes','no']:
        setup[key] = cfg['setup'][key]

#if parameters are given, overwrite default ones
if 'parameters' in cfg:
    parameters = cfg['parameters']
    screen_record = parameters['screen_record']
    screen_record_time = parameters['screen_record_time']
    screen_record_dir = parameters['screen_record_dir']
    monkey_pct_touch = parameters['pct_touch']
    monkey_pct_syskeys = parameters['pct_syskeys']
    monkey_dir = os.path.join(campaigndir, parameters['output'])
    monkey_finish_message = parameters['finish_message']
    battery_level = parameters['battery_level']
    seed = parameters['seed']
else:
    print('[WARNING] No monkey tests parameters were given in configuration file.')

#Parse ADB logging levels
try:
    adb_log_levels = cfg['adb_log_level']
    adb_console_level = adb_log_levels['console']
    adb_file_level = adb_log_levels['file']
except Exception as e:
    print ('[WARNING] No logging levels found in config file. Defaulting to "debug"')
    adb_console_level = 'debug'
    adb_file_level = 'debug'

class MonkeyTests(unittest.TestCase):
    d = Device(dev['id'])

    #changing working directory
    os.chdir(campaigndir)

    adb = ADB(deviceId=dev['id'], device=d, consoleLevel=adb_console_level, fileLevel=adb_file_level)

    # Register watchers for ANRs
    # FIXME pause testing to report ANR
    d.watcher('AUTO_FC_WHEN_ANR').when(resourceId="android:id/aerr_restart").when(resourceId="android:id/alertTitle") \
        .click(resourceId="android:id/aerr_restart")

    #initial device setup for monkey tests
    def load_setup(self):
        #quick settings to be enabled/disabled
        to_enable = {key:val for key,val in setup.items() if val == 'yes'}
        to_disable = {key:val for key,val in setup.items() if val == 'no'}

        toggle_quick_settings(self.d, to_enable, to_disable)

        if setup['hotspot'] == 'yes':
            toggle_hotspot(self.d,enable=True)
        else:
            toggle_hotspot(self.d,enable=False)

        if setup['mute_ring_volume'] == 'yes':
            self.adb.mute_ring_volume()

        if setup['close_all_apps'] == 'yes':
            close_all_apps(self.d)

        #TODO: figure a way to reboot the device

    def test_setup_app(self):
        """Download and install Holochat apk on devices"""
        app['filename'] = download_apk(url=app['url'], self=self)
        self.adb.clear_logs()
        self.adb.uninstall_apk(package=app['package'])
        self.adb.install_apk(apk=app['filename'], package=app['package'])

    def test_startup_app(self):
        """Test that Holochat can be started from adb by calling ConnectActivity"""
        self.adb.holochat_stop_app_from_adb(package=app['package'])
        self.adb.holochat_start_app_from_adb(package=app['package'], app=app)
        # TODO add results directory/archive

    def test_accept_holochat_permissions(self):
        """Test that users can accept Holochat required Android permissions DUTs"""
        # FIXME permission names are in the system language (English)
        holochat_accept_permissions(deviceId=dev['id'], device=self.d, self=self)

    def test_accept_holochat_beta(self):
        """Test that users can accept Holochat Beta disclaimer"""
        holochat_accept_beta_version(deviceId=dev['id'], device=self.d, self=self)

    def test_login_app(self):
        """Test that users can login to Holochat on DUTs"""
        holochat_sign_in(deviceId=dev['id'], device=self.d, username=dev['username'], self=self)
        holochat_verify_logged_user(deviceId=dev['id'], device=self.d, username=dev['username'], email=dev['email'],
                                    self=self)
        time.sleep(2)

    def test_monkey(self):

        #check if device is sufficiently charged
        self.adb.wait_battery_level(battery_level)
        self.adb.mute_ring_volume()

        print('Clearing logs on DUT')
        self.adb.clear_logs()
        print('Force stopping Holochat on DUT')
        self.adb.holochat_stop_app_from_adb(package=app['package'])

        # self.adb.screen_record(time_limit=screen_record_time,dir=screen_record_dir)
        print('Letting the Monkey loose')
        #looking to give the hungry monkey a seed
        if seed is None:
            #adb.monkey_threaded() is called instead of adb.monkey to allow screen recording
            self.adb.monkey_threaded(package=app['package'],
                            pct_touch=monkey_pct_touch,
                            pct_syskeys=monkey_pct_syskeys,
                            output_file=monkey_file,
                            screen_record=screen_record,
                            screen_record_time_limit=screen_record_time,
                            screen_record_dir=screen_record_dir)
        else:
            self.adb.monkey_threaded(package=app['package'],
                            pct_touch=monkey_pct_touch,
                            pct_syskeys=monkey_pct_syskeys,
                            output_file=monkey_file,
                            screen_record=screen_record,
                            screen_record_time_limit=screen_record_time,
                            screen_record_dir=screen_record_dir,
                            seed=seed)

        #reading the monkey output file
        monkey_output_file = open(monkey_file, 'r')
        lines = monkey_output_file.readlines()
        #2 hacks fixing parsing problem resulting in failed assert
        last_line = lines[-2]
        last_line = last_line.strip()

        first_lines = lines[0:50]

        try:
            self.assertEquals(last_line, monkey_finish_message)
            print('\n---Monkey tests PASSED---')
        except AssertionError as e:
            print('\n---Monkey tests FAILED---')
            print('Collecting Bug Report')
            bugreport_dir = os.path.join(campaigndir,'{}_{}_bugreport.zip'.format(datetime.datetime.now(),dev['id']))
            #get bug report
            self.adb.test_get_bugreport(filename=bugreport_dir)
            #pull screen recording
            print('Collecting screen record from DUT')
            self.adb.pull_file(screen_record_dir)

        monkey_output = open(monkey_file, 'r').read().replace('\n', ' ')
        print("\n Monkey tests  data:")

        try:
            monkey_seed = re.search('seed=([0-9]{13}).+', monkey_output).groups()[0]
            print("    -Seed: {}".format(monkey_seed))
        except Exception as e:
            print("Error parsing monkey tests seed: {}".format(e))

        try:
            print('crash')
            monkey_crash_signature = re.search('.+(aborted|CRASH).+', monkey_output[:-300]).groups()[0]
            print("    -Crash signature: {}".format(monkey_crash_signature))
        except Exception as e:
            pass

if __name__ == '__main__':

    appInitSuite = unittest.TestSuite()
    appMonkeySuite = unittest.TestSuite()
    appInitSuite.addTest(MonkeyTests('test_setup_app'))
    appInitSuite.addTest(MonkeyTests('test_startup_app'))
    appInitSuite.addTest(MonkeyTests('test_accept_holochat_permissions'))
    appInitSuite.addTest(MonkeyTests('test_accept_holochat_beta'))
    appInitSuite.addTest(MonkeyTests('test_login_app'))

    appMonkeySuite.addTest(MonkeyTests('load_setup'))
    appMonkeySuite.addTest(MonkeyTests('test_monkey'))

    testRunner=HTMLTestRunner(output='',verbosity=2)
    testRunner.run(appInitSuite)
    testRunner.run(appMonkeySuite)
