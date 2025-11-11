package com.automation.utils;

import org.apache.poi.ss.usermodel.*;
import java.io.FileInputStream;

public class ExcelUtils {
    private Sheet sheet;

    public ExcelUtils(String excelPath, String sheetName) {
        try {
            FileInputStream fis = new FileInputStream(excelPath);
            Workbook workbook = WorkbookFactory.create(fis);
            sheet = workbook.getSheet(sheetName);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public String getCellData(int rowNum, int colNum) {
        return sheet.getRow(rowNum).getCell(colNum).toString();
    }
}

