package com.automation.base;

import com.automation.utils.ConfigReader;
import org.openqa.selenium.WebDriver;
import org.testng.annotations.*;
import com.automation.factory.DriverFactory;

import java.time.Duration;

public class BaseTest {
    protected WebDriver driver;
    protected ConfigReader config;

    @BeforeMethod
    public void setUp() {
        config = new ConfigReader("src/test/resources/config/config.properties");
        String browser = config.getProperty("browser");
        driver = DriverFactory.initDriver(browser);
        driver.get(config.getProperty("url"));
        driver.manage().timeouts().implicitlyWait(
                Duration.ofSeconds(Long.parseLong(config.getProperty("timeout")))
        );
    }

    @AfterMethod
    public void tearDown() {
        driver.quit();
    }
}
