var rangeRef = "Staff!G1" // this is the cell in which the allowed personnel range (on the same sheet) is specified.
var delimiterMap = {
    "COMMA": ",",
    "SEMICOLON": ";",
    "PERIOD": ".",
    "SPACE": " "
}

/**
 * Returns the name of the sheet where the given cell recides.
 *
 * @param {string} cell The cell for which we want the sheet.
 * @param {string} trigger A cell reference which can be used to trigger a recalculation.
 * @return The name of the sheet where the cell recides.
 * @customfunction
 */
function getSheetName(cell, trigger) {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var ref = getCellReference(1);
    return ss.getRange(ref).getSheet().getName();
}

function getCellReference(argNo) {
    var sheet = SpreadsheetApp.getActiveSheet();
    var formula = SpreadsheetApp.getActiveRange().getFormula();
    var args = getFormulaArgs(formula)
    if (argNo > args.length) {
        throw new Error("Not enough arguments.");
    }

    return args[argNo - 1]; // enumeration starts at 0
}

// extract cell reference formula arguments
function getFormulaArgs(formula) {
    var args = formula.match(/=\w+\((.*)\)/i)[1].split(getDelimiter());
    for (var i = 0; i < args.length; i++) {
        var arg = args[i].trim().split('!')
        arg[0] = arg[0].replace(/'/g, '')
        args[i] = arg.join('!');
    }
    return args;
}

function getDelimiter() {
    return delimiterMap[SpreadsheetApp.TextToColumnsDelimiter];
}

/**
 * Returns the total personnel costs
 *
 * @param {string} stafflist The cell containing a list of personnel and percentages.
 * @param {number} extra (optional) The cell containing any other cost to be added (e.g. correction due to salary increase)
 * @return The sum of personnel costs
 * @customfunction
 */
function personnelCosts(stafflist, extra) {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var rangeA1 = ss.getRange(rangeRef).getSheet().getName() + "!" + ss.getRange(rangeRef).getValue();
    var range = ss.getRange(rangeA1);

    var list = parseListIntoVals(stafflist);
    var sum = 0;
    for (var i = 0; i < list.length; i++) {
        var fullcost = matchInitialToCell(list[i][0], range);
        sum = sum + (fullcost * list[i][1] / 100);
    }

    if (typeof extra !== 'undefined') {
        sum = sum + extra;
    }

    return sum;
}

// parse "AC" or "AC50" into (AC, 100) and (AC, 50)
function splitInitialsAndPercent(value) {
    var text = value.replace(/[0-9]/g, "");
    var percent = value.slice(text.length);
    if (percent.length === 0) {
        percent = 100;
    } else {
        percent = parseInt(percent);
    }
    return [text, percent];
}

// parse "AC, EB50" into [(AC, 100), (EB, 50)]
function parseListIntoVals(value) {
    var list = value.split(',');
    for (var i = 0; i < list.length; i++) {
        list[i] = splitInitialsAndPercent(list[i].trim());
    }
    return list;
}

// check if an initial is present in a given range. If so return the value to the right of it
function matchInitialToCell(text, range) {
    if (range.getNumColumns() !== 2) {
        throw new Error("The expected salary range must have two columns.");
    }
    var numRows = range.getNumRows();
    for (var i = 1; i <= numRows; i++) {
        var cellValue = range.getCell(i, 1).getValue();
        if (cellValue === text) {
            return range.getCell(i, 2).getValue();
        }
    }
    throw new Error("Could not match the initial to a value.");
}

// Test splitInitialsAndPercent()
function runTests() {
    test_splitInitialsAndPercent_explicit();
    test_splitInitialsAndPercent_implicit();
    test_parseListIntoVals();
    test_returnFormulaArg();
}

function assertArrayEquals(result, expected, errorText) {
    if (result.length !== expected.length) {
        throw new Error(errorText + ": " + result + " !== " + expected);
    }
    for (i = 0; i < expected.length; i++) {
        if (result[i] instanceof Array && expected[i] instanceof Array) {
            // recurse into the nested arrays
            assertArrayEquals(result[i], expected[i], errorText)
        } else if (result[i] !== expected[i]) {
            throw new Error(errorText + ": " + result + " !== " + expected);
        }
    }
}

// Test splitInitialsAndPercent()
function test_splitInitialsAndPercent_explicit() {
    var val = "AC50";
    var result = splitInitialsAndPercent(val);
    var expected = ["AC", 50];
    assertArrayEquals(result, expected, "splitInitialsAndPercent() broken");
}

function test_splitInitialsAndPercent_implicit() {
    var val = "AC";
    var result = splitInitialsAndPercent(val);
    var expected = ["AC", 100];
    assertArrayEquals(result, expected, "splitInitialsAndPercent() broken");
}

// Test parseListIntoVals()
function test_parseListIntoVals() {
    var val = "AC, EB50";
    var result = parseListIntoVals(val);
    var expected = [
        ["AC", 100],
        ["EB", 50]
    ];
    assertArrayEquals(result, expected, "parseListIntoVals() broken");
}

// Test returnFormulaArgs()
function test_returnFormulaArg() {
    formula = "=GETPERSONELLCOSTS('Blad 1'!A10, A11)";
    result = returnFormulaArgs(formula);
    expected = ["Blad 1!A10", "A11"]
    assertArrayEquals(result, expected, "returnFormulaArgs() broken");
}

