(holochat_tests) claudiu@claudiu-korys-XPS-13-9370:~/korys/koryshome/holochat_tests_floobits$ python ./testlink_docs.py
getLatestBuildForTestPlan(<testplanid>, [devKey=<devKey>])
 Gets the latest build by choosing the maximum build id for a specific test plan

getLastExecutionResult(<testplanid>, <testcaseid>, [testcaseexternalid=<testcaseexternalid>], [platformid=<platformid>], [platformname=<platformname>], [buildid=<buildid>], [buildname=<buildname>], [options=<options>], [devKey=<devKey>])
 Gets the result of LAST EXECUTION for a particular testcase on a test plan.
If there are no filter criteria regarding platform and build,
result will be get WITHOUT checking for a particular platform and build.

following optional arguments could only used with
TL version >= 1.9.9
- platformid, platformname, buildid, buildname

TL version >= 1.9.11
- options : dictionary with key value pair
                    'getBugs' : True / False


sayHello()
 Lets you see if the server is up and running

repeat(<str>)
 Repeats a message back

about()
 Gives basic information about the API

createBuild(<testplanid>, <buildname>, <buildnotes>, [active=<active>], [open=<open>], [releasedate=<releasedate>], [copytestersfrombuild=<copytestersfrombuild>], [devKey=<devKey>])
 Creates a new build for a specific test plan

        active      : 1 (default) = activ  0 = inactiv
        open        : 1 (default) = open   0 = closed
        releasedate : YYYY-MM-DD
        copytestersfrombuild : valid buildid tester assignments will be copied.


getProjects([devKey=<devKey>])
 Gets a list of all projects

        returns an empty list, if no test project exist

getProjectTestPlans(<testprojectid>, [devKey=<devKey>])
 Gets a list of test plans within a project

        returns an empty list, if no testplan is assigned

getBuildsForTestPlan(<testplanid>, [devKey=<devKey>])
 Gets a list of builds within a test plan

        returns an empty list, if no build is assigned

getTestSuitesForTestPlan(<testplanid>, [devKey=<devKey>])
 List test suites within a test plan alphabetically

        returns an empty list, if no suite is assigned

createTestProject(<testprojectname>, <testcaseprefix>, [notes=<notes>], [active=<active>], [public=<public>], [options=<options>], [itsname=<itsname>], [itsenabled=<itsenabled>], [devKey=<devKey>])
 Create a test project

        options : dictionary with keys
                    requirementsEnabled, testPriorityEnabled,
                    automationEnabled,inventoryEnabled
                 and values 0 (false) and 1 (true)

getTestCasesForTestSuite(<testsuiteid>, <deep>, <details>, [getkeywords=<getkeywords>], [devKey=<devKey>])
 List test cases within a test suite alphabetically

        details - default is 'simple',
                  use 'full' if you want to get summary,steps & expected_results
                  or 'only_id', if you just need an ID list

        deep - True/False - default is True
               if True, return also test case of child suites

        getkeywords - True/False - default is False
               if True AND details='full', dictionary includes for each test
               case, which as assigned keywords, an additional key value pair
               'keywords'

        returns an empty list, if no build is assigned

getTestCaseIDByName(<testcasename>, [testsuitename=<testsuitename>], [testprojectname=<testprojectname>], [testcasepathname=<testcasepathname>], [devKey=<devKey>])
 getTestCaseIDByName : Find a test case by its name
        positional args: testcasename,
        optional args : testsuitename, testprojectname, testcasepathname

        testcasepathname : Full test case path name,
                starts with test project name , pieces separator -> ::

        server return can be a list or a dictionary
        - optional arg testprojectname seems to create a dictionary response

        this methods customize the generic behaviour and converts a dictionary
        response into a list, so methods return will be always a list

