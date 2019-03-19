====================
# Holochat Tests

The Holochat Tests repository is meant to host the necessary code to run python
automated tests on the Holochat Android application.

## Deploying the Tests
### Prerequisites
On your machine please make sure you have:
1. Android SDK Platform Tools (download from https://developer.android.com/studio/releases/platform-tools)
   please extract the platform tools to your $HOME/Android/Sdk/platform-tools
2. Android SDK Tools (download fom https://developer.android.com/studio/#downloads Commad line tools only)
   please extract the sdk tools to your $HOME/Android/Sdk/tools
3. Add the android udev rules (cf. https://github.com/M0Rf30/android-udev-rules)
4. Activate ADB debugging on the devices (cf. https://developer.android.com/studio/command-line/adb#Enabling)
5. You need to set the test devices' language to English and the Screen lock to None
6. Python3 and virtualenv installed

```bash
sudo apt-get update
sudo apt-get install python3 python3-virtualenv
```

### clone the test repository

```bash
git clone git@git.korys.io:rkhalifa/holochat_tests.git
```

# TestLink-XML based automation framework

This architecture is meant to integrate TestLink as the base for all our automated tests, via XML export files.
It provides a solution to previous problems such as: code reusability, scalability, ease of use, maintainability etc.

The final goal is seamless test campaign running by using either XML Test Plan files from TestLink, or just API calls to an instance of TestLink.

What is important to note are that we have parameters on all levels (TestPlan, Test Suites and Test Cases). This allows for code reusability, meaning that (unlike in the previous architecture) we can now reuse Test Cases across Test Plans.

### How to run TestPlans:

There are currently 2 ways of running TestPlans:

####  1) Using Testlink-exported XML TestPlan files:
- Does not need a Jenkins instance, but can be ran from Jenkins by passing the testplan.xml file
- Runs XML file top to bottom, generates Test Reports both locally and on a TestLink instance by associating Test Cases in the XML with their equivalent on the platform.
- Does not require a connection to an instance of TestLink. If no connection can be made, an HTML Test Report is generated locally.

##### Test Cases are ran top-bottom. All Test Cases in a Suite have to run before it passes over to the next Suite.

##### HOW-TO:
    - Replace 'testplan.xml' file in local directory with relevant TestLink XML TestPlan file
    - Run from console:
        python ./run_testplan.py

##### Imported XML files have to be put into the same directory as xmlparser.py, under the name 'testplan.xml'

####  2) Using TestLink API calls:

- Can be run from Jenkins or can be run locally by manually passing the required parameters. Parameters needed for the API calls are:
    a) TestLink project name
    b) TestPlan name
    c) Build name
- The framework gets all needed data for running the Test Plan by these 3 parameters
- HTML Test Reports are generated both locally and on the TestLink instance

#####  HOW-TO:
    - Configure running parameters on Jenkins
    - Launch campaign from Jenkins

### Setting up devices in setup.xml:

Devices need to be set up using their device ID's (obtained from 'adb devices') and the accounts associated with them.

Example XML format:
```
<devices>
  <device>
    <id>9ad4dee2</id>
    <accounts>
      <account>
        <username>
          Korys Test1
        </username>
        <email>
          korys.test1@gmail.com
        </email>
      </account>
    </accounts>
  </device>
  <device>
    <id>977f68c3</id>
    <accounts>
      <account>
        <username>
          Korys Test2
        </username>
        <email>
          korys.test2@gmail.com
        </email>
      </account>
    </accounts>
  </device>
</devices>
```

### Test Case format:
```
	def test_case(self, devices=None,case_parameters=None,suite_parameters=None):

	Arguments:
		-case_parameters
			Dictionary of parameters to be used strictly in one particular Test Case
			Ex:
				{
					'monkey_seed': '123131234',
				}
		-suite_parameters
			Dictionary of parameters to be used in all Test Cases in a particular Test Suite
			Ex:
				{
          'logger_level_console':'info',
          'logger_level_file':'debug'
				}
```

### Exemple Test Case:

```
@create_dir
@run_for_each_device
def test_login_app(self, devices=None,case_parameters=None,suite_parameters=None):
  device = devices[0]
  username = device['accounts'][0]['username']
  email = device['accounts'][0]['email']
  holochat_sign_in(deviceId=device['id'], device=device['device'], username=username,self=self)
  holochat_skip_setup_wizard(deviceId=device['id'], device=device['device'], self=self)
  holochat_verify_logged_user(deviceId=device['id'], device=device['device'], username=device['accounts'][0]['username'], email=email,self=self)
  time.sleep(2)
```

### Decorators available for test case methods:
```
@timeout_after(timeout_time):
```
  Stops execution of method after given time limit. Sets test case as failed, with detailed error message.
```
@skip
```
  Skip test case (mainly used for debugging)
```
@run_for_each_device
```
  Runs test case method using a single thread. Devices are taken from the 'devices' parameter of the wrapped method.
```
@create_dir
```
  Creates directory for test case method (mainly used for test case specific screenshots and logs)

## Testlink_XML_Parser Documentation:

### Classes for Test Plan/Suite/Case:

```
class TestPlan():
	def __init__(self,name,testsuites,custom_fields,attributes,campaigndir,build):
```

```
class TestSuite():
	def __init__(self,name,testcases,attributes,custom_fields):
```

```
class TestCase():
	def __init__(self,name,internalid,attributes,custom_fields,devices,method_name, summary):
```


### Testlink_XML_Parser class:

Provides methods for parsing TestLink-exported XML test plan files.

#### Testlink_XML_Parser.xml_parse() method:

	Return format:
```
====================[TESTPLAN]====================
	Name: test_testplan
	Build: build1
	Attributes:
	Custom fields :
	Test Suites:
0)
		--------------------[SUITE]--------------------
		----------------------------------------------

		Name = app_init_suite
		Custom fields :
			package_name = package_name
			application_label = APP_NAME
			version_code = 1.7
			version_name = 1.7
			launchable_activity = activity
			apk_path = /home/files/holochat_v1.7.apk
			logger_level_console = info
			logger_level_file = debug
		Test cases :
    0)
			....................[CASE]....................

			Name = test_setup_app
			InternalID: 218
			Method Name: test_setup_app
			Custom fields :
			Devices:
				0) {
          'id': '9ad4dee2',
          'device': <uiautomator.AutomatorDevice object at 0x7f81f29ca668>,
          'adb': <app_adb.ADB object at 0x7f81f29cab00>,
          'accounts': [{'username': 'user1', 'email': 'email@gmail.com'}]}
        1) {
          'id': '1234abcd',
          'device': <uiautomator.AutomatorDevice object at 0x7fasd29ca668>,
          'adb': <app_adb.ADB object at 0x7fasd29c3as68>,
          'accounts': [{'username': 'user2', 'email': 'email@gmail.com'}]}
			Attributes:
				node_order = 3

		----------------------------------------------
    1)
			....................[CASE]....................

			Name = test_login_app
			InternalID: 219
			Method Name: test_login_app
			Custom fields :
			Devices:
				0) {
          'id': '9ad4dee2',
          'device': <uiautomator.AutomatorDevice object at 0x7f81f29ca668>,
          'adb': <app_adb.ADB object at 0x7f81f29cab00>,
          'accounts': [{'username': 'user1', 'email': 'email@gmail.com'}]}
        1) {
          'id': '1234abcd',
          'device': <uiautomator.AutomatorDevice object at 0x7fasd29ca668>,
          'adb': <app_adb.ADB object at 0x7fasd29c3as68>,
          'accounts': [{'username': 'user2', 'email': 'email@gmail.com'}]}
			Attributes:
				node_order = 4

		----------------------------------------------
		END Suite
==================================================
==================================================
END Plan
```

#### Testlink_XML_Parser.parse_testlink_testplan(self,testplan_name=None,build_name=None,testproject_name=None):

Returns the same object as Testlink_XML_Parser.xml_parse()

### Exemple XML export:
```ini
<?xml version="1.0" encoding="UTF-8"?>
<testplan>
  <name><![CDATA[test_testplan]]></name>

  <testproject>
    <name><![CDATA[test_project]]></name>
    <prefix><![CDATA[tp]]></prefix>
    <internal_id><![CDATA[52]]></internal_id>
  </testproject>

  <build>
    <name><![CDATA[build1]]></name>
    <internal_id><![CDATA[8]]></internal_id>
  </build>

  <testsuites>
    <testsuite name="parent_test_suite" >
      <node_order><![CDATA[3]]></node_order>
      <details><![CDATA[]]>		<custom_fields>
        <custom_field>
          <name><![CDATA[suite_parameters]]></name>
          <value><![CDATA[]]></value>
        </custom_field>
      </custom_fields>
    </details>

    <testsuite name="child_suite" >
      <node_order><![CDATA[1]]></node_order>
      <details><![CDATA[]]>		
			<custom_fields>
        <custom_field>
          <name><![CDATA[suite_parameters]]></name>
          <value><![CDATA[logger_level_console=infologger_level_file=debug]]></value>
        </custom_field>
      </custom_fields>
    </details>

    <testcase internalid="218" name="test_setup_app">
      <node_order><![CDATA[0]]></node_order>
      <custom_fields>
        <custom_field>
          <name><![CDATA[case_parameters]]></name>
          <value><![CDATA[]]></value>
        </custom_field>
      </custom_fields>
    </testcase>

  </testsuite>
</testsuite>
</testsuites>
</testplan>

```

### Running Test Plan:
```
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
python3 -m venv .venv --prompt holochat_tests
. .venv/bin/activate
pip install -r requirements.txt
python run_testplan.py
deactivate
```
