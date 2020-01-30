// ==UserScript==
// @name        Phabricator
// @version     1.0
// @grant       none
// @require     https://code.jquery.com/jquery-3.4.1.slim.min.js
// @include     https://phabricator.wikimedia.org/*
// @downloadURL https://github.com/Wikimedia-Sverige/scripts/raw/master/phabricator.user.js
// ==/UserScript==

$(function() {
    $("<a></a>")
        .attr("href", "/notification/query/unread/")
        .addClass("alert-notifications alert-unread")
        .append(
            $("<span></span>")
                .addClass("phabricator-main-menu-alert-icon phui-icon-view phui-font-fa fa-bullhorn")
        )
        .insertAfter(".alert-unread");
});
