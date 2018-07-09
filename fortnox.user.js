// ==UserScript==
// @name     Fortnox
// @version  1
// @grant    none
// @require  https://code.jquery.com/jquery-3.3.1.min.js
// @include  https://apps*.fortnox.se/time/time_time/*
// @downloadURL https://github.com/Wikimedia-Sverige/scripts/raw/master/fortnox.user.js
// ==/UserScript==

$(function() {
  var projects = {
    992400: "Anställda",
    992500: "Externa",
    172511: "EU-ansökan om HOT",
    183102: "Kopplat Öppet Kulturarv 2018",
    183103: "Wikipedia i utbildning 2018",
    183104: "Samsyn 2018",
    173125: "Statens museer för världskultur 2017 - Uppladdning",
    173129: "Statens museer för världskultur 2017 - WiR",
    173126: "3D2Commons 2017",
    183121: "Musikverket 2018",
    183120: "GLAM 2018",
    183128: "Föreläsningar 2018",
    183115: "GLAM-pedagoger 2018",
    183202: "Påverkansarbete 2018",
    183205: "Sounds of Change 2018",
    183206: "Wikipedian in Residence 2018",
    184101: "Förtroende 2018",
    184102: "Synlighet 2018",
    184202: "Buggrapportering och översättning 2018",
    184203: "Wikispeech 2018",
    184204: "Kunskap i krissituationer 2018",
    185101: "Stöd till gemenskapen 2018",
    185102: "Utvecklingsstöd 2018",
    185202: "Wiki Loves 2018",
    185203: "En gemenskap för alla 2018",
    186101: "Organisationsutveckling 2018",
    186201: "Erfarenhetsutbyte 2018",
    186301: "Föreningsengagemang 2018",
    186302: "FOSS för föreningen 2018"
  };
  for(let i = 0; i < 14; i ++) {
    let projectName = projects[$("#project_" + i).val()];
    $("#project_" + i).after($('<img alt="🛈" title="' + projectName + '"/>'));
    $(this).next().attr("title", projectName);
    $("#project_" + i).on("change", function() {
      let projectName2 = projects[this.value];
      $(this).next().attr("title", projectName2);
    });
    let projectName2 = projects[this.value];
    $(this).next().attr("title", projectName2);
  }
});