createTestCase(<testcasename>, <testsuiteid>, <testprojectid>, <authorlogin>, <summary>, [steps=<steps>], [preconditions=<preconditions>], [importance=<importance>], [executiontype=<executiontype>], [order=<order>], [internalid=<internalid>], [checkduplicatedname=<checkduplicatedname>], [actiononduplicatedname=<actiononduplicatedname>], [status=<status>], [estimatedexecduration=<estimatedexecduration>], [devKey=<devKey>])
 createTestCase: Create a test case
        positional args: testcasename, testsuiteid, testprojectid, authorlogin,
                         summary
        optional args : steps, preconditions, importance, executiontype, order,
                        internalid, checkduplicatedname, actiononduplicatedname,
                        status, estimatedexecduration

        argument 'steps' will be set with values from .stepsList,
        - when argsOptional does not include a 'steps' item
        - .stepsList can be filled before call via .initStep() and .appendStep()

        otherwise, optional arg 'steps' must be defined as a list with
        dictionaries , example
            [{'step_number' : 1, 'actions' : "action A" ,
                'expected_results' : "result A", 'execution_type' : 0},
                 {'step_number' : 2, 'actions' : "action B" ,
                'expected_results' : "result B", 'execution_type' : 1},
                 {'step_number' : 3, 'actions' : "action C" ,
                'expected_results' : "result C", 'execution_type' : 0}]



