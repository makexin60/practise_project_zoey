package com.automation.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class LoginPage {
    WebDriver driver;

    // Locators
    By username = By.name("email");
    By password = By.name("password");
    By loginBtn = By.id("dologin");

    public LoginPage(WebDriver driver) {
        this.driver = driver;
    }

    // Actions
    public void login(String user, String pass) {
        driver.findElement(username).sendKeys(user);
        driver.findElement(password).sendKeys(pass);
        driver.findElement(loginBtn).click();
    }
}
