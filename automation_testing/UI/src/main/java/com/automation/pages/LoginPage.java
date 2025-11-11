package com.automation.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;


public class LoginPage {
    WebDriver driver;
    @FindBy(linkText = "Log out")
    private WebElement logoutLink;  // Appears only if login succeeds

    @FindBy(css = ".message-error")
    private WebElement errorMessage; // Error message on failed login

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

    public boolean isLoginSuccessful() {
        try {
            // Check if logout link is displayed
            return logoutLink.isDisplayed();
        } catch (NoSuchElementException e) {
            return false; // Login failed
        }
    }

    public String getErrorMessage() {
        try {
            return errorMessage.getText();
        } catch (NoSuchElementException e) {
            return ""; // No error message displayed
        }
    }
}