reportTCResult(<testcaseid>, <testplanid>, <buildname>, <status>, <notes>, [testcaseexternalid=<testcaseexternalid>], [buildid=<buildid>], [platformid=<platformid>], [platformname=<platformname>], [guess=<guess>], [bugid=<bugid>], [customfields=<customfields>], [overwrite=<overwrite>], [user=<user>], [execduration=<execduration>], [timestamp=<timestamp>], [steps=<steps>], [devKey=<devKey>])
 Reports a result for a single test case

        args variations: testcaseid - testcaseexternalid
                         buildid - buildname
                         platformid - platformname

        customfields : dictionary with customfields names + values
            VERY IMPORTANT: value must be formatted in the way it's written to db
        overwrite    : if present and true, then last execution for
                       (testcase,testplan,build,platform) will be overwritten.
        user : if present and user is a valid login (no other check will be done)
               it will be used when writing execution.
        execduration : Exec (min) as float (2.5 = 2min 30sec)
        timestamp    : 'YYYY-MM-DD hh:mm[:ss]'#
        steps        : [{'step_number' : 6, 'result' : 'p', 'notes" : 'a_note'},
                        {'step_number' : 7, 'result' : 'f', 'notes" : 'blabla'}]


getTestCasesForTestPlan(<testplanid>, [buildid=<buildid>], [platformid=<platformid>], [testcaseid=<testcaseid>], [keywordid=<keywordid>], [keywords=<keywords>], [executed=<executed>], [assignedto=<assignedto>], [executestatus=<executestatus>], [executiontype=<executiontype>], [getstepinfo=<getstepinfo>], [details=<details>], [devKey=<devKey>])
 List test cases linked to a test plan

        details - default is 'full',
                  'simple', 'details' ??

        args variations:     keywordid - keywords

        returns an empty list, if no build is assigned

getTestCaseCustomFieldDesignValue(<testcaseexternalid>, <version>, <testprojectid>, <customfieldname>, <details>, [devKey=<devKey>])
 Gets value of a Custom Field with scope='design' for a given Test case

        details =  changes output information
            null or 'value' => just value
            'full' => a map with all custom field definition
                          plus value and internal test case id
            'simple' => value plus custom field name, label, and type (as code).

        attention - be careful with testcaseexternalid - it must include an '-'.
        otherwise TL (<=1.9.8) returns
        <ProtocolError for xmlrpc.php: 500 Internal Server Error>

addTestCaseToTestPlan(<testprojectid>, <testplanid>, <testcaseexternalid>, <version>, [platformid=<platformid>], [executionorder=<executionorder>], [urgency=<urgency>], [overwrite=<overwrite>], [devKey=<devKey>])
 Add a test case version to a test plan

getFirstLevelTestSuitesForTestProject(<testprojectid>, [devKey=<devKey>])
 get set of test suites AT TOP LEVEL of tree on a Test Project

        returns an empty list, if no suite is assigned (api error 7008)
        - details see comments for decoMakerApiCallReplaceTLResponseError

assignRequirements(<testcaseexternalid>, <testprojectid>, <requirements>, [devKey=<devKey>])
 Assign Requirements to a test case
        It is possible to assign multiple requirements, belonging to different
        requirement specifications. (the internal IDs must be known!)

        Argument REQUIREMENTS expects an array of dictionaries, example:
        .assignRequirements('GPROAPI4-2', 6652,
                           [{'req_spec' : 6729, 'requirements' : [6731]},
                            {'req_spec' : 6733, 'requirements' : [6735, 6737]}])
        This would assign to testcase 'GPROAPI4-2' (in testproject with id 6652)
        a) requirement with ID 6731 of requirement spec 6729 AND
        b) requirements with ID 6735 and 6737 of requirement spec 6733


getTestCaseAttachments(<testcaseid>, [testcaseexternalid=<testcaseexternalid>], [devKey=<devKey>])
 Gets attachments for specified test case.
        The attachment file content is Base64 encoded. To save the file to disk
        in client, Base64 decode the content and write file in binary mode.

createTestSuite(<testprojectid>, <testsuitename>, <details>, [parentid=<parentid>], [order=<order>], [checkduplicatedname=<checkduplicatedname>], [actiononduplicatedname=<actiononduplicatedname>], [devKey=<devKey>])
 create a test suite

getTestProjectByName(<testprojectname>, [devKey=<devKey>])
 Gets info about target test project

getTestPlanByName(<testprojectname>, <testplanname>, [devKey=<devKey>])
 Gets info about target test project

getTestCase(<testcaseid>, [testcaseexternalid=<testcaseexternalid>], [version=<version>], [devKey=<devKey>])
 get test case specification using external or internal id

        attention - be careful with testcaseexternalid - it must include an '-'.
        otherwise TL (<=1.9.8) returns
        <ProtocolError for xmlrpc.php: 500 Internal Server Error>

createTestPlan(<testplanname>, [testprojectname=<testprojectname>], [prefix=<prefix>], [note=<note>], [active=<active>], [public=<public>], [devKey=<devKey>])
 create a test plan

            args variations: testprojectname - prefix

            supports also pre 1.9.14 arg definition, where 'testprojectname'
            was mandatory ('prefix' comes as alternative with 1.9.14)

            examples:
            - createTestPlan('aTPlanName', 'aTProjectName')
            - createTestPlan('aTPlanName', testprojectname='aTProjectName')
            - createTestPlan('aTPlanName', prefix='aTProjectPrefix')



getFullPath(<nodeid>, [devKey=<devKey>])
 Gets full path from the given node till the top using nodes_hierarchy_table

        nodeid = can be just a single id or a list with ids
                 ATTENTION: id must be an integer.

deleteExecution(<executionid>, [devKey=<devKey>])
 delete an execution

        Default TL server configuration does not allow deletion of exections
        see Installation & Configuration Manual Version 1.9
            chap. 5.8. Test execution settings
            $tlCfg->exec_cfg->can_delete_execution

getTestSuiteByID(<testsuiteid>, [devKey=<devKey>])
 Return a TestSuite by ID

getTestSuitesForTestSuite(<testsuiteid>, [devKey=<devKey>])
 get list of TestSuites which are DIRECT children of a given TestSuite

        returns an empty list, if no TestSuite is assigned

getTestPlanPlatforms(<testplanid>, [devKey=<devKey>])
 Returns the list of platforms associated to a given test plan

        returns an empty list, if no platform is assigned (api error 3041)
        - details see comments for decoMakerApiCallReplaceTLResponseError

getTotalsForTestPlan(<testplanid>, [devKey=<devKey>])
 Gets the summarized results grouped by platform.

doesUserExist(<user>)
 Checks if user name exists
        returns true if everything OK, otherwise error structure

checkDevKey(<devKey>)
 check if Developer Key exists
        returns true if everything OK, otherwise error structure

uploadRequirementSpecificationAttachment(<attachmentfile>, <reqspecid>, [title=<title>], [description=<description>], [filename=<filename>], [filetype=<filetype>], [content=<content>], [devKey=<devKey>])
 Uploads an attachment for a Requirement Specification.

        reqspecid - The Requirement Specification ID

        mandatory non api args: attachmentfile
        - python file descriptor pointing to the file
        - or a valid file path

        default values for filename, filetype, content are determine from
        ATTACHMENTFILE, but user could overwrite it, if user want to store the
        attachment with a different name


uploadRequirementAttachment(<attachmentfile>, <requirementid>, [title=<title>], [description=<description>], [filename=<filename>], [filetype=<filetype>], [content=<content>], [devKey=<devKey>])
 Uploads an attachment for a Requirement.

        requirementid - The Requirement ID

        mandatory non api args: attachmentfile
        - python file descriptor pointing to the file
        - or a valid file path

        default values for filename, filetype, content are determine from
        ATTACHMENTFILE, but user could overwrite it, if user want to store the
        attachment with a different name


uploadTestProjectAttachment(<attachmentfile>, <testprojectid>, [title=<title>], [description=<description>], [filename=<filename>], [filetype=<filetype>], [content=<content>], [devKey=<devKey>])
 Uploads an attachment for a Test Project.

        testprojectid - The Test Project ID

        mandatory non api args: attachmentfile
        - python file descriptor pointing to the file
        - or a valid file path

        default values for filename, filetype, content are determine from
        ATTACHMENTFILE, but user could overwrite it, if user want to store the
        attachment with a different name


uploadTestSuiteAttachment(<attachmentfile>, <testsuiteid>, [title=<title>], [description=<description>], [filename=<filename>], [filetype=<filetype>], [content=<content>], [devKey=<devKey>])
 Uploads an attachment for a Test Suite.

        testsuiteid - The Test Suite ID

        mandatory non api args: attachmentfile
        - python file descriptor pointing to the file
        - or a valid file path

        default values for filename, filetype, content are determine from
        ATTACHMENTFILE, but user could overwrite it, if user want to store the
        attachment with a different name


uploadTestCaseAttachment(<attachmentfile>, <testcaseid>, [title=<title>], [description=<description>], [filename=<filename>], [filetype=<filetype>], [content=<content>], [devKey=<devKey>])
 Uploads an attachment for a Test Case.

        testcaseid - Test Case INTERNAL ID

        mandatory non api args: attachmentfile
        - python file descriptor pointing to the file
        - or a valid file path

        default values for filename, filetype, content are determine from
        ATTACHMENTFILE, but user could overwrite it, if user want to store the
        attachment with a different name


uploadExecutionAttachment(<attachmentfile>, <executionid>, <title>, <description>, [filename=<filename>], [filetype=<filetype>], [content=<content>], [devKey=<devKey>])
 Uploads an attachment for an execution

        executionid - execution ID

        mandatory non api args: attachmentfile
        - python file descriptor pointing to the file
        - or a valid file path

        default values for filename, filetype, content are determine from
        ATTACHMENTFILE, but user could overwrite it, if user want to store the
        attachment with a different name


uploadAttachment(<attachmentfile>, <fkid>, <fktable>, [title=<title>], [description=<description>], [filename=<filename>], [filetype=<filetype>], [content=<content>], [devKey=<devKey>])
 Uploads an attachment for an execution

        fkid    - The Attachment Foreign Key ID
        fktable - The Attachment Foreign Key Table

        mandatory non api args: attachmentfile
        - python file descriptor pointing to the file
        - or a valid file path

        default values for filename, filetype, content are determine from
        ATTACHMENTFILE, but user could overwrite it, if user want to store the
        attachment with a different name


getTestCaseCustomFieldExecutionValue(<customfieldname>, <testprojectid>, <version>, <executionid>, <testplanid>, [devKey=<devKey>])
 Gets a Custom Field of a Test Case in Execution Scope.

getTestCaseCustomFieldTestPlanDesignValue(<customfieldname>, <testprojectid>, <version>, <testplanid>, <linkid>, [devKey=<devKey>])
 Gets a Custom Field of a Test Case in Test Plan Design Scope.

getTestSuiteCustomFieldDesignValue(<customfieldname>, <testprojectid>, <testsuiteid>, [devKey=<devKey>])
 Gets a Custom Field of a Test Suite in Design Scope.

getTestPlanCustomFieldDesignValue(<customfieldname>, <testprojectid>, <testplanid>, [devKey=<devKey>])
 Gets a Custom Field of a Test Plan in Design Scope.

getReqSpecCustomFieldDesignValue(<customfieldname>, <testprojectid>, <reqspecid>, [devKey=<devKey>])
 Gets a Custom Field of a Requirement Specification in Design Scope.

getRequirementCustomFieldDesignValue(<customfieldname>, <testprojectid>, <requirementid>, [devKey=<devKey>])
 Gets a Custom Field of a Requirement Specification in Design Scope.

createTestCaseSteps(<action>, <steps>, [testcaseexternalid=<testcaseexternalid>], [testcaseid=<testcaseid>], [version=<version>], [devKey=<devKey>])
 creates new test steps or updates existing test steps

        action - possible values: 'create','update','push'
            create: if step exist NOTHING WILL BE DONE
            update: if step DOES NOT EXIST will be created else will be updated.
            push: NOT IMPLEMENTED YET (TL 1.9.9)
                  shift down all steps with step number >= step number provided
                  and use provided data to create step number requested.
        steps - each element is a hash with following keys
            step_number,actions,expected_results,execution_type
        args variations: testcaseid - testcaseexternalid
        version - optional if not provided LAST ACTIVE version will be used
                  if all versions are INACTIVE, then latest version will be used.


deleteTestCaseSteps(<testcaseexternalid>, <steps>, [version=<version>], [devKey=<devKey>])
 deletes test cases steps

        steps - each element is a step_number
        version - optional if not provided LAST ACTIVE version will be used


updateTestCaseCustomFieldDesignValue(<testcaseexternalid>, <version>, <testprojectid>, <customfields>, [devKey=<devKey>])
 Update value of Custom Field with scope='design' for a given Test case

       customfields : dictionary with customfields names + values
            VERY IMPORTANT: value must be formatted in the way it's written to db

setTestCaseExecutionType(<testcaseexternalid>, <version>, <testprojectid>, <executiontype>, [devKey=<devKey>])
 Update execution type for a test case version

        possible executiontype values
        1 = TESTCASE_EXECUTION_TYPE_MANUAL, 2 = TESTCASE_EXECUTION_TYPE_AUTO

getExecCountersByBuild(<testplanid>, [devKey=<devKey>])
 Gets execution metrics information for a testplan

createPlatform(<testprojectname>, <platformname>, [notes=<notes>], [devKey=<devKey>])
 Creates a platform for test project

getProjectPlatforms(<testprojectid>, [devKey=<devKey>])
 Gets a dictionary of platforms for a project

        returns an empty dictionary, if no platform is assigned

addPlatformToTestPlan(<testplanid>, <platformname>, [devKey=<devKey>])
 Adds a platform to a test plan

removePlatformFromTestPlan(<testplanid>, <platformname>, [devKey=<devKey>])
 Removes a platform from a test plan

getUserByLogin(<user>, [devKey=<devKey>])
  returns user data for account with login name USER

        if everything ok returns an array on just one element with following user data
    *
    * firstName,lastName,emailAddress,locale,isActive,defaultTestprojectID,
    * globalRoleID
    * globalRole    array with role info
    * tprojectRoles array
    * tplanRoles    array
    * login
    * dbID
    * loginRegExp
    *
    * ATTENTION: userApiKey will be set to NULL, because is worst that access to user password

getUserByID(<userid>, [devKey=<devKey>])
  returns user data for account with USERID in users table, column ID

    * if everything ok returns an array on just one element with following user data
    *
    * firstName,lastName,emailAddress,locale,isActive,defaultTestprojectID,
    * globalRoleID
    * globalRole    array with role info
    * tprojectRoles array
    * tplanRoles    array
    * login
    * dbID
    * loginRegExp
    *
    * ATTENTION: userApiKey will be set to NULL, because is worst that access to user password


updateTestCase(<testcaseexternalid>, [version=<version>], [testcasename=<testcasename>], [summary=<summary>], [preconditions=<preconditions>], [steps=<steps>], [importance=<importance>], [executiontype=<executiontype>], [status=<status>], [estimatedexecduration=<estimatedexecduration>], [user=<user>], [devKey=<devKey>])
 Update an existing test case

        steps     array - each element is a hash with following keys
                  step_number,actions,expected_results,execution_type
        user      login name used as updater - optional
                  if not provided will be set to user that request update

        Not all test case attributes will be able to be updated using this method


assignTestCaseExecutionTask(<user>, <testplanid>, <testcaseexternalid>, [buildid=<buildid>], [buildname=<buildname>], [platformid=<platformid>], [platformname=<platformname>], [devKey=<devKey>])
 assigns a user to a test case execution task

        user                 login name => tester
        testplanid           test plan id
        testcaseexternalid   format PREFIX-NUMBER

        args variations:     buildid - buildname
                             platformid - platformname
        build information is general mandatory
        platform information is required, when test plan has assigned platforms


getTestCaseBugs(<testplanid>, [testcaseid=<testcaseid>], [testcaseexternalid=<testcaseexternalid>], [buildid=<buildid>], [buildname=<buildname>], [platformid=<platformid>], [platformname=<platformname>], [devKey=<devKey>])
 Returns all bugs linked to a particular testcase on a test plan.
        If there are no filter criteria regarding platform and build,
        result will be get WITHOUT checking for a particular platform and build.


        testplanid       test plan id

        args variations: testcaseid - testcaseexternalid  (mandatory!)
                         buildid - buildname
                         platformid - platformname
        test case information is general mandatory


getTestCaseAssignedTester(<testplanid>, <testcaseexternalid>, [buildid=<buildid>], [buildname=<buildname>], [platformid=<platformid>], [platformname=<platformname>], [devKey=<devKey>])
 Gets the result of LAST EXECUTION for a particular testcase on a
        test plan.

        testplanid           test plan id
        testcaseexternalid   format PREFIX-NUMBER

        args variations:     buildid - buildname
                             platformid - platformname
        build information is general mandatory
        platform information is required, when test plan has assigned platforms


unassignTestCaseExecutionTask(<testplanid>, <testcaseexternalid>, [buildid=<buildid>], [buildname=<buildname>], [platformid=<platformid>], [platformname=<platformname>], [user=<user>], [action=<action>], [devKey=<devKey>])
 assigns a user to a test case execution task

        testplanid           test plan id
        testcaseexternalid   format PREFIX-NUMBER

        args variations:     buildid - buildname
                             platformid - platformname
                             user (login name) - action ('unassignAll')
        build information is general mandatory
        platform information is required, when test plan has assigned platforms
        if action=='unassignAll', user information is not needed
        - otherwise, TL itself will set action to 'unassignOne' and expects a
          valid user information (login name => tester)



getProjectKeywords(<testprojectid>, [devKey=<devKey>])
 Gets a dictionary of valid keywords for a project

        returns an empty dictionary, if no keywords are defined

getTestCaseKeywords([testcaseid=<testcaseid>], [testcaseexternalid=<testcaseexternalid>], [devKey=<devKey>])
 Gets a dictionary of keywords for a given Test case

        args variations: testcaseid - testcaseexternalid  (mandatoy!)

        returns an empty dictionary, if no keywords are defined

deleteTestPlan(<testplanid>, [devKey=<devKey>])
 Delete a test plan and all related link to other items

addTestCaseKeywords(<keywords>, [devKey=<devKey>])
 adds list of keywords to a set of test cases

        expects as arg <keywords> a dictionary with
          <testcaseexternalid> as a key and <list of keywords> as value

        example:
          {'TC-4711' : ['KeyWord02'], 'TC-4712' : ['KeyWord01', KeyWord03']}

          adds to test case 'TC-4711' the keyword 'KeyWord02'
          adds to test case 'TC-4712' the keywords 'KeyWord01' + KeyWord03'


removeTestCaseKeywords(<keywords>, [devKey=<devKey>])
 removes list of keywords from a set of test cases

        expects as arg <keywords> a dictionary with
          <testcaseexternalid> as a key and <list of keywords> as value

        example:
          {'TC-4711' : ['KeyWord02'], 'TC-4712' : ['KeyWord01', KeyWord03']}

          removes from test case 'TC-4711' the keyword 'KeyWord02'
          removes from test case 'TC-4712' the keywords 'KeyWord01' + KeyWord03'


deleteTestProject(<prefix>, [devKey=<devKey>])
 Delete a test project and all related link to other items

updateTestSuiteCustomFieldDesignValue(<testprojectid>, <testsuiteid>, <customfields>, [devKey=<devKey>])
 Update value of Custom Field with scope='design' for a given Test Suite

        customfields  : dictionary with customfields names + values
        VERY IMPORTANT: value must be formatted in the way it's written to db


getTestSuite(<testsuitename>, <prefix>, [devKey=<devKey>])
 Returns list with all test suites named TESTUITENAME defined for
        test project using PREFIX

updateTestSuite(<testsuiteid>, [testprojectid=<testprojectid>], [prefix=<prefix>], [parentid=<parentid>], [testsuitename=<testsuitename>], [details=<details>], [order=<order>], [devKey=<devKey>])
 update a test suite

        mandatory arg: testsuiteid - identifies the test suite to be change

        mandatory args variations: testprojectid or prefix
        - test project information is general mandatory

        optional args:
        - testsuitename - if defined, test suite name will be changed
        - details       - if defined test suite details will be changed
        - order         - if defined, order inside parent container is changed


getIssueTrackerSystem(<itsname>, [devKey=<devKey>])
 Get Issue Tracker System by name

updateBuildCustomFieldsValues(<testprojectid>, <testplanid>, <buildid>, <customfields>, [devKey=<devKey>])
 Update value of Custom Field with scope='design' for a given Build

        customfields  : dictionary with customfields names + values
        VERY IMPORTANT: value must be formatted in the way it's written to db


getExecutionSet(<testplanid>, [testcaseid=<testcaseid>], [testcaseexternalid=<testcaseexternalid>], [buildid=<buildid>], [buildname=<buildname>], [platformid=<platformid>], [platformname=<platformname>], [options=<options>], [devKey=<devKey>])
 Gets a set of EXECUTIONS for a particular testcase on a test plan.
            If there are no filter criteria regarding platform and build, result
            will be get WITHOUT checking for a particular platform and build.

        mandatory arg: testplanid - identifies the test plan

        mandatory args variations: testcaseid - testcaseexternalid
        - test case information is general mandatory

        optional args variations:  buildid - buildname
                                   platformid - platformname

        options : dictionary with key 'getOrderDescending' and
                                  values 0 (false = default) or 1 (true)


getRequirements(<testprojectid>, [testplanid=<testplanid>], [platformid=<platformid>], [devKey=<devKey>])
 Get requirements.

        mandatory arg: testprojectid - identifies the test project

        optional args: testplanid, platformid


getReqCoverage(<testprojectid>, <requirementdocid>, [devKey=<devKey>])
 Get requirement coverage.
            Retrieve the test cases associated to a requirement

        mandatory arg:
            testprojectid    - identifies the test project
            requirementdocid - identifies the requirement



setTestCaseTestSuite(<testcaseexternalid>, <testsuiteid>, [devKey=<devKey>])
 move a test case to a different Test Suite

        mandatory arg:
            testcaseexternalid - identifies the test case
            testsuiteid        - identifies the test suite



getTestSuiteAttachments(<testsuiteid>, [devKey=<devKey>])
 Gets attachments for specified test suite.
        The attachment file content is Base64 encoded. To save the file to disk
        in client, Base64 decode the content and write file in binary mode.

getAllExecutionsResults(<testplanid>, [testcaseid=<testcaseid>], [testcaseexternalid=<testcaseexternalid>], [platformid=<platformid>], [buildid=<buildid>], [options=<options>], [devKey=<devKey>])
 Gets ALL EXECUTIONS for a particular testcase on a test plan.
            If there are no filter criteria regarding platform and build,
            result will be get WITHOUT checking for a particular platform and build.

        mandatory arg: testplanid - identifies the test plan

        mandatory args variations: testcaseid - testcaseexternalid
        - test case information is general mandatory

        optional args:  buildid
                        platformid

        options : dictionary with key 'getBugs' and
                                  values 0 (false = default) or 1 (true)
