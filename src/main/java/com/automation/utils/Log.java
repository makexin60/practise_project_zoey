package com.automation.utils;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class Log {
    private static final Logger logger = LogManager.getLogger(Log.class);

    public static void startTestCase(String testName) {
        logger.info("===== Starting test: " + testName + " =====");
    }

    public static void endTestCase(String testName) {
        logger.info("===== Finished test: " + testName + " =====");
    }

    public static void info(String message) {
        logger.info(message);
    }

    public static void warn(String message) {
        logger.warn(message);
    }

    public static void error(String message) {
        logger.error(message);
    }
}

