// ==UserScript==
// @name        Fortnox login
// @version     1.0
// @grant       none
// @require     https://code.jquery.com/jquery-3.4.1.slim.min.js
// @include     https://*.fortnox.se/*
// @downloadURL https://github.com/Wikimedia-Sverige/scripts/raw/master/fortnox-login.user.js
// ==/UserScript==

$(function() {
  var anchors = document.querySelectorAll('a.Header_loginBtn__wQ_VG');
    for (var i = 0; i < anchors.length; i++) {
      anchors[i].setAttribute('target', '_self');
    }
});

