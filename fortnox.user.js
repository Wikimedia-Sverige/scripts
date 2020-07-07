// ==UserScript==
// @name     Fortnox
// @version  1.17
// @grant    none
// @require  https://code.jquery.com/jquery-3.3.1.min.js
// @include  https://apps*.fortnox.se/time/time_time/*
// @downloadURL https://github.com/Wikimedia-Sverige/scripts/raw/master/fortnox.user.js
// ==/UserScript==

$(function() {
  var projects = {
    992400: "Anställda",
    992401: "Anställda - Utbildning",
    992501: "Externa",
    992600: "Infrastruktur",
    172511: "EU-ansökan om HOT",
    183102: "FindingGLAMs 2018",
    183103: "Wikipedia i utbildning 2018",
    183104: "Samsyn 2018",
    183116: "Biblioteksdata 2018",
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
    186203: "Wikimania 2019",
    186301: "Föreningsengagemang 2018",
    186302: "FOSS för föreningen 2018",
    193103: "Wikipedia i utbildning 2019",
    193116: "Strategisk inkludering av biblioteksdata på Wikidata 2019",
    193117: "Wikipedia i biblioteken 2019",
    193120: "GLAM 2019",
    193121: "MP - Musikverket 2019",
    193122: "Fri Musik på Wikipedia 2019",
    193126: "MP - Problematisk information 2018",
    193127: "MP - SMHI 2019",
    193128: "MP - Föreläsningar 2019",
    193202: "Påverkansarbete 2019",
    194101: "Förtroende 2019",
    194102: "Synlighet 2019",
    194103: "Wikipedia och Globala målen 2019",
    194202: "Buggrapportering och översättning 2019",
    194203: "Wikispeech 2019",
    194204: "Kunskap i krissituationer 2019",
    194205: "Wikispeech - Talresursinsamlaren 2019",
    195101: "Stöd till gemenskapen 2019",
    195102: "Utvecklingsstöd 2019",
    195202: "Wiki Loves 2019",
    195203: "En gemenskap för alla 2019",
    195205: "Fake News 2019",
    196101: "Organisationsutveckling 2019",
    196102: "Verktyg för partnerskap 2019 – Blueprinting",
    196201: "Erfarenhetsutbyte 2019",
    196301: "Föreningsengagemang 2019",
    196302: "FOSS för föreningen 2019",
    195204: "Wikimania 2019",
    194206: "Wikispeech för AI 2020",
    203103: "Wikipedia i utbildning 2020",
    203120: "GLAM 2020",
    203128: "Föreläsningar 2020",
    203202: "Påverkansarbete 2020",
    204101: "Förtroende 2020",
    204102: "Synlighet 2020",
    204202: "Buggrapportering och översättning 2020",
    204204: "Kunskap i krissituationer 2020",
    205101: "Stöd till gemenskapen 2020",
    205102: "Utvecklingsstöd 2020",
    205202: "Wiki Loves 2020",
    205203: "En gemenskap för alla 2020",
    206101: "Organisationsutveckling 2020",
    206102: "Verktyg för partnerskap 2020 – Blueprinting",
    206201: "Erfarenhetsutbyte 2020",
    206301: "Föreningsengagemang 2020",
    206302: "FOSS för föreningen 2020",
  };
  for(let i = 0; i < 14; i ++) {
    let projectName = projects[$("#project_" + i).val()];
    let $projectInput = $("#project_" + i);
    $("<span></span>")
      .text(projectName)
      .css({
        "white-space": "normal",
        "border-left": "1px solid black"
      })
      .insertAfter($projectInput);
    $projectInput.on("blur", function() {
      let projectNumber = Number(this.value);
      if(projectNumber === 0){
        $(this).next().text("");
      } else {
        let selectedProject = projects[projectNumber];
        $(this).next().text(selectedProject);
      }
    });
  }
});
