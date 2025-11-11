package com.automation.tests;

import org.junit.Test;
import org.testng.Assert;
import com.automation.utils.Log;
import com.automation.utils.ExcelUtils;
import com.automation.base.BaseTest;
import com.automation.pages.LoginPage;

public class LoginTest extends BaseTest {

    @Test
    public void verifyLogin() {
        Log.startTestCase("validLoginTest");
        Log.info("Navigating to login page");
        String path = "C:\\Users\\smile\\PycharmProjects\\practise_project_zoey\\src\\resources\\test_data\\LoginTest.xlsx";
        ExcelUtils excel = new ExcelUtils(path, "Sheet1");

        String username = excel.getCellData(1, 0);
        String password = excel.getCellData(1, 1);
        String expectedResult = excel.getCellData(1, 2);


        LoginPage login = new LoginPage(driver);
        login.login(username, password);

        Log.info("Verifying login");

        if (expectedResult.equalsIgnoreCase("Success")) {
            Assert.assertTrue(login.isLoginSuccessful(), "Login should be successful but failed.");
        } else if (expectedResult.equalsIgnoreCase("Failure")) {
            String actualError = login.getErrorMessage();
            Assert.assertTrue(actualError.contains("Invalid"),
                    "Expected failure message not displayed.");
        }
        Log.endTestCase("validLoginTest");

    }
}
