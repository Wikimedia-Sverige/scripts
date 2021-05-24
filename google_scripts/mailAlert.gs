var subject = "Du har nya mejl hos din WMSE-adress";
var body = '<p style="font-size: large">Det finns <b>{amount}</b> nya mejl hos din WMSE-mejl. Logga in på <a href="webmail.wikimedia.se">webmail.wikimedia.se</a> för att läsa dem.</p><p>Det här är ett automatiskt utskick som du får eftersom du har en mejladress hos Wikimedia Sverige. Vill ändra hur ofta du får dessa utskick, följ <a href="https://se.wikimedia.org/wiki/GSuite/Inst%C3%A4llning_f%C3%B6r_avisering_av_mail">instruktionerna på vår wiki</a>. Har du andra frågor om dessa utskick, kontakta <a href="mailto:drift@wikimedia.se">drift@wikimedia.se</a>.</p>';
var maintenanceAddress = "drift@wikimedia.se";
var spreadsheetId = "111tOiT0gBu25feH5lHc5Ukp6AUhYLgPlmJhyDkGIZSs";
var spreadsheet = SpreadsheetApp.openById(spreadsheetId);
var unreadMessagesSheet = spreadsheet.getSheetByName("Unread messages");
var errorSheet = spreadsheet.getSheetByName("Error message time");
var emailAddress = Session.getActiveUser().getEmail();
// Send error emails at most every 24 hours.
var errorInterval = 1000 * 60 * 60 * 24;

function checkForNewMessages() {
    try {
        Logger.log("User: " + Session.getActiveUser());
        Logger.log("Checking email for '" + emailAddress + "'...");
        var alertAddress = getAlertAddress();
        if(alertAddress) {
            // Unread messages in the inbox
            var unread = getUnreadFromInbox();
            Logger.log("Unread messages in inbox: (" + unread.length + ") " + unread);
            // Unread messages last time we checked.
            var oldUnread = loadUnread();
            Logger.log("Unread messages last check: (" + oldUnread.length + ") " + oldUnread);
            saveUnread(unread);
            // Unread messages that was not there last time we checked.
            var newUnread = unread.filter(x => !oldUnread.includes(x));
            Logger.log("New messages: (" + newUnread.length + ") " + newUnread);
            if(newUnread.length) {
                var numberOfUread = newUnread.length;
                var bodyHtml = body.replace("{amount}", numberOfUread);
                GmailApp.sendEmail(alertAddress, subject, null, {htmlBody: bodyHtml});
                Logger.log("Alert message sent.");
            }
        } else {
            Logger.log("No alert email address found.");
        }
    } catch (e) {
        Logger.log(e);
        var cell = errorSheet.getRange("A1");
        var lastErrorTime = cell.getValue();
        var time = new Date().getTime();
        var timeSinceLastErrorMessage = time - lastErrorTime;
        if(lastErrorTime === "" || timeSinceLastErrorMessage > errorInterval) {
            GmailApp.sendEmail(maintenanceAddress, "Email alert error", Logger.getLog());
            cell.setValue(time);
        }
        throw(e);
    }
}

function getAlertAddress() {
    var files = DriveApp.getRootFolder().getFilesByName("Mejladress för avisering");
    if(!files.hasNext()) {
        Logger.log("No alert address file found.");
        return null;
    }
    var fileId = files.next().getId();
    var file = DocumentApp.openById(fileId);
    if(!file) {
        Logger.log("Couldn't open address file.");
        return null;
    }
    var address = file.getBody().getText();
    return address;
}

function getUnreadFromInbox() {
    var unreadMessages = [];
    var threads = GmailApp.getInboxThreads();
    for(var thread of threads) {
        for(var message of thread.getMessages()) {
            if(message.isUnread()) {
                var id = message.getId();
                unreadMessages.push(id);
            }
        }
    }
    return unreadMessages;
}

function saveUnread(messages) {
    var messagesString = messages.join(" ");
    var unread = getUnreadFromSaved();
    if(unread) {
        unread.setValue(messagesString);
    } else {
        unreadMessagesSheet.appendRow([emailAddress, messagesString]);
    }
}

function getUnreadFromSaved() {
    var range = unreadMessagesSheet.getDataRange();
    var values = range.getValues();
    for(var i = 0; i < values.length; i ++) {
        var value = values[i];
        var address = value[0];
        if(value[0] === emailAddress) {
            var range = unreadMessagesSheet.getRange(i + 1, 2);
            return range;
        }
    }
}

function loadUnread() {
    var unread = getUnreadFromSaved();
    if(unread === undefined || unread.getValue() === "") {
        return [];
    }
    var messages = unread.getValue().split(" ");
    return messages;
}

// Deprecated functions.

function sendAlertMail() {
    checkForNewMessages();
}

function sendAlertMailDocument() {
    checkForNewMessages();
}
