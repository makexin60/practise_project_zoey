package com.automation.tests;

import org.junit.Test;
import org.testng.annotations.Test;
import com.automation.base.BaseTest;
import com.automation.pages.LoginPage;

public class LoginTest extends BaseTest {

    @Test
    public void verifyLogin() {
        LoginPage login = new LoginPage(driver);
        login.login("john", "1234");
        // Add assertions here
    }
}
