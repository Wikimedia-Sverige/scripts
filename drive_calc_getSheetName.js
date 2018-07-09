var delimiterLookup = {
    "COMMA": ",",
    "SEMICOLON": ";",
    "PERIOD": ".",
    "SPACE": " "
}

/**
 * Returns the name of the sheet where the given cell recides.
 *
 * @param {string} ref The cell for which we want the sheet.
 * @return The name of the sheet where the cell recides.
 * @customfunction
 */
function getSheetName(ref) {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var cell = getCellReference(1);
    return ss.getRange(cell).getSheet().getName();
}

function getDelimiter() {
    return delimiterLookup[SpreadsheetApp.TextToColumnsDelimiter];
}

function getCellReference(argNo) {
    var sheet = SpreadsheetApp.getActiveSheet();
    var formula = SpreadsheetApp.getActiveRange().getFormula();
    var args = returnFormulaArgs(formula)
    if (argNo > args.length) {
        throw new Error("Not enough arguments.");
    }

    return args[argNo - 1]; // enumeration starts at 0
}

// extract cell reference formula arguments
function returnFormulaArgs(formula) {
    var args = formula.match(/=\w+\((.*)\)/i)[1].split(getDelimiter());
    for (i = 0; i < args.length; i++) {
        var arg = args[i].trim().split('!')
        arg[0] = arg[0].replace(/'/g, '')
        args[i] = arg.join('!');
    }
    return args;
}
