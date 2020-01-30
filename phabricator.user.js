// ==UserScript==
// @name     Phabricator
// @version  1.0
// @grant    none
// @require  https://code.jquery.com/jquery-3.4.1.slim.min.js
// @include  https://phabricator.wikimedia.org/*
// ==/UserScript==

$(function() {
    $("<a></a>")
        .attr("href", "/notification/query/unread/")
        .addClass("alert-notifications")
        .append(
            $("<span></span>")
                .addClass("phabricator-main-menu-message-icon phui-icon-view phui-font-fa fa-bullhorn")
        )
        .insertAfter(".alert-unread");
});
