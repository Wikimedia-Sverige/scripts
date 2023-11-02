// ==UserScript==
// @name        Fortnox login
// @version     1.1
// @grant       none
// @require     https://tools-static.wmflabs.org/cdnjs/ajax/libs/jquery/3.4.1/jquery.slim.min.js
// @include     https://*.fortnox.se/*
// @downloadURL https://github.com/Wikimedia-Sverige/scripts/raw/master/fortnox-login.user.js
// ==/UserScript==

$(function() {
  'use strict';

  var anchors = document.querySelectorAll('a.Header_loginBtn__wQ_VG');
  anchors.forEach(e => e.setAttribute('target', '_self'));
});

