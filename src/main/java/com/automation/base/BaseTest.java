package com.automation.base;

import org.openqa.selenium.WebDriver;
import org.testng.annotations.*;
import com.automation.factory.DriverFactory;

public class BaseTest {
    protected WebDriver driver;

    @BeforeMethod
    public void setUp() {
        driver = DriverFactory.initDriver("chrome");
        driver.get("https://www.126.com/");
    }

    @AfterMethod
    public void tearDown() {
        driver.quit();
    }
}
