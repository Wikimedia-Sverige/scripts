/** 
 * Google Apps Script - List all files & folders in a Google Drive folder, & write into a speadsheet.
 *    - Main function 1: List all folders
 *    - Main function 2: List all files & folders
 * 
 * Hint: Set your folder ID first! You may copy the folder ID from the browser's address field. 
 *       The folder ID is everything after the 'folders/' portion of the URL.
 * 
 * @version 1.0
 * @see     https://github.com/mesgarpour
 */
 
// TODO: Set folder ID
var folderId = '';
var projectsFolderId = "";
 
// Main function 1: List all folders, & write into the current sheet.
function listFolers(){
  getFolderTree(folderId, false, 0);
};

// Main function 2: List all files & folders, & write into the current sheet.
function listAll(){
  getFolderTree(folderId, true, 0); 
};

function listProjects() {
  getFolderTree(projectsFolderId, false, 2, true);
};

// =================
// Get Folder Tree
function getFolderTree(folderId, listAll, maxDepth, onlyChildren) {
  // Initialise the sheet
  var sheet = SpreadsheetApp.getActiveSheet();
  try {
  // Get folder by id
  var parentFolder = DriveApp.getFolderById(folderId);
  
  //sheet.clear();
  sheet.appendRow(["######################################################################################"]);
  sheet.appendRow(["Full Path", "Name", "Date", "URL", "Last Updated", "Description", "Size", "Number of Files"]);
    
  // Get files and folders
  getChildFolders(parentFolder.getName(), parentFolder, sheet, listAll, maxDepth, onlyChildren);
  
  } catch (e) {
    sheet.appendRow(["Couldn't read folder: " + folderId + ", exception: " + e]);
    //Logger.log(e.toString());
  }
};

// Get the list of files and folders and their metadata in recursive mode
function getChildFolders(parentName, parent, sheet, listAll, maxDepth, onlyChildren) {
  Logger.log("> getChildFolders(): %s", onlyChildren);
  var childFolders = parent.getFolders();
  
  // List folders inside the folder
  while (childFolders.hasNext()) {
    var childFolder = childFolders.next();
    // Logger.log("Folder Name: " + childFolder.getName());
    var numberOfFiles = -1;
    if(!onlyChildren) {
      numberOfFiles = countFiles(childFolder)
    }
    data = [ 
      parentName + "\\" + childFolder.getName(),
      childFolder.getName(),
      childFolder.getDateCreated(),
      childFolder.getUrl(),
      childFolder.getLastUpdated(),
      childFolder.getDescription(),
      childFolder.getSize(),
      numberOfFiles
    ];
    // Write
    sheet.appendRow(data);
    
    // List files inside the folder
    var files = childFolder.getFiles();
    if(listAll) {
      while (files.hasNext()) {
        var childFile = files.next();
        // Logger.log("File Name: " + childFile.getName());
        data = [ 
          parentName + "\\" + childFolder.getName() + "\\" + childFile.getName(),
          childFile.getName(),
          childFile.getDateCreated(),
          childFile.getUrl(),
          childFile.getLastUpdated(),
          childFile.getDescription(),
          childFile.getSize(),
          childFile.getDownloadUrl()
        ];
        // Write
        sheet.appendRow(data);
      }
    }
    var newMaxDepth = undefined;
    // Recursive call of the subfolder
    if(maxDepth !== undefined) {
      newMaxDepth = maxDepth - 1;
    }
    if(newMaxDepth === undefined || newMaxDepth > 0) {
      getChildFolders(parentName + "\\" + childFolder.getName(), childFolder, sheet, listAll, newMaxDepth, false);
    }
  }
};

function countFiles(folder) {
  var numberOfFiles = 0;
  var files = folder.getFiles();
  while(files.hasNext()) {
    numberOfFiles ++;
    files.next();
  }
  var folders = folder.getFolders();
  while(folders.hasNext()) {
    numberOfFiles += countFiles(folders.next());
  }
  return numberOfFiles;
}
