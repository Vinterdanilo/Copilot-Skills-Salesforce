---
applyTo: "**/*Test.cls,**/*_Test.cls,**/*Tests.cls"
description: "Apex test rules"
---
# Apex tests — path-scoped rules

- Arrange-Act-Assert. `@TestSetup` + a `TestDataFactory`; never `@SeeAllData=true`.
- Every test method has at least one `Assert.*` with a message describing the expected behavior. A test without asserts is a defect, not coverage.
- Minimum scenario set per public service method: **positive**, **negative/exception**, **bulk (200+ records)** and, for user-facing code, **`System.runAs` with a restricted user** to prove USER_MODE behavior.
- Wrap the act step in `Test.startTest()` / `Test.stopTest()`; assert async results after `stopTest()`.
- Mock callouts with `HttpCalloutMock` / `Test.setMock`. Note: `@IntegrationTest` (Developer Preview, scratch orgs only) can hit real endpoints but does not count for coverage and needs `@TearDown` cleanup — never use it as the only test.
- Naming: `methodName_scenario_expectedResult`.
- Coverage target comes from `.github/salesforce-platform.json → quality.coverageTarget`; do not pad coverage with assert-free tests to reach it.
